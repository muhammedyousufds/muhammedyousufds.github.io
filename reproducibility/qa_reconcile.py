"""Reconcile the Python CSV outputs with the saved Excel workbook using stdlib only."""
from pathlib import Path
import csv
import re
import math
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
OUT = ROOT / "output"
XLSX = ROOT / "excel" / "GFG_Project1A_analytics_demo_v0.1.xlsx"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}

def rows(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def close(label, left, right, tol=0.00011):
    left, right = float(left), float(right)
    ok = math.isclose(left, right, rel_tol=0, abs_tol=tol)
    checks.append((label, left, right, tol, ok))

with zipfile.ZipFile(XLSX) as z:
    workbook = ET.fromstring(z.read("xl/workbook.xml"))
    names = [s.attrib["name"] for s in workbook.findall(".//m:sheet", NS)]
    assert names == ["Overview", "Inputs", "Working capital", "Inventory and ANZ"], names
    shared_root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    shared = ["".join(t.text or "" for t in si.findall(".//m:t", NS))
              for si in shared_root.findall("m:si", NS)]
    sheets = {}
    formulas = []
    errors = []
    for i, name in enumerate(names, 1):
        root = ET.fromstring(z.read(f"xl/worksheets/sheet{i}.xml"))
        cells = {}
        for c in root.findall(".//m:c", NS):
            ref = c.attrib.get("r")
            v = c.find("m:v", NS)
            f = c.find("m:f", NS)
            value = v.text if v is not None else None
            if c.attrib.get("t") == "s" and value is not None:
                value = shared[int(value)]
            cells[ref] = value
            if f is not None:
                formulas.append((name, ref, f.text or "", value))
                if value is None:
                    errors.append(f"{name}!{ref}: formula has no saved cached value")
                if c.attrib.get("t") == "e" or (value or "").startswith("#"):
                    errors.append(f"{name}!{ref}: cached formula error {value}")
        sheets[name] = cells

assert formulas, "No formulas found in workbook"
assert not errors, "; ".join(errors)
formula_text = " ".join(f for _, _, f, _ in formulas).upper()
assert "#REF!" not in formula_text

def cell(sheet, ref):
    value = sheets[sheet].get(ref)
    if value is None:
        raise AssertionError(f"Missing workbook cell {sheet}!{ref}")
    return float(value)

checks = []
# Ten public trend series reconcile to the workbook's Inputs sheet (the workbook
# presents these reported figures as inputs; only selected trends are charted in Overview).
trend_cells = {
    "Revenue": ("B5", "C5"), "Gross profit": ("B6", "C6"),
    "EBIT": ("B7", "C7"), "Adjusted EBITDA": ("B8", "C8"),
    "NMV": ("B9", "C9"), "Net inventory": ("B10", "C10"),
    "Current trade and other receivables": ("B11", "C11"),
    "Cash and cash equivalents": ("B12", "C12"), "Total assets": ("B13", "C13"),
    "Net operating cash flow": ("B14", "C14"),
}
for row in rows("financial_trends.csv"):
    label = row["metric"]
    b, c = trend_cells[label]
    close(f"Trend input FY2024 {label}", row["FY2024_EURm"], cell("Inputs", b))
    close(f"Trend input FY2025 {label}", row["FY2025_EURm"], cell("Inputs", c))
    if label in ("Revenue", "Gross profit", "Net inventory"):
        overview_row = {"Revenue": 6, "Gross profit": 7, "Net inventory": 9}[label]
        close(f"Overview absolute change {label}", row["absolute_change_EURm"],
              cell("Overview", f"D{overview_row}"))
        close(f"Overview percent change {label}", row["percent_change_if_positive_base"],
              cell("Overview", f"E{overview_row}")*100, tol=0.0001)

for row in rows("gross_margin.csv"):
    r = 8 if row["period"] == "FY2024" else 8
    col = "B" if row["period"] == "FY2024" else "C"
    close(f"Gross margin {row['period']}", float(row["gross_margin_percent"])/100,
          cell("Overview", f"{col}{r}"), tol=0.000001)

nwc_rows = rows("nwc_reconciliation.csv")
for i, row in enumerate(nwc_rows[:5], 5):
    close(f"NWC component FY2024 {row['component']}", row["FY2024_EURm"], cell("Working capital", f"B{i}"))
    close(f"NWC component FY2025 {row['component']}", row["FY2025_EURm"], cell("Working capital", f"C{i}"))
for col, period in [("B", "FY2024_EURm"), ("C", "FY2025_EURm")]:
    close(f"Calculated GFG NWC {period}", sum(float(r[period]) for r in nwc_rows[:5]),
          cell("Working capital", f"{col}10"))
    close(f"NWC difference after workbook rounding {period}", 0, cell("Working capital", f"{col}12"))
    close(f"Overview NWC movement {period}",
          float(next(r[period] for r in nwc_rows if r["component"] == "GFG-defined NWC")),
          cell("Overview", f"{col}10"))

inventory_rows = rows("inventory_analytics.csv")
inventory_cells = {"Raw materials and supplies": 5, "Finished goods and merchandise": 6,
                   "Less: provision": 7, "Net inventories": 10}
for row in inventory_rows:
    if row["metric"] in inventory_cells:
        r = inventory_cells[row["metric"]]
        close(f"Inventory {row['metric']} FY2024", row["FY2024"], cell("Inventory and ANZ", f"B{r}"))
        close(f"Inventory {row['metric']} FY2025", row["FY2025"], cell("Inventory and ANZ", f"C{r}"))
    elif row["metric"] == "Provision / gross finished goods":
        close("Provision ratio FY2024", float(row["FY2024"])/100, cell("Inventory and ANZ", "B9"), tol=0.000001)
        close("Provision ratio FY2025", float(row["FY2025"])/100, cell("Inventory and ANZ", "C9"), tol=0.000001)
for col in ("B", "C"):
    close(f"Inventory reconciliation {col}", 0, cell("Inventory and ANZ", f"{col}11"))

cash_rows = rows("proforma_cash_reconciliation.csv")
cash_cells = {
    "IFRS cash and cash equivalents": "C15",
    "APM restricted cash and deposit receivables adjustment": "C16",
    "Investment funds in APM reconciliation": "C17",
    "Calculated Pro-Forma Cash": "C18", "Published Pro-Forma Cash": "C19",
    "Difference to published APM": "C20",
    "Note 16 restricted cash plus deposit receivables": "C22",
    "Unallocated Note 16 total less APM adjustment": "C23",
}
for row in cash_rows:
    close(f"Cash bridge {row['component']}", row["EURm"], cell("Overview", cash_cells[row["component"]]))

for row in rows("anz_sensitivity.csv"):
    idx = {"Discount rates": 15, "EBITDA margin": 16, "Capital expenditure": 17,
           "2028/2029 revenue growth rate": 18}[row["assumption"]]
    close(f"ANZ threshold {row['assumption']}", row["published_break_even_change"], cell("Inventory and ANZ", f"B{idx}"))
    close(f"ANZ synthetic case {row['assumption']}", row["illustrative_scenario_change"], cell("Inventory and ANZ", f"C{idx}"))
    expected = row["published_threshold_reached_by_illustration"]
    actual = "Yes" if sheets["Inventory and ANZ"].get(f"E{idx}") == "At/beyond" else "No"
    if actual != expected:
        checks.append((f"ANZ threshold flag {row['assumption']}", expected, actual, "exact", False))
    else:
        checks.append((f"ANZ threshold flag {row['assumption']}", expected, actual, "exact", True))

failed = [c for c in checks if not c[4]]

def excel_reference(label):
    trend_rows = {"Revenue": 5, "Gross profit": 6, "EBIT": 7, "Adjusted EBITDA": 8,
                  "NMV": 9, "Net inventory": 10, "Current trade and other receivables": 11,
                  "Cash and cash equivalents": 12, "Total assets": 13,
                  "Net operating cash flow": 14}
    if label.startswith("Trend input "):
        period = "FY2024" if "FY2024" in label else "FY2025"
        metric = label.split(period + " ", 1)[1]
        return f"Inputs!{'B' if period == 'FY2024' else 'C'}{trend_rows[metric]}"
    if label.startswith("Overview absolute change ") or label.startswith("Overview percent change "):
        prefix = "Overview absolute change " if label.startswith("Overview absolute change ") else "Overview percent change "
        metric = label[len(prefix):]
        row = {"Revenue": 6, "Gross profit": 7, "Net inventory": 9}[metric]
        col = "D" if label.startswith("Overview absolute change ") else "E"
        return f"Overview!{col}{row}"
    if label.startswith("Gross margin "):
        return "Overview!B8" if "FY2024" in label else "Overview!C8"
    if label.startswith("NWC component "):
        period = "FY2024" if "FY2024" in label else "FY2025"
        component = label.split(period + " ", 1)[1]
        component_rows = {row["component"]: i for i, row in enumerate(rows("nwc_reconciliation.csv")[:5], 5)}
        return f"Working capital!{'B' if period == 'FY2024' else 'C'}{component_rows[component]}"
    if label.startswith("Calculated GFG NWC"):
        return "Working capital!B10" if "FY2024" in label else "Working capital!C10"
    if label.startswith("NWC difference after workbook rounding"):
        return f"Working capital!{'B' if 'FY2024' in label else 'C'}12"
    if label.startswith("Overview NWC movement"):
        return "Overview!B10" if "FY2024" in label else "Overview!C10"
    if label.startswith("Inventory "):
        metric = label.split("Inventory ", 1)[1].rsplit(" FY", 1)[0]
        row = {"Raw materials and supplies": 5, "Finished goods and merchandise": 6,
               "Less: provision": 7, "Net inventories": 10}.get(metric)
        if row:
            return f"Inventory and ANZ!{'B' if 'FY2024' in label else 'C'}{row}"
    if label.startswith("Provision ratio "):
        return "Inventory and ANZ!B9" if "FY2024" in label else "Inventory and ANZ!C9"
    if label.startswith("Inventory reconciliation "):
        return f"Inventory and ANZ!{'B' if label.endswith('B') else 'C'}11"
    cash_cells = {"IFRS cash and cash equivalents": "C15", "APM restricted cash and deposit receivables adjustment": "C16",
                  "Investment funds in APM reconciliation": "C17", "Calculated Pro-Forma Cash": "C18",
                  "Published Pro-Forma Cash": "C19", "Difference to published APM": "C20",
                  "Note 16 restricted cash plus deposit receivables": "C22",
                  "Unallocated Note 16 total less APM adjustment": "C23"}
    if label.startswith("Cash bridge "):
        return "Overview!" + cash_cells[label.split("Cash bridge ", 1)[1]]
    for prefix, col in (("ANZ threshold flag ", "E"), ("ANZ threshold ", "B"), ("ANZ synthetic case ", "C")):
        if label.startswith(prefix):
            assumption = label[len(prefix):]
            row = {"Discount rates": 15, "EBITDA margin": 16, "Capital expenditure": 17,
                   "2028/2029 revenue growth rate": 18}[assumption]
            return f"Inventory and ANZ!{col}{row}"
    raise AssertionError(f"Missing workbook cell for: {label}")

def source_locator(label):
    prefixes = ("Trend input FY2024 ", "Trend input FY2025 ",
                "Overview absolute change ", "Overview percent change ")
    if label.startswith(prefixes):
        prefix = next(prefix for prefix in prefixes if label.startswith(prefix))
        metric = label[len(prefix):]
        row = next(r for r in rows("financial_trends.csv") if r["metric"] == metric)
        return row.get("source_2024") or row.get("source_2025") or "Annual Report pp.47-52, 127-129"
    if label.startswith("Gross margin "):
        return "Annual Report p.47; gross profit and revenue"
    if label.startswith("NWC component "):
        component = label.split(" ", 3)[3]
        return next(r["source"] for r in rows("nwc_reconciliation.csv") if r["component"] == component)
    if label.startswith(("Calculated GFG NWC", "NWC difference", "Overview NWC movement")):
        return "Annual Report p.129; FY2024 inventory also Note 15 p.83"
    if label.startswith("Inventory "):
        metric = label.split("Inventory ", 1)[1].rsplit(" FY", 1)[0]
        row = next((r for r in rows("inventory_analytics.csv") if r["metric"] == metric), None)
        return row["source"] if row else "Annual Report p.83, Note 15"
    if label.startswith("Provision ratio "):
        return "Annual Report p.83, Note 15"
    if label.startswith("Cash bridge "):
        item = label.split("Cash bridge ", 1)[1]
        return "Annual Report p.84, Note 16" if item.startswith(("Note 16", "Unallocated Note 16")) else "Annual Report pp.48, 129; Pro-Forma Cash reconciliation"
    if label.startswith("ANZ "):
        return "Annual Report p.83, ANZ impairment sensitivity disclosure"
    return "GFG FY2025 Annual Report; see input locators"

source_url = "https://ir.global-fashion-group.com/media/document/4253e28d-9c76-4c94-8c4a-d67607b5e277/assets/LU2010095458-JA-2025-EQ-E-00.pdf?disposition=inline"
with (OUT / "reconciliation_results.csv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["check_number", "check", "python_value", "excel_reference",
        "excel_value", "tolerance", "status", "source_locator", "source_url"])
    writer.writeheader()
    for index, (label, left, right, tol, ok) in enumerate(checks, 1):
        locator = source_locator(label)
        page_match = re.search(r"p\.?\s*(\d+)", locator)
        page = page_match.group(1) if page_match else "47"
        writer.writerow({"check_number": index, "check": label, "python_value": left,
            "excel_reference": excel_reference(label), "excel_value": right, "tolerance": tol,
            "status": "PASS" if ok else "FAIL", "source_locator": locator,
            "source_url": f"{source_url}#page={page}"})

