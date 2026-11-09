# Physics Map

Physics from Newton's mechanics to the open research frontier, as one subject within [SubjectMap](../../README.md).

**11 branches · 82 topics · 326 concepts · 228 citation entries**

- [Browse the index](INDEX.md).
- [Download the OPML map](map.opml) for MindNode, XMind or another outliner.
- [Newton's first law explainer source](explainers/first-law/index.html).
- [Creation record and upstream attribution](provenance/README.md).

The branches cover mechanics, electromagnetism and optics, thermodynamics, quantum theory, relativity, particles, atomic and molecular physics, condensed matter, astrophysics, fluids and complex systems, and open questions.

## Local preview

Run these commands from the **SubjectMap repository root**, not this subject folder:

```bash
python3 tools/build.py
python3 -m http.server 8000 --directory site --bind 127.0.0.1
```

Open **http://127.0.0.1:8000/physics/**. The site links each topic to its explanation and sources. The intended hosted route is `/subjectmap/physics/` after publication.

## Review and contributions

The topics were imported from [Physics Map](https://github.com/BrianY28/physics-map) at commit `361e305e8870a917193a0059af3aa1b1b665fef1`. Original drafting, AI review and frontier dates are preserved. No human subject review or new scientific review is implied by this migration.

Follow the shared [contribution guide](../../CONTRIBUTING.md). Edit files under `subjects/physics/nodes/`, then rebuild from the repository root. Content, including the entire imported explainer, remains [CC BY-SA 4.0](../../LICENSE-CONTENT.md) with credit to Physics Map contributors.
