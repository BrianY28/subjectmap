# Source checks: branches 07–12

Drafted with Codex (AI), 10 November 2026. The six branches contain 36 topics and 144 concepts. All `reviewed_by` lists remain empty: this record describes a drafting and source-selection pass, not human subject review or a complete audit of every cited work.

## Established topics

The initial explanations use established chemistry principles and original wording. Sources were selected for their connection to the actual topic; source availability and claim verification are distinct.

- **Analytical methods:** inspected the NIST Technical Note 1297 record and its 1994-edition contents, OpenStax's NMR, mass-spectrometry and spectroscopy chapter records, and David Harvey's own curriculum page linking *Analytical Chemistry 2.1*. Harvey's older DePauw host was inaccessible through the web tool, so citations use his current book page, which confirms the 2016 edition and links its formats; this is not a claim that every relevant chapter was opened. NIST's older publication listing labels the original 1993 issue, while the linked PDF and current contents identify the revised 1994 edition used here.
- **Electrochemistry:** inspected OpenStax's electrode-potential chapter. Nodes explicitly distinguish formal oxidation states from atomic charge, reversible potential from operating losses, Faradaic efficiency from energy efficiency, and standard-state activities from nominal concentrations. Other OpenStax chapter links identify the intended textbook sections; this pass did not independently audit every paragraph of those chapters.
- **Biochemistry:** inspected the OpenStax protein and enzyme chapters, the primary AlphaFold 3 paper and its limitations section, and the publication record for *The promise and peril of chemical probes*. The initial wording avoids treating all proteins as rigid, all enzymes as Michaelis–Menten systems, or bond breaking alone as the source of ATP hydrolysis free energy.
- **Materials:** inspected OpenStax's chain-growth, step-growth and polymer-summary records and its crystal-lattice chapter, the publisher record for Israelachvili's *Intermolecular and Surface Forces*, and official Nobel lecture/background records for supramolecular chemistry and quantum dots. MOFs are treated as established materials. The 2025 Nobel background PDF returned an access error and is not used as the sole support for a claim.
- **Environmental chemistry:** inspected the EPA ozone page, USGS pH and alkalinity resources, EPA/ATSDR fate-and-transport records, ACS's green-chemistry principles and the IEA ammonia roadmap overview. No current quantitative climate, regulatory or health thresholds are asserted. Some introductory source pages simplify pH and standard states; the nodes retain the more general chemistry definitions rather than repeating those simplifications.

Classic papers and books are included as historical or deeper references where appropriate. Their complete texts and all ISBNs were not comprehensively audited in this drafting pass. Dates in the nodes are broad context, not individually verified discovery-priority claims.

## Frontier check

The `as_of: 2026-11-10` dates record this focused source check. They do not mean an exhaustive literature review through that date. The final concept in each frontier node states an open research question; it is a synthesis of the preceding evidence rather than a quotation or a claim that the field has one agreed roadmap.

| Topic | Evidence inspected | Limits retained in the node |
| --- | --- | --- |
| Predictive synthesis | Maziarz et al., [RetroChimera, 2026](https://doi.org/10.1038/s41586-026-11160-9): publisher abstract, author list, date and citation. The publisher labels it an accepted early article; subscription content beyond the abstract was not accessed. | Distribution-shift and chemist-preference results are bounded demonstrations, not universal route reliability. |
| Autonomous laboratories | Dai et al., [2024](https://doi.org/10.1038/s41586-024-08173-7): abstract and main text, including the unexpected-product example requiring human inspection; Burger et al., [2020](https://doi.org/10.1038/s41586-020-2442-2): publisher search record and abstract summary. | Chemistry scope, measurement validity, failure detection and transfer between laboratories remain explicit limits. |
| Molecular design with AI | Abramson et al., [AlphaFold 3, 2024](https://doi.org/10.1038/s41586-024-07487-w): article and limitations; Lv et al., [2026](https://doi.org/10.1038/s41467-026-74666-w): article, citation and discussion of design-space limitations. | Structure prediction, binding affinity, biological activity and reliable novelty are distinct targets. |
| Sustainable chemical energy | Zhong et al., [2025](https://doi.org/10.1016/j.cej.2025.161119): publisher abstract and metadata; [IEA ammonia roadmap](https://www.iea.org/reports/ammonia-technology-roadmap): overview and scope. | A device demonstration is distinct from a favorable full-process energy, durability and material balance; no universal efficiency or deployment claim is made. |
| Circular polymers | Norton-Baker et al., [2026](https://doi.org/10.1038/s41467-026-78471-3): publisher article, authors and discussion of process-relevant testing; Tournier et al., [2020](https://doi.org/10.1038/s41586-020-2149-4): established primary reference for PET depolymerization. | PET assays do not establish recycling of all polymers; the 2026 paper itself calls for high-solids, high-conversion, pH-controlled evaluation. |
| Origins of chemical life | Patel et al., [2015](https://doi.org/10.1038/nchem.2202): indexed primary-paper record and public PMC abstract; Singh et al., [2025](https://doi.org/10.1038/s41586-025-09388-y): publisher article, author list and abstract. | Plausible component reactions do not reconstruct the full historical origin of a self-maintaining, evolving system. |

Several bare Nature URLs initially returned cookie-redirect errors; public article pages subsequently opened using the publisher's indexed `?error=cookies_not_supported` URLs. Stable DOI links are retained in nodes. No access credentials were used, and subscription-only full text was not represented as read.

## Remaining review work

A chemist should check each node's wording, source coverage and historical context. Useful next improvements include section-level references for the broader books, validation of every external link, more direct experimental references for instrument methods, and an independent current-literature review of the frontier. The structural validator confirms six nodes per branch and four concepts per node; it cannot certify scientific accuracy.