report = ["# Python–Excel calculation reconciliation", "",
          f"Public package release: 31 October 2026. Checks: {len(checks)}; passed: {len(checks)-len(failed)}; failed: {len(failed)}.",
          f"Workbook formulas: {len(formulas)}; formulas with missing cached values/errors: {len(errors)}.",
          "", "All amounts are €m unless stated. Numeric comparisons use absolute tolerance 0.00011 for €m/value outputs to allow workbook floating-point representation and CSV rounding; ratios and change rates use tighter tolerances. NWC and inventory tie-out cells are rounded to €0.01 in Excel. Python trends retain four decimal places for derived percentages; workbook display formats round visual percentages to one decimal place, while formulas retain full precision.",
          "", "## Result detail", "", "| Check | Python | Excel | Tolerance | Result |", "|---|---:|---:|---:|---|"]
for label, left, right, tol, ok in checks:
    report.append(f"| {label} | {left} | {right} | {tol} | {'PASS' if ok else 'FAIL'} |")
report += ["", "## Scope notes", "",
           "The Python trend file includes ten metrics; the workbook Inputs sheet contains the same ten reported input values, while its Overview calculates and displays revenue, gross profit, gross margin and net inventory changes. GFG-defined NWC, inventory composition/provision ratio, Pro-Forma Cash bridge and the four illustrative ANZ comparisons were reconciled to formula outputs. The sensitivity comparison is a one-variable numeric threshold check, not an impairment-model reproduction.",
           "", "The €0.9m Note 16/APM difference remains visible and unallocated. Q03 remains unresolved and unallocated. No accounting misstatement is inferred.",
           "", "A PASS means the defined calculations agree within the stated precision. It does not validate management's underlying accounting records or constitute audit evidence."]
(OUT / "calculation_reconciliation.md").write_text("\n".join(report) + "\n", encoding="utf-8")
print(f"checks={len(checks)} passed={len(checks)-len(failed)} failed={len(failed)} formulas={len(formulas)}")
if failed:
    raise SystemExit("Reconciliation failed; see output/calculation_reconciliation.md")

