"""Read, validate and write node files. Standard library only.

A node file is Markdown with a small front-matter block:

    ---
    order: 10
    when: "1860s-present"
    status: established        # established | open
    as_of: 2026-11-10          # required when status is open
    sources:
      - "OpenStax (2019). Chemistry 2e, 13.2 Equilibrium Constants. https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants"
    drafted_by: Codex (AI)
    reviewed_by:
    ---

    # Chemical equilibrium

    One or two sentences: the core idea.

    ## Concepts

    - **Mass action**: At equilibrium, Q equals K. [Explainer](../../explainers/equilibrium/)

The front matter accepts only: `key: value`, `key:` followed by `  - item` lines, and
`# comments`. Values are bare words or "double-quoted strings".
"""
import datetime
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODES = ROOT / "nodes"

FIELDS = {"order", "when", "people", "status", "as_of", "sources", "drafted_by", "reviewed_by"}
LIST_FIELDS = {"people", "sources", "reviewed_by"}
BRANCH_FIELDS = {"span"}
CONCEPT_RE = re.compile(r"^- \*\*(?P<title>.+?)\*\*: (?P<note>.+?)(?: \[Explainer\]\((?P<explainer>[^)]+)\))?\s*$")


class NodeError(Exception):
    pass


def _scalar(raw, where):
    raw = raw.strip()
    if raw.startswith('"'):
        if not raw.endswith('"') or len(raw) < 2:
            raise NodeError(f"{where}: unterminated quoted string")
        return raw[1:-1].replace('\\"', '"')
    if raw.startswith(("'", "[", "{", "|", ">")):
        raise NodeError(f"{where}: use a bare value or a \"double-quoted\" string (found {raw[:12]!r})")
    return raw


def parse_front_matter(text, where):
    if not text.startswith("---\n"):
        raise NodeError(f"{where}: file must start with a '---' front-matter line")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise NodeError(f"{where}: front matter has no closing '---' line")
    meta, key = {}, None
    for n, line in enumerate(text[4:end].split("\n"), start=2):
        loc = f"{where}:{n}"
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if key is None or not isinstance(meta.get(key), list):
                raise NodeError(f"{loc}: list item without a list key above it")
            meta[key].append(_scalar(line[4:], loc))
            continue
        m = re.match(r"^([a-z_]+):(.*)$", line)
        if not m:
            raise NodeError(f"{loc}: cannot read this line: {line!r}")
        key, rest = m.group(1), m.group(2).strip()
        if key in meta:
            raise NodeError(f"{loc}: duplicate field '{key}'")
        if not rest.startswith('"'):
            rest = rest.split(" #", 1)[0].strip()
        meta[key] = [] if rest == "" else _scalar(rest, loc)
    return meta, text[end + 5:]


def quote(s):
    s = str(s)
    return s if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 .()'’,&-]*", s) and ": " not in s else '"' + s.replace('"', '\\"') + '"'


def dump_front_matter(meta, order):
    out = ["---"]
    for k in order:
        if k not in meta:
            continue
        v = meta[k]
        if isinstance(v, list):
            out.append(f"{k}:")
            out += [f"  - {quote(x) if k != 'sources' else chr(34) + str(x).replace(chr(34), chr(92) + chr(34)) + chr(34)}" for x in v]
        else:
            out.append(f"{k}: {v if k in ('order', 'as_of', 'status') else quote(v)}")
    out.append("---")
    return "\n".join(out) + "\n"


def parse_body(body, where):
    lines = body.strip("\n").split("\n")
    if not lines or not lines[0].startswith("# "):
        raise NodeError(f"{where}: body must start with '# Title'")
    title = lines[0][2:].strip()
    try:
        ci = lines.index("## Concepts")
    except ValueError:
        raise NodeError(f"{where}: missing '## Concepts' section")
    note = "\n".join(lines[1:ci]).strip()
    concepts = []
    for l in lines[ci + 1:]:
        if not l.strip():
            continue
        m = CONCEPT_RE.match(l)
        if not m:
            raise NodeError(f"{where}: concept lines must look like '- **Title**: One sentence.' (got {l[:60]!r})")
        concepts.append({k: v for k, v in m.groupdict().items() if v})
    return title, note, concepts


