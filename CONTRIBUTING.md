# Contributing to Chemistry Map

Each topic is one Markdown file. Make a focused correction or addition, cite the evidence, and rebuild the map before opening a pull request.

## Content standards

- Use plain language for a student encountering the topic for the first time.
- State the assumptions behind an equation, including ideality, temperature, pressure or steady-state limits where relevant.
- Distinguish an equilibrium position from a reaction rate, a model from an observation, and an established result from an open research question.
- Use 2–5 concepts per topic and a short introduction. Four concepts is the initial edition's convention.
- Cite the source that supports the claim. Prefer original research, official standards and data, or an authoritative textbook for established fundamentals.

## File layout

Topics live at `nodes/NN-branch-name/topic-id.md`. The filename is a globally unique lowercase ID with hyphens. Each branch has a `README.md` with a `span` field, a title and a short summary.

```markdown
---
order: 10
when: "1860s-present"
status: established
sources:
  - "OpenStax (2019). Chemistry 2e, 13.2 Equilibrium Constants. https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants"
drafted_by: "your-name"
reviewed_by:
---

# Chemical equilibrium

Forward and reverse reactions continue at equal rates at equilibrium, so macroscopic composition remains constant in a closed system under fixed conditions.

## Concepts

- **Dynamic equilibrium**: Equal opposing rates do not require equal reactant and product concentrations.
- **Mass action**: The dimensionless activity quotient Q equals K at equilibrium at a specified temperature.
- **Reaction direction**: Comparing Q with K determines the thermodynamically favored direction under the stated constraints, not the reaction speed.
```

The front matter supports scalar `key: value` lines and lists using `  - item`. It is a deliberately small subset of YAML: use bare values or double quotes, not inline lists or multiline blocks.

| Field | Meaning |
| --- | --- |
| `order` | Nonnegative whole number, unique within the branch. Use steps of ten. |
| `when` | Historical context; a year or a broad period. Avoid unsupported priority claims. |
| `people` | Optional list of people relevant to a specific historical contribution. |
| `status` | `established` or `open`. Open denotes a research question or programme, not unsupported speculation. |
| `as_of` | Valid `YYYY-MM-DD` date required for open topics. Update it only after checking the current evidence. |
| `sources` | At least one full citation with a DOI or stable URL when available. |
| `drafted_by` | The person or AI system that drafted the text. |
| `reviewed_by` | Reviewers who actually checked the claims. Leave empty until reviewed. Mark AI reviewers with `(AI)`. |

Keep the topic title to seven words or fewer. Each concept line must have the form `- **Title**: One sentence.` An optional link to an explainer goes at the end: ` [Explainer](../../explainers/equilibrium/)`.

## Review and sources

Check the claims against the cited sources, including equations, historical context, scope and uncertainty. Add your name and relevant background under `reviewed_by` only after completing that check. An AI drafting pass does not count as human review.

For frontier topics, cite an actual result and explain what remains unresolved. A result demonstrated on one dataset, reaction family or apparatus does not establish general reliability. Older foundational work can remain useful, but check whether later work changes the question. The build warns when an open topic's review date is more than a year old.

Do not copy lengthy passages from sources. Write an original explanation and cite the work. Record AI assistance in `drafted_by` and state what you verified in the pull request.

## Interactive explainers

Create `explainers/NAME/index.html` as an HTML fragment: the build adds the document wrapper. Keep styles and scripts inline and avoid external dependencies. Follow the equilibrium example for keyboard-accessible controls, small-screen layouts, dark mode, sources and a link back to the topic.

State the model's assumptions and units. Check numerical limiting cases and conservation laws. A visually plausible animation is not evidence that its model is correct.

## Check and submit

```bash
python3 tools/build.py
python3 tools/build.py --check
python3 -m unittest discover -s tools -p 'test_*.py'
```

Commit your source edits and the regenerated `INDEX.md` and `map.opml`. The generated `site/` directory is ignored. GitHub checks pull requests and rebuilds the site after changes reach `main`.

When editing the equilibrium explainer, also run `node tools/test_equilibrium.cjs`. It exercises the actual script against known equilibrium, free-energy and relaxation results without installing a browser.

Use the **Node correction**, **New node** or **Frontier update** issue form if you prefer to describe a change. By contributing, you agree to the [content license](LICENSE-CONTENT.md) or [code license](LICENSE), as applicable.
