# Creation record

Chemistry Map was drafted on 10 November 2026 with Codex (AI). Parallel drafting tasks covered foundations and core chemistry (branches 01–06), applied chemistry and research questions (07–12), and the static-site generator. No human chemistry review has been completed. Empty `reviewed_by` fields preserve that distinction.

The starting build tools and GitHub workflow came from the local checkout of [BrianY28/physics-map](https://github.com/BrianY28/physics-map), verified against remote HEAD `361e305e8870a917193a0059af3aa1b1b665fef1`. The original physics topics, explainer, AI logs and review claims were not carried over.

The chemistry outline contains 12 branches with six topics each. It is a broad learning map, not a comprehensive syllabus. Historical periods are orientation aids; they do not settle priority disputes. Sources appear in each node, while the accompanying source notes describe the checks and access limits during drafting.

The equilibrium explainer uses a closed, ideal A ⇌ B model at 298.15 K, with fixed total concentration. Its calculations use Q = x_B/(1 − x_B), x_B,eq = K/(1 + K), and ΔᵣG = RT ln(Q/K). The display kinetics use k_forward = K/(1 + K) and k_reverse = 1/(1 + K) in arbitrary inverse time units. Thus k_forward/k_reverse = K and their sum is one; this fixes the illustrative relaxation timescale rather than predicting an experimental rate.

Equilibrium and free-energy source pages inspected during development:

- [OpenStax Chemistry 2e, 13.2 Equilibrium Constants](https://openstax.org/books/chemistry-2e/pages/13-2-equilibrium-constants).
- [OpenStax Chemistry 2e, 16.4 Free Energy](https://openstax.org/books/chemistry-2e/pages/16-4-free-energy).
- [IUPAC Gold Book, chemical equilibrium](https://goldbook.iupac.org/terms/view/C01023) was requested but returned an access error during the explainer check; the accessible textbook chapters supported the model independently.

Software validation checks structure, generated links and numerical behavior. It does not establish that every scientific claim or citation has received expert review. Human review of the initial content remains the most valuable next contribution.

## Initial validation

- The final build contains 12 branches, 72 topics, 288 concepts and 137 citation entries (entries can cite the same source).
- Nine Python regression tests pass for parsing, validation, escaped output, deterministic generation, local links and OPML.
- The actual equilibrium JavaScript passes numerical checks for nine starting mixtures, reaction Gibbs energy, conservation, relaxation, reset and reduced motion.
- An additional check of the complete generated site found no broken targets among 586 local links across 74 HTML pages. The OPML parses with the expected hierarchy.
- A local Safari preview loaded and rendered the Markmap during integration. Full visual and narrow-screen browser QA was not completed: the browser automation host was unavailable, and native UI checks conflicted with concurrent browser use.

An independent AI spot-check of branches 07–12 found and corrected wording about atom economy and conventional batteries. It also checked recent frontier reference identities. This is not human expert review, and no human-review credit was added.
