"""Reproduce 15 selected public-source calculations for the GFG case study.

Python 3 standard library only. Inputs are limited, sanitized figures transcribed
from GFG's FY2025 Annual Report; formulas and source locators are documented in
README.md and inputs.csv. This is not the private 76-check Python–Excel suite.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs.csv"
OUTPUT = ROOT / "results.csv"
TOLERANCE = 0.00015


def read_inputs() -> dict[str, dict[str, str]]:
    with INPUTS.open(encoding="utf-8-sig", newline="") as handle:
        return {row["key"]: row for row in csv.DictReader(handle)}


def value(data: dict[str, dict[str, str]], key: str, period: str) -> float:
    cell = data[key][period]
    if not cell:
        raise ValueError(f"Missing {period} input for {key}")
    return float(cell)


def main() -> None:
    d = read_inputs()
    rev24, rev25 = value(d, "revenue", "FY2024_EURm"), value(d, "revenue", "FY2025_EURm")
    gp24, gp25 = value(d, "gross_profit", "FY2024_EURm"), value(d, "gross_profit", "FY2025_EURm")
    inv24, inv25 = value(d, "net_inventory_reported", "FY2024_EURm"), value(d, "net_inventory_reported", "FY2025_EURm")
    finished24, finished25 = value(d, "inventory_finished", "FY2024_EURm"), value(d, "inventory_finished", "FY2025_EURm")
    prov24, prov25 = value(d, "inventory_provision", "FY2024_EURm"), value(d, "inventory_provision", "FY2025_EURm")
    margin24, margin25 = 100 * gp24 / rev24, 100 * gp25 / rev25
    ratio24, ratio25 = 100 * abs(prov24) / finished24, 100 * abs(prov25) / finished25
    inventory_calc24 = sum(value(d, key, "FY2024_EURm") for key in ("inventory_raw", "inventory_finished", "inventory_provision"))
    inventory_calc25 = sum(value(d, key, "FY2025_EURm") for key in ("inventory_raw", "inventory_finished", "inventory_provision"))

    def nwc(period: str) -> float:
        return sum(value(d, key, period) for key in ("nwc_inventory", "nwc_receivables", "nwc_payables", "nwc_convertible", "nwc_share_based"))

    cash_calc = sum(value(d, key, "FY2025_EURm") for key in ("ifrs_cash", "apm_cash_adjustment", "investment_funds"))
    cash_reported = value(d, "proforma_cash_reported", "FY2025_EURm")
    note16_total = value(d, "note16_restricted_cash", "FY2025_EURm") + value(d, "note16_deposit_receivables", "FY2025_EURm")
    apm_adjustment = value(d, "apm_cash_adjustment", "FY2025_EURm")

    rows = [
        ("C01", "Revenue change", "FY2025 minus FY2024 (€m)", rev25 - rev24, -42.8, "Revenue; Annual Report p.47", "Calculated from reported IFRS values."),
        ("C02", "Revenue percentage change", "(FY2025 / FY2024 − 1) × 100", 100 * (rev25 / rev24 - 1), -5.9231, "Revenue; Annual Report p.47", "Reported-euro movement; distinct from constant-currency APM."),
        ("C03", "Gross margin FY2024", "Gross profit / revenue × 100", margin24, 44.8934, "Gross profit and revenue; Annual Report p.47", "Calculated percentage."),
        ("C04", "Gross margin FY2025", "Gross profit / revenue × 100", margin25, 46.4107, "Gross profit and revenue; Annual Report p.47", "Calculated percentage."),
        ("C05", "Gross margin movement", "FY2025 margin − FY2024 margin (percentage points)", margin25 - margin24, 1.5173, "Gross profit and revenue; Annual Report p.47", "Calculated percentage-point movement."),
        ("C06", "Inventory tie-out FY2024", "Raw materials + finished goods + provision − reported net inventory (€m)", inventory_calc24 - inv24, 0.0, "Note 15 p.83; statement p.48", "Zero difference at reported €0.1m precision."),
        ("C07", "Inventory tie-out FY2025", "Raw materials + finished goods + provision − reported net inventory (€m)", inventory_calc25 - inv25, 0.0, "Note 15 p.83; statement p.48", "Zero difference at reported €0.1m precision."),
        ("C08", "Net inventory percentage change", "(FY2025 / FY2024 − 1) × 100", 100 * (inv25 / inv24 - 1), -15.0415, "Net inventories; Annual Report pp.48, 83", "Calculated percentage change."),
        ("C09", "Provision / finished goods FY2024", "Absolute provision / finished goods × 100", ratio24, 8.8403, "Note 15 p.83", "Denominator follows the documented calculation basis."),
        ("C10", "Provision / finished goods FY2025", "Absolute provision / finished goods × 100", ratio25, 8.0408, "Note 15 p.83", "Denominator follows the documented calculation basis."),
        ("C11", "Provision ratio movement", "FY2025 ratio − FY2024 ratio (percentage points)", ratio25 - ratio24, -0.7995, "Note 15 p.83", "Rounds to −0.80 percentage points; does not assess adequacy."),
        ("C12", "GFG-defined NWC FY2024", "Sum of five disclosed APM components (€m)", nwc("FY2024_EURm"), -54.8, "APM definition p.129", "GFG APM, not conventional current assets less current liabilities."),
        ("C13", "GFG-defined NWC FY2025", "Sum of five disclosed APM components (€m)", nwc("FY2025_EURm"), -80.3, "APM definition p.129", "GFG APM, not conventional current assets less current liabilities."),
        ("C14", "Pro-Forma Cash bridge difference", "IFRS cash + APM adjustment + investment funds − reported Pro-Forma Cash (€m)", cash_calc - cash_reported, 0.0, "APM definition p.129", "Published APM arithmetic reproduces; APM is not an IFRS line item."),
        ("C15", "Q03 Note 16/APM difference", "Restricted cash + deposit receivables − APM cash adjustment (€m)", note16_total - apm_adjustment, 0.9, "Note 16 p.84; APM definition p.129", "Unexplained and unallocated public-source difference; no misstatement is inferred."),
    ]

    output_rows = []
    failed = []
    for check_id, label, formula, result, expected, source, note in rows:
        result_rounded = round(result, 4)
        if result_rounded == 0:
            result_rounded = 0.0  # avoid displaying a rounded negative zero
        expected_rounded = round(expected, 4)
        passed = math.isclose(result_rounded, expected_rounded, rel_tol=0.0, abs_tol=TOLERANCE)
        output_rows.append({"check_id": check_id, "calculation": label, "formula": formula,
                            "result": f"{result_rounded:.4f}", "reference_value": f"{expected_rounded:.4f}",
                            "tolerance": f"{TOLERANCE:.5f}", "status": "PASS" if passed else "FAIL",
                            "source_locator": source, "interpretation": note})
        if not passed:
            failed.append(check_id)

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Public checks: {len(rows)}; passed: {len(rows) - len(failed)}; failed: {len(failed)}")
    print(f"Output: {OUTPUT.name}")
    if failed:
        raise SystemExit("Failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
