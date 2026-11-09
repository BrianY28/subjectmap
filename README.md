# Chemistry Map

An open map of chemistry, from atoms and bonding to the research frontier. Each topic lives in a small, sourced Markdown file that can be corrected or extended through a pull request.

This is a chemistry counterpart to [Physics Map](https://github.com/BrianY28/physics-map), with the same plain-text approach, Python build, OPML export and GitHub Pages workflow.

## Explore

- [INDEX.md](INDEX.md): browse all topics and their concepts on GitHub.
- [map.opml](map.opml): import the map into MindNode, XMind or another OPML outliner.
- Interactive site: build locally using the commands below. The map supports zooming and topic browsing; each topic opens a readable page with sources.
- [Chemical equilibrium explainer](explainers/equilibrium/index.html): an interactive model of a reversible reaction, included in the generated site.

This checkout has not been published. The GitHub links in the generated site target the intended repository, `BrianY28/chemistry-map`; they become available after that repository is created and populated.

## Scope

The initial edition contains **12 branches, 72 topics and 288 concepts**. Branches form a learning path rather than a single historical timeline. Topic dates provide broad historical context, not claims of sole discovery or priority.

| Branch | Topics |
| --- | ---: |
| Foundations and atoms | 6 |
| Bonding and molecular structure | 6 |
| Thermodynamics and equilibrium | 6 |
| Kinetics and catalysis | 6 |
| Inorganic chemistry | 6 |
| Organic chemistry | 6 |
| Analytical chemistry | 6 |
| Electrochemistry and interfaces | 6 |
| Biochemistry and chemical biology | 6 |
| Polymers and materials | 6 |
| Environmental and green chemistry | 6 |
| Open frontier | 6 |

Start with foundations, bonding and thermodynamics. Then follow a branch of interest. The frontier distinguishes demonstrated methods from remaining questions about reliability, scope, sustainability and scale.

## Build and preview

Python 3.9 or newer is the only build dependency.

```bash
python3 tools/build.py
python3 tools/build.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
python3 -m http.server 8000 --directory site --bind 127.0.0.1
```

Open **http://127.0.0.1:8000/**. Stop the server with Ctrl+C.

For the optional numerical checks of the explainer, run `node tools/test_equilibrium.cjs` with Node.js installed. These checks also run in CI; Node.js is not needed to build or serve the site.

The build validates the node files and generates `INDEX.md`, `map.opml` and `site/`. Commit the first two generated files with content changes. The site is rebuilt by GitHub Actions. The zoomable map loads a pinned Markmap release from a CDN; the topic index, topic pages and equilibrium explainer also work without that dependency.

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Useful contributions include correcting one claim, improving a citation, reviewing one topic, adding a missing concept, or updating a frontier topic against recent literature. Issue forms and a pull request template are included.

All initial topics are **AI-assisted drafts awaiting human subject review**. A source link is a starting point for verification, not a claim that a chemistry expert has checked the text. See [provenance/README.md](provenance/README.md) for the creation record and source-check limits.

## Publish on GitHub Pages

1. Create an empty repository named `chemistry-map` in the intended GitHub account and push this checkout to its `main` branch.
2. In the repository's **Settings → Pages**, select **GitHub Actions** as the publishing source.
3. Run the **Publish map** workflow, or push a change to `main`.

The expected Pages address is `https://briany28.github.io/chemistry-map/` once deployment succeeds. If you use a different account or repository name, update `REPO` and `SITE_URL` in `tools/build.py` and the links in the issue forms, then rebuild.

## License and attribution

Content is [CC BY-SA 4.0](LICENSE-CONTENT.md). Build and site code is [MIT](LICENSE). The build tools and GitHub workflow are adapted from Physics Map at commit `361e305e8870a917193a0059af3aa1b1b665fef1`; the original copyright notice is retained. Chemistry topic content and the equilibrium explainer were newly drafted for this project.