def load(root=None):
    """Return the whole map: [{dir, title, span, summary, nodes: [...]}, ...]."""
    root = Path(root) if root is not None else ROOT
    nodes_dir = root / "nodes" if root != ROOT else NODES
    branches = []
    if not nodes_dir.is_dir():
        raise NodeError("nodes/: missing directory")
    for bdir in sorted(p for p in nodes_dir.iterdir() if p.is_dir()):
        readme = bdir / "README.md"
        if not readme.is_file():
            raise NodeError(f"nodes/{bdir.name}/: missing README.md")
        meta, body = parse_front_matter(readme.read_text(encoding="utf-8"), str(readme.relative_to(root)))
        lines = body.strip().splitlines()
        if not lines or not lines[0].startswith("# ") or not lines[0][2:].strip():
            raise NodeError(f"{readme.relative_to(root)}: branch body must start with '# Title'")
        unknown = set(meta) - BRANCH_FIELDS
        if unknown:
            raise NodeError(f"{readme.relative_to(root)}: unknown field(s) {sorted(unknown)}")
        btitle, summary = lines[0][2:].strip(), "\n".join(lines[1:]).strip()
        nodes = []
        for f in sorted(bdir.glob("*.md")):
            if f.name == "README.md":
                continue
            rel = str(f.relative_to(root))
            m, b = parse_front_matter(f.read_text(encoding="utf-8"), rel)
            if not re.fullmatch(r"[0-9]+", str(m.get("order", ""))):
                raise NodeError(f"{rel}: 'order' must be a whole number")
            unknown = set(m) - FIELDS
            if unknown:
                raise NodeError(f"{rel}: unknown field(s) {sorted(unknown)}")
            title, note, concepts = parse_body(b, rel)
            nodes.append({"id": f.stem, "path": rel, "title": title, "note": note, "concepts": concepts, **m})
        nodes.sort(key=lambda n: int(n.get("order", 0)))
        branches.append({"dir": bdir.name, "path": str(readme.relative_to(root)), "title": btitle,
                         "summary": summary, "nodes": nodes, **meta})
    return branches


def validate(branches, root=None):
    root = Path(root) if root is not None else ROOT
    errs, ids = [], {}
    if not branches:
        errs.append("nodes/: add at least one branch")
    for b in branches:
        if not isinstance(b.get("span"), str) or not b["span"]:
            errs.append(f"{b['path']}: missing or invalid 'span'")
        if not re.fullmatch(r"[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*", b["dir"]):
            errs.append(f"{b['path']}: branch directory must be NN-lowercase-words")
        if not b["nodes"] or not b["summary"]:
            errs.append(f"{b['path']}: branch needs a summary and at least one node")
        orders = [int(n["order"]) if re.fullmatch(r"[0-9]+", str(n.get("order", ""))) else str(n.get("order")) for n in b["nodes"]]
        if len(set(orders)) != len(orders):
            errs.append(f"{b['dir']}: two nodes share the same 'order'")
        for n in b["nodes"]:
            p = n["path"]
            unknown = set(n) - FIELDS - {"id", "path", "title", "note", "concepts"}
            if unknown:
                errs.append(f"{p}: unknown field(s) {sorted(unknown)}")
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n["id"]):
                errs.append(f"{p}: file name must be lowercase-words-with-hyphens.md")
            if n["id"] in ids:
                errs.append(f"{p}: duplicate node id, also in {ids[n['id']]}")
            ids[n["id"]] = p
            if not str(n.get("order", "")).isdigit():
                errs.append(f"{p}: 'order' must be a whole number")
            for k in ("when", "status"):
                if not isinstance(n.get(k), str) or not n[k]:
                    errs.append(f"{p}: missing or invalid '{k}'")
            for k in LIST_FIELDS:
                if k in n and not isinstance(n[k], list):
                    errs.append(f"{p}: '{k}' must be a list of '  - item' lines")
                elif k in n and any(not isinstance(item, str) or not item.strip() for item in n[k]):
                    errs.append(f"{p}: '{k}' cannot contain empty items")
            if "drafted_by" in n and (not isinstance(n["drafted_by"], str) or not n["drafted_by"].strip()):
                errs.append(f"{p}: 'drafted_by' must name the person or AI that drafted it")
            if n.get("status") not in ("established", "open"):
                errs.append(f"{p}: 'status' must be established or open")
            if n.get("status") == "open" or "as_of" in n:
                try:
                    date = str(n.get("as_of", ""))
                    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
                        raise ValueError
                    datetime.date.fromisoformat(date)
                except ValueError:
                    errs.append(f"{p}: 'as_of' must be a real date in YYYY-MM-DD format")
            if not n.get("sources"):
                errs.append(f"{p}: add at least one source under 'sources:'")
            if not n["title"] or len(n["title"].split()) > 7:
                errs.append(f"{p}: title must contain 1 to 7 words")
            if not n["note"]:
                errs.append(f"{p}: add a short summary before Concepts")
            if not 2 <= len(n["concepts"]) <= 5:
                errs.append(f"{p}: needs 2 to 5 concepts (has {len(n['concepts'])})")
            for c in n["concepts"]:
                if "explainer" in c:
                    match = re.fullmatch(r"\.\./\.\./explainers/([a-z0-9]+(?:-[a-z0-9]+)*)/", c["explainer"])
                    if not match:
                        errs.append(f"{p}: explainer must be ../../explainers/lowercase-name/")
                    else:
                        target = root / "explainers" / match.group(1) / "index.html"
                        if not target.is_file() or not target.resolve().is_relative_to((root / "explainers").resolve()):
                            errs.append(f"{p}: explainer must point to an existing page inside explainers/")
    return errs
