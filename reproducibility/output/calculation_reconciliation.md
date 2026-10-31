# Python–Excel calculation reconciliation

Public package release: 31 October 2026. Checks: 76; passed: 76; failed: 0.
Workbook formulas: 61; formulas with missing cached values/errors: 0.

All amounts are €m unless stated. Numeric comparisons use absolute tolerance 0.00011 for €m/value outputs to allow workbook floating-point representation and CSV rounding; ratios and change rates use tighter tolerances. NWC and inventory tie-out cells are rounded to €0.01 in Excel. Python trends retain four decimal places for derived percentages; workbook display formats round visual percentages to one decimal place, while formulas retain full precision.

## Result detail

| Check | Python | Excel | Tolerance | Result |
|---|---:|---:|---:|---|
| Trend input FY2024 Revenue | 722.6 | 722.6 | 0.00011 | PASS |
| Trend input FY2025 Revenue | 679.8 | 679.8 | 0.00011 | PASS |
| Overview absolute change Revenue | -42.8 | -42.80000000000007 | 0.00011 | PASS |
| Overview percent change Revenue | -5.9231 | -5.923055632438423 | 0.0001 | PASS |
| Trend input FY2024 Gross profit | 324.4 | 324.4 | 0.00011 | PASS |
| Trend input FY2025 Gross profit | 315.5 | 315.5 | 0.00011 | PASS |
| Overview absolute change Gross profit | -8.9 | -8.899999999999977 | 0.00011 | PASS |
| Overview percent change Gross profit | -2.7435 | -2.743526510480876 | 0.0001 | PASS |
| Trend input FY2024 EBIT | -74.9 | -74.9 | 0.00011 | PASS |
| Trend input FY2025 EBIT | -40.0 | -40.0 | 0.00011 | PASS |
| Trend input FY2024 Adjusted EBITDA | -17.6 | -17.6 | 0.00011 | PASS |
| Trend input FY2025 Adjusted EBITDA | 9.3 | 9.3 | 0.00011 | PASS |
| Trend input FY2024 Net inventory | 96.4 | 96.4 | 0.00011 | PASS |
| Trend input FY2025 Net inventory | 81.9 | 81.9 | 0.00011 | PASS |
| Overview absolute change Net inventory | -14.5 | -14.5 | 0.00011 | PASS |
| Overview percent change Net inventory | -15.0415 | -15.041493775933612 | 0.0001 | PASS |
| Trend input FY2024 Current trade and other receivables | 48.8 | 48.8 | 0.00011 | PASS |
| Trend input FY2025 Current trade and other receivables | 21.1 | 21.1 | 0.00011 | PASS |
| Trend input FY2024 Cash and cash equivalents | 210.6 | 210.6 | 0.00011 | PASS |
| Trend input FY2025 Cash and cash equivalents | 176.5 | 176.5 | 0.00011 | PASS |
| Trend input FY2024 Total assets | 637.5 | 637.5 | 0.00011 | PASS |
| Trend input FY2025 Total assets | 530.3 | 530.3 | 0.00011 | PASS |
| Trend input FY2024 NMV | 1099.6 | 1099.6 | 0.00011 | PASS |
| Trend input FY2025 NMV | 1041.6 | 1041.6 | 0.00011 | PASS |
| Trend input FY2024 Net operating cash flow | -15.0 | -15.0 | 0.00011 | PASS |
| Trend input FY2025 Net operating cash flow | 7.5 | 7.5 | 0.00011 | PASS |
| Gross margin FY2024 | 0.448934 | 0.4489344035427622 | 1e-06 | PASS |
| Gross margin FY2025 | 0.464107 | 0.4641070903206826 | 1e-06 | PASS |
| NWC component FY2024 Inventory | 96.4 | 96.4 | 0.00011 | PASS |
| NWC component FY2025 Inventory | 81.9 | 81.9 | 0.00011 | PASS |
| NWC component FY2024 Current trade and other receivables | 48.8 | 48.8 | 0.00011 | PASS |
| NWC component FY2025 Current trade and other receivables | 21.1 | 21.1 | 0.00011 | PASS |
| NWC component FY2024 Less current trade payables and other financial liabilities | -204.0 | -204.0 | 0.00011 | PASS |
| NWC component FY2025 Less current trade payables and other financial liabilities | -224.7 | -224.7 | 0.00011 | PASS |
| NWC component FY2024 Add back current convertible bond liabilities | 2.7 | 2.7 | 0.00011 | PASS |
| NWC component FY2025 Add back current convertible bond liabilities | 40.4 | 40.4 | 0.00011 | PASS |
| NWC component FY2024 Add back share based payment liabilities | 1.3 | 1.3 | 0.00011 | PASS |
| NWC component FY2025 Add back share based payment liabilities | 1.0 | 1.0 | 0.00011 | PASS |
| Calculated GFG NWC FY2024_EURm | -54.8 | -54.80000000000001 | 0.00011 | PASS |
| NWC difference after workbook rounding FY2024_EURm | 0.0 | 0.0 | 0.00011 | PASS |
| Overview NWC movement FY2024_EURm | -54.8 | -54.80000000000001 | 0.00011 | PASS |
| Calculated GFG NWC FY2025_EURm | -80.29999999999998 | -80.29999999999998 | 0.00011 | PASS |
| NWC difference after workbook rounding FY2025_EURm | 0.0 | 0.0 | 0.00011 | PASS |
| Overview NWC movement FY2025_EURm | -80.3 | -80.29999999999998 | 0.00011 | PASS |
| Inventory Raw materials and supplies FY2024 | 0.5 | 0.5 | 0.00011 | PASS |
| Inventory Raw materials and supplies FY2025 | 0.7 | 0.7 | 0.00011 | PASS |
| Inventory Finished goods and merchandise FY2024 | 105.2 | 105.2 | 0.00011 | PASS |
| Inventory Finished goods and merchandise FY2025 | 88.3 | 88.3 | 0.00011 | PASS |
| Inventory Less: provision FY2024 | -9.3 | -9.3 | 0.00011 | PASS |
| Inventory Less: provision FY2025 | -7.1 | -7.1 | 0.00011 | PASS |
| Inventory Net inventories FY2024 | 96.4 | 96.4 | 0.00011 | PASS |
| Inventory Net inventories FY2025 | 81.9 | 81.9 | 0.00011 | PASS |
| Provision ratio FY2024 | 0.088403 | 0.08840304182509506 | 1e-06 | PASS |
| Provision ratio FY2025 | 0.08040800000000001 | 0.08040770101925254 | 1e-06 | PASS |
| Inventory reconciliation B | 0.0 | 0.0 | 0.00011 | PASS |
| Inventory reconciliation C | 0.0 | 0.0 | 0.00011 | PASS |
| Cash bridge IFRS cash and cash equivalents | 176.5 | 176.5 | 0.00011 | PASS |
| Cash bridge APM restricted cash and deposit receivables adjustment | 8.6 | 8.6 | 0.00011 | PASS |
| Cash bridge Investment funds in APM reconciliation | 0.0 | 0.0 | 0.00011 | PASS |
| Cash bridge Calculated Pro-Forma Cash | 185.1 | 185.1 | 0.00011 | PASS |
| Cash bridge Published Pro-Forma Cash | 185.1 | 185.1 | 0.00011 | PASS |
| Cash bridge Difference to published APM | 0.0 | 0.0 | 0.00011 | PASS |
| Cash bridge Note 16 restricted cash plus deposit receivables | 9.5 | 9.5 | 0.00011 | PASS |
| Cash bridge Unallocated Note 16 total less APM adjustment | 0.9 | 0.9 | 0.00011 | PASS |
| ANZ threshold Discount rates | 8.0 | 8.0 | 0.00011 | PASS |
| ANZ synthetic case Discount rates | 2.0 | 2.0 | 0.00011 | PASS |
| ANZ threshold flag Discount rates | No | No | exact | PASS |
| ANZ threshold EBITDA margin | -3.0 | -3.0 | 0.00011 | PASS |
| ANZ synthetic case EBITDA margin | -1.0 | -1.0 | 0.00011 | PASS |
| ANZ threshold flag EBITDA margin | No | No | exact | PASS |
| ANZ threshold Capital expenditure | 26.9 | 26.9 | 0.00011 | PASS |
| ANZ synthetic case Capital expenditure | 10.0 | 10.0 | 0.00011 | PASS |
| ANZ threshold flag Capital expenditure | No | No | exact | PASS |
| ANZ threshold 2028/2029 revenue growth rate | -3.3 | -3.3 | 0.00011 | PASS |
| ANZ synthetic case 2028/2029 revenue growth rate | -1.0 | -1.0 | 0.00011 | PASS |
| ANZ threshold flag 2028/2029 revenue growth rate | No | No | exact | PASS |

## Scope notes

The Python trend file includes ten metrics; the workbook Inputs sheet contains the same ten reported input values, while its Overview calculates and displays revenue, gross profit, gross margin and net inventory changes. GFG-defined NWC, inventory composition/provision ratio, Pro-Forma Cash bridge and the four illustrative ANZ comparisons were reconciled to formula outputs. The sensitivity comparison is a one-variable numeric threshold check, not an impairment-model reproduction.

The €0.9m Note 16/APM difference remains visible and unallocated. Q03 remains unresolved and unallocated. No accounting misstatement is inferred.

A PASS means the defined calculations agree within the stated precision. It does not validate management's underlying accounting records or constitute audit evidence.

