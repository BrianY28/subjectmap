# Content license and attribution

SubjectMap's map content is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

Full legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode

This covers the Markdown topic files and branch descriptions in `subjects/*/nodes/`, educational explainer content, Markdown documentation and provenance, the generated indexes and OPML maps, and the corresponding content in the generated site.

## Attribution by subject

- **Physics:** Credit **Physics Map contributors** and link to [the original Physics Map](https://github.com/BrianY28/physics-map). SubjectMap imported the collection at commit `361e305e8870a917193a0059af3aa1b1b665fef1`. The migration changes its location, navigation and generated presentation; original topic authorship and review records are preserved. See [physics provenance](subjects/physics/provenance/README.md).
- **Chemistry:** Credit **Chemistry Map contributors** and identify this SubjectMap collection. Chemistry topic content and its equilibrium explainer were newly drafted for the chemistry project before it became a subject here. See [chemistry provenance](subjects/chemistry/provenance/README.md).
- **Shared documentation and subsequent contributions:** Credit **SubjectMap contributors** and link to the project at `https://github.com/BrianY28/subjectmap`.

When sharing or adapting the content, retain the applicable attribution, indicate your changes, and distribute adaptations under the same license. A citation does not relicense the referenced publication or its assets. Historical material that is in the public domain remains in the public domain.

## Code boundaries

The entire imported physics explainer at `subjects/physics/explainers/first-law/index.html` remains **CC BY-SA 4.0**, including its embedded JavaScript and CSS. This also applies to its generated copy. The original Physics Map content license covered everything in its `explainers/` directory; the migration does not change that license.

Code in `tools/`, `.github/`, the generated site's shared interface, and JavaScript/CSS in `subjects/chemistry/explainers/` is covered by the [MIT license](LICENSE). Educational prose in the chemistry explainer remains CC BY-SA 4.0. Third-party libraries retain their own licenses.
