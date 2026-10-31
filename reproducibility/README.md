# GFG Project 1A — Python and Excel calculation package

This public package contains the complete **76-check Python–Excel reconciliation** described in the portfolio. It includes the Python scripts, sanitized public-source inputs, the four-sheet Excel workbook, generated outputs and the detailed check results.

Prepared by [Muhammed Yousuf](https://muhammedyousufds.github.io/) · [LinkedIn](https://www.linkedin.com/in/muhammedyousuf111197/)

## Run it

Requirements: Python 3.10 or later. The scripts use Python's standard library and need no network access or third-party packages.

From this folder, run:

```text
python run_checks.py
```

The runner regenerates the analysis outputs and charts, then runs the Python–Excel reconciliation. A successful run reports **76 checks passed, zero failed**, and checks that the workbook contains **61 formulas with saved results and no formula errors**. The detailed comparison is written to `output/reconciliation_results.csv`; a readable report is written to `output/calculation_reconciliation.md`.

The checks compare the regenerated Python results with the workbook's saved formula results. They do not launch Excel or another spreadsheet application to recalculate the workbook. The script checks that formula results are present and error-free, then compares the defined overlapping values within the stated tolerances. You can inspect or recalculate the workbook separately in Excel or a compatible spreadsheet program.

## Analysis period and scope

The validated quantitative trend analysis covers **FY2024 and FY2025**. The broader portfolio project frame mentions FY2021–FY2025, but this package does not contain a validated FY2021–FY2023 trend series.

The calculations cover reported financial statement trends, gross margin, inventory composition and provision ratios, GFG-defined net working capital, Pro-Forma Cash, and illustrative comparisons with GFG's published ANZ impairment sensitivity thresholds. The workbook has four sheets: `Overview`, `Inputs`, `Working capital`, and `Inventory and ANZ`.

The ANZ scenario changes are synthetic illustrations; they are not GFG forecasts, do not combine interacting assumptions, do not reproduce management's impairment model, and do not calculate an impairment amount.

## Sources and input traceability

The inputs are selected figures transcribed from GFG's FY2025 Annual Report. Each input row includes its report locator and a direct source link. The supporting input tables also link directly to the relevant report pages:

- [FY2025 Annual Report — consolidated statements, notes and APM definitions](https://ir.global-fashion-group.com/media/document/4253e28d-9c76-4c94-8c4a-d67607b5e277/assets/LU2010095458-JA-2025-EQ-E-00.pdf?disposition=inline#page=47)
- [FY2025 results announcement](https://ir.global-fashion-group.com/news-detail/global-fashion-group-reports-q4-and-fy-2025-results/135deb4a-36c7-4082-ab84-2641184bda30)

## How to interpret a PASS

A `PASS` means a defined Python result agrees with the corresponding saved Excel result within the displayed tolerance (or matches the stated text flag). It confirms consistency between those calculation outputs; it does **not** validate GFG's underlying accounting records, estimate assumptions or internal controls. The checks are not audit evidence.

The €0.9m difference between the broader Note 16 restricted-cash/deposit-receivable population and the Pro-Forma Cash APM adjustment remains **unexplained and unallocated**. Q03 remains unresolved; no misstatement is inferred.

This is an educational public-source analysis, not a statutory audit. No company records were tested, none of the 45 proposed procedures was performed, and no audit opinion is expressed. The package does not include the full risk assessment, proposed-procedure register, approval records, freeze manifest or AI prompt/review logs.

## Attribution and licence

The MIT licence in `LICENSE` applies to original code only. GFG's report, company marks and source data remain subject to their respective rights. GFG does not sponsor or endorse this project.

