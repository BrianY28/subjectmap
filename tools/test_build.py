"""Regression checks for source validation and self-contained site navigation."""
import contextlib
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

import build
import nodelib


NODE = '''---
order: 10
when: "1860s-present"
status: established
sources:
  - "Example source. https://example.org/paper?a=1&b=2"
drafted_by: Codex (AI)
reviewed_by:
---

# Chemical equilibrium

A closed ideal model with A and B.

## Concepts

- **Mass action**: At equilibrium, Q equals K. [Explainer](../../explainers/equilibrium/)
- **Dynamic balance**: Forward and reverse rates are equal.
'''


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        branch = self.root / 'nodes' / '01-foundations'
        branch.mkdir(parents=True)
        self.branch = branch / 'README.md'
        self.branch.write_text('---\nspan: "1661-present"\n---\n\n# Foundations\n\nA starting point.\n', encoding='utf-8')
        self.node = branch / 'chemical-equilibrium.md'
        self.node.write_text(NODE, encoding='utf-8')
        explainer = self.root / 'explainers' / 'equilibrium' / 'index.html'
        explainer.parent.mkdir(parents=True)
        explainer.write_text('<h1>Equilibrium</h1><a href="../../index.html">Map</a>', encoding='utf-8')
        for target, name, value in ((nodelib, 'ROOT', self.root), (nodelib, 'NODES', self.root / 'nodes'), (build, 'ROOT', self.root)):
            patcher = patch.object(target, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_build(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = build.main(list(args))
        return result, output.getvalue()

    def test_build_is_deterministic_and_check_detects_stale_output(self):
        self.assertEqual(self.run_build()[0], 0)
        before = {p.relative_to(self.root / 'site'): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()}
        self.assertEqual(self.run_build('--check')[0], 0)
        self.assertEqual(self.run_build()[0], 0)
        after = {p.relative_to(self.root / 'site'): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.node.write_text(NODE.replace('Dynamic balance', 'Reversible balance'), encoding='utf-8')
        result, output = self.run_build('--check')
        self.assertEqual(result, 1)
        self.assertIn('out of date', output)

    def test_all_generated_local_links_resolve_including_fragments(self):
        self.assertEqual(self.run_build()[0], 0)
        site = self.root / 'site'
        for page in site.rglob('*.html'):
            parsed = Links()
            parsed.feed(page.read_text(encoding='utf-8'))
            for ref in parsed.references:
                url = urlsplit(ref)
                if url.scheme or url.netloc:
                    continue
                target = (page.parent / unquote(url.path)).resolve() if url.path else page.resolve()
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.is_file(), f'{page}: missing {ref}')
                self.assertTrue(target.is_relative_to(site.resolve()), ref)
                if url.fragment:
                    destination = Links()
                    destination.feed(target.read_text(encoding='utf-8'))
                    self.assertIn(unquote(url.fragment), destination.ids, ref)
        self.assertIn('(nodes/chemical-equilibrium.html)', build.markmap_md(nodelib.load()))

    def test_opml_round_trip_preserves_unicode_and_notes(self):
        branches = nodelib.load()
        branches[0]['nodes'][0]['note'] = 'ΔG < 0 & Q ≠ K'
        tree = ET.fromstring(build.opml(branches))
        node = tree.find('./body/outline/outline/outline')
        self.assertIn('ΔG < 0 & Q ≠ K', node.attrib['_note'])
        self.assertEqual(len(node.findall('outline')), 2)

    def test_text_cannot_inject_html_script_or_markdown_links(self):
        branches = nodelib.load()
        node = branches[0]['nodes'][0]
        node['title'] = '</script><script>alert(1)</script>'
        node['note'] = '<img src=x onerror=alert(1)> __MARKMAP__'
        node['concepts'][0]['title'] = '[Click](javascript:alert(1))'
        node['sources'] = ['<script>alert(1)</script> https://example.org/?x=" onclick="bad']
        page = build.topic_page(branches[0], node)
        parsed = Links()
        parsed.feed(page)
        self.assertNotIn('script', parsed.tags)
        self.assertNotIn('img', parsed.tags)
        self.assertTrue(all(not ref.startswith('javascript:') for ref in parsed.references))
        markdown = build.markmap_md(branches)
        self.assertNotIn('</script>', markdown)
        self.assertIn(r'\[Click\]\(javascript:alert\(1\)\)', markdown)
        build.build_site(branches, build.index_md(branches), build.opml(branches))
        home = (self.root / 'site' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('__MARKMAP__', home)  # A token in source text must not expand.
        self.assertNotIn('<script>alert(1)</script>', home)

    def test_bad_metadata_returns_actionable_error_without_traceback(self):
        cases = [
            (NODE.replace('order: 10', 'order: ten'), 'whole number'),
            (NODE.replace('order: 10', 'order: 10\norder: 20'), 'duplicate field'),
            (NODE.replace('status: established', 'status: open\nas_of: 2026-02-30'), 'real date'),
            (NODE.replace('sources:\n  - "Example source. https://example.org/paper?a=1&b=2"', 'sources: []'), 'bare value'),
            (NODE.replace('drafted_by: Codex (AI)', 'drafted_by:\n  - Codex'), 'must name'),
            (NODE.replace('../../explainers/equilibrium/', '../../explainers/../../private/'), 'explainer must'),
        ]
        for text, message in cases:
            with self.subTest(message=message):
                self.node.write_text(text, encoding='utf-8')
                result, output = self.run_build('--check')
                self.assertEqual(result, 1)
                self.assertIn(message, output)
                self.assertNotIn('Traceback', output)

    def test_missing_or_malformed_branch_heading_is_reported(self):
        self.branch.write_text('---\nspan: 1800-present\n---\nFoundations\n', encoding='utf-8')
        self.assertIn("branch body must start", self.run_build('--check')[1])
        self.branch.unlink()
        self.assertIn('missing README.md', self.run_build('--check')[1])

    def test_duplicate_numeric_orders_are_rejected(self):
        other = self.node.with_name('another-topic.md')
        other.write_text(NODE.replace('order: 10', 'order: 010'), encoding='utf-8')
        self.assertIn('two nodes share', self.run_build('--check')[1])

    def test_empty_sources_are_rejected(self):
        self.node.write_text(NODE.replace('Example source. https://example.org/paper?a=1&b=2', ''), encoding='utf-8')
        self.assertIn('cannot contain empty items', self.run_build('--check')[1])

    def test_missing_nodes_directory_is_reported(self):
        with patch.object(nodelib, 'NODES', self.root / 'missing'):
            self.assertIn('missing directory', self.run_build('--check')[1])


if __name__ == '__main__':
    unittest.main()
