"""Regression checks for shared builds, source validation and local navigation."""
import contextlib
import copy
import io
import json
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
        self.config = {'title': 'SubjectMap', 'repository': 'https://github.com/example/subjectmap',
                       'site_url': 'https://example.github.io/subjectmap/', 'subjects': []}
        for slug, name in [('physics', 'Physics'), ('chemistry', 'Chemistry')]:
            subject = self.root / 'subjects' / slug
            branch = subject / 'nodes' / '01-foundations'
            branch.mkdir(parents=True)
            (branch / 'README.md').write_text('---\nspan: "1661-present"\n---\n\n# Foundations\n\nA starting point.\n', encoding='utf-8')
            (branch / 'shared-topic.md').write_text(NODE.replace('Chemical equilibrium', name + ' topic'), encoding='utf-8')
            explainer = subject / 'explainers' / 'equilibrium' / 'index.html'
            explainer.parent.mkdir(parents=True)
            explainer.write_text('<title>An explainer</title><h1>Equilibrium</h1><a href="../../index.html">Map</a>', encoding='utf-8')
            self.config['subjects'].append({'id': slug, 'name': name, 'title': name + ' Map',
                'map_title': name + ': From basics to the frontier', 'headline': 'Explore ' + name,
                'description': name + ' concepts and sources', 'symbol': name[:2], 'explainer': 'equilibrium'})
        self.config_path = self.root / 'subjects.json'
        self.write_config()
        self.subject_root = self.root / 'subjects' / 'chemistry'
        self.branch = self.subject_root / 'nodes' / '01-foundations' / 'README.md'
        self.node = self.branch.with_name('shared-topic.md')
        patcher = patch.object(build, 'ROOT', self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_config(self, config=None):
        self.config_path.write_text(json.dumps(self.config if config is None else config), encoding='utf-8')

    def run_build(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = build.main(list(args))
        return result, output.getvalue()

    def subjects(self):
        return build.load_subjects(build.load_config())

    def test_two_subjects_preserve_separate_ids_metadata_exports_and_source_links(self):
        self.assertEqual(self.run_build()[0], 0)
        site = self.root / 'site'
        for slug, name in [('physics', 'Physics'), ('chemistry', 'Chemistry')]:
            topic = (site / slug / 'nodes' / 'shared-topic.html').read_text(encoding='utf-8')
            self.assertIn(f'<h1>{name} topic</h1>', topic)
            self.assertIn(f'/blob/main/subjects/{slug}/nodes/01-foundations/shared-topic.md', topic)
            self.assertIn('href="../../index.html"', topic)
            subject_opml = self.root / 'subjects' / slug / 'map.opml'
            self.assertEqual(subject_opml.read_bytes(), (site / slug / 'map.opml').read_bytes())
            self.assertIn(f'/subjectmap/{slug}/explainers/equilibrium/', subject_opml.read_text())
            self.assertIn(f'{name} Map index', (self.root / 'subjects' / slug / 'INDEX.md').read_text())
        self.assertFalse((self.root / 'map.opml').exists())
        self.assertFalse((site / 'map.opml').exists())
        self.assertIn('2 subjects, 2 topics, 4 concepts', (self.root / 'INDEX.md').read_text())

    def test_build_is_deterministic_and_check_detects_stale_output_in_each_subject(self):
        self.assertEqual(self.run_build()[0], 0)
        before = {p.relative_to(self.root / 'site'): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()}
        self.assertEqual(self.run_build('--check')[0], 0)
        self.assertEqual(self.run_build()[0], 0)
        after = {p.relative_to(self.root / 'site'): p.read_bytes() for p in (self.root / 'site').rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        for relative in ['INDEX.md', 'subjects/physics/INDEX.md', 'subjects/physics/map.opml',
                         'subjects/chemistry/INDEX.md', 'subjects/chemistry/map.opml']:
            output = self.root / relative
            original = output.read_bytes()
            output.write_text('stale', encoding='utf-8')
            result, message = self.run_build('--check')
            self.assertEqual(result, 1)
            self.assertIn(relative + ' out of date', message)
            self.assertEqual(output.read_text(), 'stale', '--check must not write outputs')
            output.write_bytes(original)
        self.node.write_text(NODE.replace('Dynamic balance', 'Reversible balance'), encoding='utf-8')
        result, message = self.run_build('--check')
        self.assertEqual(result, 1)
        self.assertIn('subjects/chemistry/INDEX.md', message)

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
        self.assertIn('(nodes/shared-topic.html)', build.markmap_md(self.subjects()[0]))

    def test_explainer_document_has_one_title(self):
        self.assertEqual(self.run_build()[0], 0)
        for slug in ('physics', 'chemistry'):
            parsed = Links()
            parsed.feed((self.root / 'site' / slug / 'explainers/equilibrium/index.html').read_text())
            self.assertEqual(parsed.tags.count('title'), 1)
            self.assertEqual(parsed.tags.count('html'), 1)
            self.assertEqual(parsed.tags.count('body'), 1)

    def test_opml_round_trip_preserves_unicode_and_notes(self):
        subject = self.subjects()[0]
        subject['branches'][0]['nodes'][0]['note'] = 'ΔG < 0 & Q ≠ K'
        tree = ET.fromstring(build.opml(subject, self.config))
        node = tree.find('./body/outline/outline/outline')
        self.assertIn('ΔG < 0 & Q ≠ K', node.attrib['_note'])
        self.assertEqual(len(node.findall('outline')), 2)

    def test_text_cannot_inject_html_script_or_markdown_links(self):
        subjects = self.subjects()
        subject = subjects[0]
        node = subject['branches'][0]['nodes'][0]
        node['title'] = '</script><script>alert(1)</script>'
        node['note'] = '<img src=x onerror=alert(1)> __MARKMAP__'
        node['concepts'][0]['title'] = '[Click](javascript:alert(1))'
        node['sources'] = ['<script>alert(1)</script> https://example.org/?x=" onclick="bad']
        page = build.topic_page(subject, subject['branches'][0], node, self.config, subjects)
        parsed = Links()
        parsed.feed(page)
        self.assertNotIn('script', parsed.tags)
        self.assertNotIn('img', parsed.tags)
        self.assertTrue(all(not ref.startswith('javascript:') for ref in parsed.references))
        markdown = build.markmap_md(subject)
        self.assertNotIn('</script>', markdown)
        self.assertIn(r'\[Click\]\(javascript:alert\(1\)\)', markdown)
        subject['description'] = '<img src=x onerror=alert(1)> __SUBJECTS__'
        build.build_site(self.config, subjects, build.generated_outputs(self.config, subjects))
        subject_home = (self.root / 'site/physics/index.html').read_text(encoding='utf-8')
        hub = (self.root / 'site/index.html').read_text(encoding='utf-8')
        self.assertIn('__MARKMAP__', subject_home)
        self.assertIn('__SUBJECTS__', hub)
        self.assertNotIn('<script>alert(1)</script>', subject_home)
        self.assertNotIn('<img src=x', hub)

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
                self.assertIn('subjects/chemistry/', output)
                self.assertNotIn('Traceback', output)

    def test_missing_or_malformed_branch_heading_is_reported(self):
        self.branch.write_text('---\nspan: 1800-present\n---\nFoundations\n', encoding='utf-8')
        self.assertIn('branch body must start', self.run_build('--check')[1])
        self.branch.unlink()
        self.assertIn('missing README.md', self.run_build('--check')[1])

    def test_duplicate_numeric_orders_are_rejected_within_subject(self):
        self.node.with_name('another-topic.md').write_text(NODE.replace('order: 10', 'order: 010'), encoding='utf-8')
        self.assertIn('two nodes share', self.run_build('--check')[1])

    def test_empty_sources_are_rejected(self):
        self.node.write_text(NODE.replace('Example source. https://example.org/paper?a=1&b=2', ''), encoding='utf-8')
        self.assertIn('cannot contain empty items', self.run_build('--check')[1])

    def test_missing_nodes_directory_is_reported(self):
        (self.subject_root / 'nodes').rename(self.subject_root / 'missing')
        self.assertIn('missing directory', self.run_build('--check')[1])

    def test_invalid_config_and_duplicate_or_escaping_subject_ids_are_reported(self):
        cases = []
        for value, message in [('../escape', 'lowercase-words'), ('assets', 'cannot'), ('physics', 'duplicate')]:
            config = copy.deepcopy(self.config)
            config['subjects'][1]['id'] = value
            cases.append((config, message))
        for value in [[], {'subjects': []}, {'title': 'SubjectMap', 'repository': 'http://unsafe.example', 'site_url': 'https://example.org', 'subjects': []}]:
            cases.append((value, 'subjects.json'))
        malformed_url = copy.deepcopy(self.config)
        malformed_url['repository'] = 'https://[invalid'
        cases.append((malformed_url, 'valid HTTPS URL'))
        for config, message in cases:
            with self.subTest(config=config):
                self.write_config(config)
                result, output = self.run_build('--check')
                self.assertEqual(result, 1)
                self.assertIn(message, output)
                self.assertNotIn('Traceback', output)
        self.config_path.write_text('{broken json', encoding='utf-8')
        self.assertEqual(self.run_build('--check')[0], 1)

    def test_subject_symlink_cannot_escape_subject_directory(self):
        outside = self.root / 'outside'
        (self.root / 'subjects/chemistry').rename(outside)
        (self.root / 'subjects/chemistry').symlink_to(outside, target_is_directory=True)
        self.assertIn('outside subjects', self.run_build('--check')[1])

    def test_explainer_cannot_escape_its_subject(self):
        subject = self.root / 'subjects/chemistry'
        page = subject / 'explainers/equilibrium/index.html'
        outside = self.root / 'outside.html'
        page.rename(outside)
        page.symlink_to(outside)
        self.assertIn('inside the subject', self.run_build('--check')[1])


if __name__ == '__main__':
    unittest.main()
