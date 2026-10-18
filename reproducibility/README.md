# GFG public calculation sample

This small package reproduces 15 selected calculations shown in the portfolio. It uses a limited set of public-source figures and Python 3's standard library; it contains no private workpapers, raw company records, Excel workbook, full risk register, KAM source material or approval records.

## Run

From the website repository root:

```text
python reproducibility/run_checks.py
```

The script reads `inputs.csv` and writes `results.csv` in this folder. It runs without third-party packages. A clean run reports 15 checks passed and zero failed. Outputs are rounded to four decimal places and compared with the listed reference value within an absolute tolerance of €0.00015m or 0.00015 percentage points, as applicable.

## Scope and interpretation

The checks cover reported-euro revenue movement, calculated gross margins, inventory tie-outs and movements, inventory-provision ratios, GFG-defined net working capital, the Pro-Forma Cash arithmetic and the unresolved Q03 difference. Input rows include their annual-report page or note locator and a direct link to the source disclosure. For the FY2024 NWC inventory input, the calculation uses the €96.4m statement/Note 15 amount to reproduce reported NWC; the KPI table’s €96.3m display difference remains disclosed as Q02.

“PASS” means the formula in this script reproduces the documented reference result from the included inputs at the stated rounding/tolerance. It does not validate GFG's accounting records, estimate assumptions or internal controls, and it is not audit evidence. GFG-defined net working capital and Pro-Forma Cash are alternative performance measures (APMs), not IFRS line items. Q03 remains an unexplained €0.9m difference between the Note 16 population and APM adjustment; it is not allocated and is not described as a misstatement.

The project separately completed 76 Python–Excel checks internally. This sample does not recreate that private test suite or workbook. No GFG records were tested, none of the 45 proposed audit procedures was performed, and no audit opinion is expressed.

## Source

Global Fashion Group S.A., FY2025 Annual Report, principally the consolidated profit-or-loss statement (printed p.47), consolidated statement of financial position (p.48), inventory Note 15 (p.83), cash Note 16 (p.84), and APM definitions (p.129): [official report PDF](https://ir.global-fashion-group.com/media/document/4253e28d-9c76-4c94-8c4a-d67607b5e277/assets/LU2010095458-JA-2025-EQ-E-00.pdf?disposition=inline).

Company-reported facts and data remain attributable to GFG. This package does not grant rights to the source report, company marks or third-party materials.
