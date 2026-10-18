# AI-Assisted Audit & Finance Analytics Portfolio

**Website:** [muhammedyousufds.github.io](https://muhammedyousufds.github.io/)

This portfolio demonstrates how public financial disclosures can be analysed with accounting judgement, audit-oriented risk thinking, Python, Excel and carefully checked AI assistance. It is intended for finance, accounting and audit recruitment conversations, including junior audit and assurance roles. All company case work is an educational simulation.

## Featured case study: Global Fashion Group S.A.

Project 1A examines GFG’s published FY2025 annual report and FY2025 results announcement. It uses a FY2021–FY2025 project frame, while the validated numerical trend pilot is limited to FY2024–FY2025. It presents reported IFRS amounts separately from calculated metrics and GFG-defined alternative performance measures (APMs).

The public case study summarises nine potential financial-statement risk categories, their relevant assertions and 45 proposed responses. These are risk hypotheses and possible procedures. No GFG accounting records were accessed, no procedure was performed, no audit evidence was obtained and no audit opinion is expressed.

## Audit and analytical method

The analysis starts with source-linked reported facts and their period, unit and reporting perimeter. Calculations are kept separate from company-reported figures; neutral observations are kept separate from hypotheses and potential risks. Proposed procedures are clearly labelled and are not represented as executed. Public aggregate disclosures cannot establish transaction-level accuracy, item-level inventory NRV, control operation, estimate adequacy or the cause of a balance movement.

Key observations include reported-euro revenue of €679.8m in FY2025 versus €722.6m in FY2024 (a calculated 5.92% decline), gross margin of 46.41% versus 44.89%, and net inventory of €81.9m versus €96.4m. These are not findings of misstatement. The €0.9m difference between Note 16’s broader restricted-cash/deposit-receivables total and the Pro-Forma Cash APM adjustment remains unexplained and unallocated; it is not characterised as a misstatement.

## Technology and reproducibility

The project used Python for financial calculations and chart preparation, Excel formulas for a parallel analytical workbook, and AI assistance for organising public disclosures and drafting selected observations. The public website uses HTML, CSS, JavaScript and accessible SVG charts.

Run the limited public calculation sample from the repository root:

```text
python reproducibility/run_checks.py
```

It uses Python 3’s standard library, reads the included source-linked `inputs.csv`, writes `results.csv`, and reproduces 15 selected calculations. A clean run reports 15 passed and zero failed. Each check includes its formula, result, reference value, tolerance and source locator. The inputs are selected public-source figures, not company records.

Separately, the internal project workflow completed 76 Python–Excel cross-checks, including a workbook with 61 saved formulas. The full workbook, input set and detailed reconciliation log are not public; those 76 checks are not independently rerunnable from this repository. The 15 public checks are a newly scoped sample, not a claim that the full internal suite has been published.

## Responsible AI and human review

AI assisted with selected public-disclosure organisation and drafting. Python and Excel handled the defined calculations. Material statements were traced to the cited annual report and calculations were reperformed. Human judgement determined whether an observation supported a hypothesis, how to word the limits and when an explanation could not be supported.

The review record shows an important provenance distinction: the original AI draft did not quantify the inventory-provision ratio movement. An intermediate human review draft stated 0.84 percentage points; recalculation gave 0.7995 percentage points, rounded to 0.80. The 0.84 figure was a human drafting error, not an AI suggestion. A broad supplier-finance/NWC inference was also narrowed because public disclosures did not map supplier-finance balances to the NWC payable component. AI output is not self-validating and can omit context, make arithmetic errors or suggest unsupported explanations.

## KAM firewall

The independent risk assessment was frozen before the separate Stage 9 comparison with EY’s published FY2025 Key Audit Matters. The comparison is a thematic learning exercise only. It does not rewrite the independent assessment, imply EY endorsement or provide independent validation, and it does not evaluate audit quality. The frozen risk assessment, detailed assertion/procedure registers and private approval records remain outside this public repository.

## Evidence limits

- Project frame: FY2021–FY2025; validated numerical trend series: FY2024–FY2025.
- Q02: the FY2024 KPI definition table displays inventory of €96.3m while the statement and Note 15 show €96.4m; this €0.1m display difference remains documented.
- Q03: the €0.9m Note 16/APM cash difference remains unexplained and unallocated.
- Synthetic sensitivity scenarios are illustrations, not GFG forecasts or an impairment calculation.
- No executed audit procedures, tested company records, control conclusions or audit opinion.
- GFG reporting, source data and auditor KAM content remain attributable to their original publishers; their inclusion does not imply endorsement.

## Repository structure

```text
index.html                  Portfolio homepage and professional profile
case-study.html             GFG analysis, charts and selected report links
methodology.html            Audit methodology, AI review and KAM firewall
evidence.html               Public evidence and reproducibility status
styles.css, site.js         Responsive visual system and accessible navigation
assets/                     Responsive chart SVGs
downloads/                  Author-reviewed selected portfolio reports
reproducibility/            Limited public inputs, Python script, run guide, results
```

The separate technical research repository and private working papers are not linked or included.
