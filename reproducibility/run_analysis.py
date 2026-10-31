"""Reproduce Project 1A analytics from the published, sanitized input files.

Company amounts are transcribed from GFG's FY2025 Annual Report. Scenario
changes are clearly labelled synthetic illustrations.
"""
from pathlib import Path
import csv

ROOT=Path(__file__).parent
DATA=ROOT/"data"
OUT=ROOT/"output"
OUT.mkdir(exist_ok=True)

def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path,columns,rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns); w.writeheader(); w.writerows(rows)

register={r["ID"]:r for r in read_csv(ROOT/"inputs.csv")}
note={r["metric"]:r for r in read_csv(ROOT/"public_note_inputs.csv")}
nwc_inputs=read_csv(DATA/"nwc_components.csv")

def num(id): return float(register[id]["Value"])
def note_num(metric,period): return float(note[metric][period])
def rnd(value): return round(value+0.0,4)

metrics=[
 ("Revenue","S02","S01"),("Gross profit","S03A","S03"),
 ("EBIT","S05A","S05"),("Adjusted EBITDA","S06A","S06"),
 ("Net inventory","S08","S07"),("Current trade and other receivables","S09A","S09"),
 ("Cash and cash equivalents","S10A","S10"),("Total assets","S11A","S11"),
 ("NMV","S13A","S13"),("Net operating cash flow","S12A","S12"),
]
trends=[]
for label,id24,id25 in metrics:
    prior,current=num(id24),num(id25)
    trends.append({"metric":label,"FY2024_EURm":prior,"FY2025_EURm":current,
        "absolute_change_EURm":rnd(current-prior),
        "percent_change_if_positive_base":rnd(100*(current/prior-1)) if prior>0 else "",
        "source_2024":register[id24]["Locator"],"source_2025":register[id25]["Locator"],
        "note":"Percent change omitted where FY2024 base is negative." if prior<=0 else ""})
write_csv(OUT/"financial_trends.csv",list(trends[0]),trends)

gross_margin=[]
for period,gross_profit,revenue in [("FY2024",num("S03A"),num("S02")),("FY2025",num("S03"),num("S01"))]:
    gross_margin.append({"period":period,"gross_profit_EURm":gross_profit,"revenue_EURm":revenue,
                         "gross_margin_percent":rnd(100*gross_profit/revenue),
                         "source":"Calculated from Annual Report p.47; register S01-S03A"})
write_csv(OUT/"gross_margin.csv",list(gross_margin[0]),gross_margin)

nwc=[{"component":r["component"],"FY2024_EURm":float(r["FY2024_EURm"]),
      "FY2025_EURm":float(r["FY2025_EURm"]),"source":r["source_locator"]} for r in nwc_inputs]
for period,reported in [("FY2024_EURm",-54.8),("FY2025_EURm",-80.3)]:
    assert round(sum(r[period] for r in nwc),1)==reported
nwc.append({"component":"GFG-defined NWC","FY2024_EURm":-54.8,"FY2025_EURm":-80.3,"source":"Calculated; Annual Report p.129 published totals"})
write_csv(OUT/"nwc_reconciliation.csv",list(nwc[0]),nwc)

cash=[{"component":"IFRS cash and cash equivalents","EURm":num("S10"),"basis":"Reported; source register S10"},
      {"component":"APM restricted cash and deposit receivables adjustment","EURm":num("S17"),"basis":"Reported APM; source register S17"},
      {"component":"Investment funds in APM reconciliation","EURm":num("S24"),"basis":"Reported; source register S24"}]
cash_total=sum(r["EURm"] for r in cash)
cash.extend([{"component":"Calculated Pro-Forma Cash","EURm":round(cash_total,2),"basis":"Calculated sum of above"},
             {"component":"Published Pro-Forma Cash","EURm":num("S23"),"basis":"Reported; source register S23"},
             {"component":"Difference to published APM","EURm":round(cash_total-num("S23"),2),"basis":"Calculated"},
             {"component":"Note 16 restricted cash plus deposit receivables","EURm":num("C04"),"basis":"Reported component total; source register C04"},
             {"component":"Unallocated Note 16 total less APM adjustment","EURm":num("C08"),"basis":"Unresolved public-source limitation; no allocation"}])
