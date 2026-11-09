# SubjectMap

Open, sourced maps of physics and chemistry. Each subject has its own topic tree, interactive map and OPML export, with shared tools and a common contribution format.

A topic is one short Markdown file. Readers can follow its concepts, inspect its sources, and propose a correction through a pull request.

## Explore the subjects

| Subject | Branches | Topics | Concepts | Citation entries | Browse | Export |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| [Physics](subjects/physics/README.md) | 11 | 82 | 326 | 228 | [Index](subjects/physics/INDEX.md) | [OPML](subjects/physics/map.opml) |
| [Chemistry](subjects/chemistry/README.md) | 12 | 72 | 288 | 137 | [Index](subjects/chemistry/INDEX.md) | [OPML](subjects/chemistry/map.opml) |
| **Total** | **23** | **154** | **614** | **365** | [Subject index](INDEX.md) | |

Citation entries can refer to the same source. Branches organize each subject; dates provide historical context and do not establish sole discovery or priority.

The interactive site opens with a subject selector. Each subject has a zoomable map, a searchable topic index, readable topic pages with sources, and an explainer: Newton's first law for physics and chemical equilibrium for chemistry.

Browse the [interactive maps](https://briany28.github.io/subjectmap/) or the [source repository](https://github.com/BrianY28/subjectmap).

## Build and preview

Run these commands from the repository root. Python 3.9 or newer is the only build dependency.

```bash
python3 tools/build.py
python3 tools/build.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
python3 -m http.server 8000 --directory site --bind 127.0.0.1
```

Open **http://127.0.0.1:8000/** and choose a subject. Direct local routes are `/physics/` and `/chemistry/`. Stop the server with Ctrl+C.

The build validates both subjects and generates the root `INDEX.md`, each subject's `INDEX.md` and `map.opml`, and `site/`. Commit the generated Markdown indexes and OPML files with content changes; `site/` is rebuilt and remains ignored. The `--check` command validates all subjects and fails if any tracked generated output is stale.

For the equilibrium model's numerical checks, also run `node tools/test_equilibrium.cjs` with Node.js installed. These checks run in CI; Node.js is not needed to build or serve the site. The zoomable maps load a pinned Markmap release from a CDN. Topic browsing and local topic pages remain usable without it.

## Project layout

```text
subjects.json                Subject metadata and publication URLs
subjects/physics/            Physics nodes, explainer, provenance and exports
subjects/chemistry/          Chemistry nodes, explainer, provenance and exports
tools/                       Shared validator, builder, templates and tests
.github/                     Contribution forms and GitHub Actions workflows
site/                        Generated subject selector and subject sites
```

## Contribute and review

Read [CONTRIBUTING.md](CONTRIBUTING.md). Useful contributions include correcting a claim, improving a citation, reviewing one topic, or updating a frontier question against recent literature.

Both collections await human subject review. Imported physics topics retain their original DeepSeek drafting and Claude AI review records; chemistry topics retain their Codex drafting records and empty reviewer fields. Moving them into SubjectMap does not constitute a new scientific review. See the [physics provenance](subjects/physics/provenance/README.md) and [chemistry provenance](subjects/chemistry/provenance/README.md) for the creation records and checking limits.

## GitHub Pages

Push changes to `main` to run validation and publish the maps at **https://briany28.github.io/subjectmap/**. The **Publish maps** workflow checks both subjects and runs the tests before deploying.

For a fork, select **GitHub Actions** in **Settings → Pages**. Update `repository` and `site_url` in [subjects.json](subjects.json), update the issue-form links, rebuild, and run **Publish maps**.

## License and lineage

SubjectMap builds on [Physics Map](https://github.com/BrianY28/physics-map) at commit `361e305e8870a917193a0059af3aa1b1b665fef1`. It brings the existing physics collection and the newly drafted chemistry collection together as peer subjects.

Map content is [CC BY-SA 4.0](LICENSE-CONTENT.md). Shared build and site code is [MIT](LICENSE), with the original copyright notices retained. The imported physics explainer remains entirely CC BY-SA 4.0, including its embedded code; the chemistry explainer's JavaScript and CSS are MIT. See the license files for the exact scope and attribution requirements.
