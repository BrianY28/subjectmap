# Physics Map

An open mind map of physics, from Newton's Principia (1687) to the open research frontier, built from plain-text files so that anyone can correct, extend or review a single node through a pull request.

## View the map

- [Live interactive map](https://briany28.github.io/physics-map/): a zoomable mind map. Every node links to that node's Markdown file on GitHub, where anyone can propose an edit.
- [INDEX.md](INDEX.md): every branch and node with links, for browsing on GitHub.
- [map.opml](map.opml): import into MindNode, XMind or any OPML outliner.

## What's inside

The map holds 11 branches, 82 nodes and 326 concepts. The structure is map > branch > node > concept: a node is a topic such as "Newton's laws" or "Quantum gravity", and its concepts are the 2 to 5 key results, laws, experiments or open questions.

| Branch | Period | Nodes | Concepts |
| --- | --- | --- | --- |
| Newtonian mechanics | 1687-1830s | 6 | 24 |
| Electromagnetism and optics | 1785-1900 | 7 | 26 |
| Thermodynamics and statistical mechanics | 1824-1902 | 7 | 28 |
| Quantum mechanics and QFT | 1900-1970s | 8 | 32 |
| Relativity and gravitation | 1905-present | 7 | 27 |
| Nuclear and particle physics | 1896-2012 | 8 | 32 |
| Atomic, molecular, optical physics | 1814-present | 7 | 28 |
| Condensed matter physics | 1911-present | 8 | 32 |
| Astrophysics and cosmology | 1915-present | 8 | 32 |
| Fluids, plasmas and complex systems | 1822-present | 7 | 28 |
| Open frontier | today | 9 | 37 |

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. The issue forms are at [issues/new/choose](https://github.com/BrianY28/physics-map/issues/new/choose).

1. **Fix a node.** Open its file on GitHub (or click it in the live map), press the pencil icon, edit, and open a pull request. You can also open an issue with the "Node correction" form. See [Quick edits on GitHub](CONTRIBUTING.md#quick-edits-on-github).
2. **Check a node or improve its sources.** Every node already lists sources; checking a node against them, or adding a better primary source, is the most useful first contribution. Add yourself to `reviewed_by` when you have checked a node. See [Sources](CONTRIBUTING.md#sources) and [Reviewing a node](CONTRIBUTING.md#reviewing-a-node).
3. **Add a node.** Create a new file in the right branch folder, one node per pull request, or propose it with the "New node" form. See [Adding a node](CONTRIBUTING.md#adding-a-node).
4. **Update the frontier.** When a result changes the status of an open question, update the node, its sources and `as_of`. Use the "Frontier update" form. See [Frontier nodes](CONTRIBUTING.md#frontier-nodes).
5. **Write an explainer page.** One interactive page per concept, with simulations, history and sources. See [Explainer pages](CONTRIBUTING.md#explainer-pages).

## How this map was made

On 8 November 2026 the map was drafted by DeepSeek V4.1 Flash (through Ollama) and supervised by Claude (Anthropic's AI model). Claude designed the outline, checked every branch and sent DeepSeek about 40 factual corrections; for example, the four-equation vector form of Maxwell's equations is Heaviside's (1884), not Maxwell's; Carnot never wrote η = 1 − T_C/T_H; and several frontier results were out of date, such as the muon g-2 anomaly, which largely went away in 2025.

DeepSeek then drafted 224 citations. Claude checked every one, fixed a citation that blended two different dark-matter papers, a wrong author list and frontier entries that cited only old discoveries, and verified the recent papers against publisher records. The map now has 228 sources. The Newton's first law explainer was also written by DeepSeek and tested by Claude in a browser, with 18 fixes over three rounds. No physicist has reviewed the map yet, so every node currently lists only "Claude (AI)" under `reviewed_by`. Expert review is the most valuable contribution. The full record is in [`provenance/`](provenance/).

## Build it locally

You need Python 3.9 or newer and no other dependencies.

```bash
python3 tools/build.py
python3 tools/build.py --check
```

The first command checks every file and regenerates `INDEX.md`, `map.opml` and `site/`. The second checks every file and fails if `INDEX.md` or `map.opml` are out of date.

## License

Content in `nodes/`, `explainers/`, `INDEX.md` and `map.opml` is CC BY-SA 4.0, see [LICENSE-CONTENT.md](LICENSE-CONTENT.md). Code in `tools/` and `.github/` is MIT, see [LICENSE](LICENSE). By opening a pull request, you agree that your contribution is licensed the same way.