write_csv(OUT/"proforma_cash_reconciliation.csv",list(cash[0]),cash)

inventory=[]
for label,metric in [("Raw materials and supplies","raw_materials_and_supplies"),
                     ("Finished goods and merchandise","finished_goods_and_merchandise"),
                     ("Less: provision","inventory_provision")]:
    inventory.append({"metric":label,"FY2024":note_num(metric,"FY2024"),"FY2025":note_num(metric,"FY2025"),
                      "unit":"EUR million","source":"Annual Report p.83 Note 15"})
assert round(sum(r["FY2024"] for r in inventory),1)==num("S08")
assert round(sum(r["FY2025"] for r in inventory),1)==num("S07")
inventory.extend([
 {"metric":"Net inventories","FY2024":num("S08"),"FY2025":num("S07"),"unit":"EUR million","source":"Annual Report p.83 Note 15; statement p.48"},
 {"metric":"Provision / gross finished goods","FY2024":rnd(100*9.3/105.2),"FY2025":rnd(100*7.1/88.3),"unit":"percent","source":"Calculated from Annual Report p.83 Note 15"},
])
write_csv(OUT/"inventory_analytics.csv",list(inventory[0]),inventory)

sensitivity=[]
for r in read_csv(ROOT/"anz_sensitivity_inputs.csv"):
    threshold=float(r["break_even_change"]); scenario=float(r["illustrative_scenario_change"])
    reached=(scenario>=threshold) if threshold>0 else (scenario<=threshold)
    sensitivity.append({"assumption":r["assumption"],"published_break_even_change":threshold,
        "unit":r["unit"],"illustrative_scenario_change":scenario,"published_threshold_reached_by_illustration":"Yes" if reached else "No",
        "source":r["source_locator"],"scope":"One-variable published threshold; illustrative scenario, not impairment amount."})
write_csv(OUT/"anz_sensitivity.csv",list(sensitivity[0]),sensitivity)

summary=f"""# GFG Project 1A — reproducible analytics pilot

Generated from the published input files and GFG FY2025 Annual Report disclosures. All amounts are €m unless stated otherwise.

## Financial trends

- Revenue: €{num('S02'):.1f}m to €{num('S01'):.1f}m ({100*(num('S01')/num('S02')-1):.2f}%).
- Gross profit: €{num('S03A'):.1f}m to €{num('S03'):.1f}m; gross margin {100*num('S03A')/num('S02'):.1f}% to {100*num('S03')/num('S01'):.1f}%.
- Net inventory: €{num('S08'):.1f}m to €{num('S07'):.1f}m ({100*(num('S07')/num('S08')-1):.2f}%).

## Working capital and inventory

- GFG-defined NWC: €(54.8)m to €(80.3)m. This is the company's definition, not conventional current assets less current liabilities. The FY2024 KPI table's €0.1m inventory display inconsistency remains documented.
- The inventory provision divided by gross finished goods and merchandise moved from {100*9.3/105.2:.2f}% to {100*7.1/88.3:.2f}%. This aggregate comparison cannot establish item-level NRV or provision adequacy.

## Impairment sensitivity

The sensitivity output reproduces GFG's published one-variable ANZ break-even changes from Annual Report p.83 and compares them with clearly labelled illustrative changes. It is not a reproduction of management's impairment model and does not calculate an impairment amount.

These are public-source analytics and synthetic illustrations. No proposed audit procedure was performed, no underlying accounting records were tested and no audit opinion is expressed.
"""
(OUT/"results_summary.md").write_text(summary,encoding="utf-8")
print(f"Generated: {len(trends)} trend metrics, {len(nwc)} NWC rows, {len(inventory)} inventory rows, {len(sensitivity)} sensitivity rows.")

