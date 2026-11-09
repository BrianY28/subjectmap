# Claude's review of DeepSeek's output

## Round 1: skeleton (DeepSeek original kept in skeleton.deepseek-original.json)
- Root renamed to "Physics: From Newton to the Frontier".
- Moved AMO physics after quantum mechanics (lasers and BEC depend on QM).
- Quantum: split matrix/wave mechanics; added entanglement and Bell's theorem.
- Relativity: added tests of GR (1919 eclipse onward); span now runs to the 2015 GW detection.
- Nuclear/particle: added neutron and neutrino; fission became "fission and fusion".
- Condensed matter: dropped Drude model; added semiconductors/transistor, high-Tc cuprates, topological and 2D materials; RG reframed as phase transitions.
- Astro/cosmology: added compact stars and black holes; dark energy merged with precision ΛCDM; span extended to present.
- Replaced "Nonlinear dynamics and complexity" (it held biophysics and fractal geometry) with "Fluids, plasmas and complex systems": fluid dynamics, turbulence and plasma physics were missing from the map.
- Frontier: split dark matter from dark energy/Hubble tension; added beyond-Standard-Model and strongly correlated matter; "AI-driven physics" renamed "Machine learning in physics".

## Round 2: branch content (DeepSeek drafts kept in branches.v1/; my feedback in feedback/)
Errors found and sent back to DeepSeek:
- Newtonian: tautochrone called a variational result (Huygens 1673, geometric); Clairaut wrongly credited; rigid-body date; wrong Lagrange-multiplier claim; Cavendish measured Earth's density, not G directly.
- EM: four-vector form of Maxwell's equations is Heaviside's (1884), not Maxwell's 1865 paper.
- Thermo: Carnot never wrote η = 1 − T_C/T_H (caloric theory; formula needs Kelvin's absolute scale).
- Quantum: "ultraviolet catastrophe" myth about Planck; ħ/2 form is Kennard's; positron discoverer missing; Bell tests and 2022 Nobel missing.
- Relativity: GW concepts stopped at 2015; event-horizon interpretation is 1958, not 1916.
- AMO: stopped at 1995 (added optical clocks, attosecond lasers, laser cooling).
- Astro: stars held up by gas pressure (not radiation); r-process omitted; COBE spectrum was 1990; pulsar discoverer Bell Burnell missing.
- Frontier: stale facts on muon g-2 (resolved 2025), KATRIN (0.45 eV), NIF (8.6 MJ, 2025), DESI (2.8–4.2σ), JUNO (June 2026), neutral-atom qubits, fusion people (executives, not physicists); added 2024/2025/2026 Nobel prizes.
- Automatic checks: 3 duplicate concepts across branches.

## Explainer: Newton's first law (explainers/first-law/)
Published: https://claude.ai/artifact/Aafqvp4cgXV2Kv3edftSeJ (private). Final file: newtons-first-law.html (= v4.html).
DeepSeek wrote every version from brief.md; Claude reviewed, browser-tested and sent the feedback-v*.txt files.
- Attempt 1 failed: DeepSeek spent its whole 32k-token budget drafting code inside its thinking (kept in failed/). Fix: 96k budget + "plan briefly, write code in the answer".
- v1 -> v2 (13 fixes): Motte 1729 wording (v1 used the 1934 Motte-Cajori text); Buridan "quantity of matter"; Voyager 1 wording; fictitious force −m·a_bus; uppercase labels turned μ into "M" and d = h / sin θ into "D = H / SIN Θ"; Plate III label overlap, 0.8 s event too fast (now ×0.25 slow motion), ball frozen while text said it moved (now hits the front wall); frame labels on readouts; clipped puck; t (s) axis label; plate spacing on phones.
- v2 -> v3: ball drawn half outside the bus at the end; passenger-view bus speed labelled "(ground)".
- v3 -> v4: bus frame is only non-inertial while braking; caption and end note corrected.
Verified in a browser at 1280px and 400px, light and dark: v(t) = 6 − μgt, d = h / sin θ, v = √(2gh) = 4.43 m/s, bus 4.0 → 0 at 5 m/s², no console errors, no horizontal overflow.
- Backlink: the MindNode node "First law: inertia" now links to the explainer (Node → Edit Link shows https://claude.ai/artifact/Aafqvp4cgXV2Kv3edftSeJ). Added in the MindNode app only; the OPML file in this folder does not carry it.

## Round 4: GitHub version (8 November 2026)
- Converted the 82 reviewed nodes from JSON to one Markdown file each (`nodes/`), by script; round trip checked exactly (titles, notes, 326 concepts, people).
- Sources: DeepSeek drafted 224 citations (13 marked medium confidence). Claude read every one. Fixes: an LZ dark-matter citation that carried XENONnT's journal reference (PRL 133, 191002) — replaced by the correct LZ (PRL 135, 011802) and XENONnT papers; the 2018 magic-angle paper had a wrong co-author (Demir for Fang); DESI DR2's first author is Abdul-Karim (not Adame); Navier's memoir year (published 1827, read 1822); frontier nodes that cited only old discoveries now cite the current results (muon g-2 final 2025, KATRIN 2025, JUNO 2026, DESI DR2, LZ 2025, XENONnT 2024, FQAH 2023-24, IceCube 2013). Recent papers checked against publisher records. Result: 228 sources.
- File-name fixes: amp-res-force-law -> amperes-force-law; dark-energy-and-cdm -> dark-energy-and-lambda-cdm. Branch spans updated (AMO, condensed matter, relativity).
- README, CONTRIBUTING, issue forms and PR template drafted by DeepSeek from briefs in `briefs/`; one fix round for README/CONTRIBUTING (provenance paragraph, sources wording, DOI rule, code-block languages). Issue forms validated as YAML.
- Newton's first law page shortened by DeepSeek (v5): 1,625 -> 933 words including plate labels; history collapsed; misconceptions folded into the plates; simulation script byte-identical to reviewed v4; MindNode links replaced by the public map and GitHub links. All three simulations re-tested.
- Build tooling (tools/build.py, nodelib.py) and workflows written by Claude. Site tested in a browser: 82 topics link to their files; dark-mode text colour bug found and fixed.
