"""Generate desktop and narrow-screen financial charts from the pilot CSV outputs."""
from pathlib import Path
import csv
from html import escape

ROOT = Path(__file__).parent
OUT = ROOT / "output" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, BLUE, TEAL, AMBER = "#17324F", "#3677B8", "#16847E", "#E49B31"
INK, MUTED, GRID, PALE = "#263442", "#657583", "#D8E1E7", "#EAF0F4"

def read_csv(name):
    with (ROOT / "output" / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def svg_start(width, height, title, desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<title id="title">{escape(title)}</title>', f'<desc id="desc">{escape(desc)}</desc>',
            '<rect width="100%" height="100%" fill="#ffffff"/>']

def txt(parts, x, y, value, size=14, weight="400", color=INK, anchor="start"):
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>')

def rect(parts, x, y, w, h, color, radius=4):
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(0,w):.1f}" height="{max(0,h):.1f}" rx="{radius}" fill="{color}"/>')

def line(parts, x1, y1, x2, y2, color=GRID, width=1):
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')

def get_values():
    trend = {r["metric"]: r for r in read_csv("financial_trends.csv")}
    series = [("Revenue", 100.0, 100*float(trend["Revenue"]["FY2025_EURm"])/float(trend["Revenue"]["FY2024_EURm"]), BLUE),
              ("Gross profit", 100.0, 100*float(trend["Gross profit"]["FY2025_EURm"])/float(trend["Gross profit"]["FY2024_EURm"]), TEAL),
              ("Net inventory", 100.0, 100*float(trend["Net inventory"]["FY2025_EURm"])/float(trend["Net inventory"]["FY2024_EURm"]), AMBER)]
    nwc = read_csv("nwc_reconciliation.csv")[-1]
    nwc_values = [("FY2024", float(nwc["FY2024_EURm"])), ("FY2025", float(nwc["FY2025_EURm"]))]
    sensitivities=[]
    for row in read_csv("anz_sensitivity.csv"):
        pct=100*abs(float(row["illustrative_scenario_change"])/float(row["published_break_even_change"]))
        label=row["assumption"].replace("2028/2029 revenue growth rate","Revenue growth")
        sensitivities.append((label,pct))
    return series,nwc_values,sensitivities

def desktop_chart():
    W,H=1200,930
    p=svg_start(W,H,"GFG financial analytics — FY2024 to FY2025", "Indexed financial trends, GFG-defined net working capital and illustrative ANZ sensitivity comparisons. All amounts are public-source or illustrative as labelled.")
    txt(p,40,43,"GFG Project 1A · public-source financial analysis",25,"700",NAVY)
    txt(p,40,70,"Validated numeric series: FY2024–FY2025 · €m unless otherwise stated",14,"400",MUTED)
    series,nwc,sens=get_values()
    txt(p,40,116,"Financial trends · FY2024 = 100",19,"700",NAVY)
    txt(p,820,116,"■ FY2024",12,"700",BLUE); txt(p,920,116,"■ FY2025",12,"700",NAVY)
    x0,y0,w,h=110,148,940,155
    for tick in (80,85,90,95,100,105):
        y=y0+(105-tick)/25*h; line(p,x0,y,x0+w,y); txt(p,76,y+4,tick,11,"400",MUTED,"end")
    for i,(label,v24,v25,color) in enumerate(series):
        center=250+i*300
        for j,val in enumerate((v24,v25)):
            x=center+j*68; y=y0+(105-val)/25*h; base=y0+h
            rect(p,x,y,46,base-y,color if j==0 else NAVY,3)
            txt(p,x+23,y-7,f"{val:.1f}",12,"700",INK,"middle")
        txt(p,center+50,y0+h+25,label,14,"700",NAVY,"middle")
    txt(p,40,382,"GFG-defined net working capital",19,"700",NAVY)
    txt(p,40,405,"Negative values are shown to the left of zero.",12,"400",MUTED)
    xzero=730; scale=7.25
    line(p,xzero,420,xzero,534,GRID,2)
    for i,(period,value) in enumerate(nwc):
        y=436+i*49; width=abs(value)*scale; left=xzero-width
        txt(p,80,y+20,period,14,"700",NAVY)
        rect(p,left,y,width,28,BLUE if i==0 else NAVY,4)
        # Keep the amount inside the negative bar so it cannot clip beyond the SVG viewBox.
        txt(p,left+10,y+19,f"−€{abs(value):.1f}m",13,"700","#ffffff")
    txt(p,80,548,"Longer bar = more negative · company-defined APM, not conventional current assets less current liabilities.",12,"400",MUTED)
    txt(p,40,612,"Illustrative ANZ changes · % of disclosed one-variable break-even movement",19,"700",NAVY)
    sx,sy,sw,sh=330,650,700,180
    for tick in (0,25,50,75,100):
        y=sy+(100-tick)/100*sh; line(p,sx,y,sx+sw,y); txt(p,sx-14,y+4,f"{tick}%",11,"400",MUTED,"end")
    for i,(label,pct) in enumerate(sens):
        x=sx+45+i*165; y=sy+(100-pct)/100*sh
        rect(p,x,y,72,sy+sh-y,TEAL,4); txt(p,x+36,y-7,f"{pct:.1f}%",12,"700",INK,"middle")
        txt(p,x+36,sy+sh+22,label,11,"400",INK,"middle")
    txt(p,40,892,"Synthetic assumptions only. This comparison does not reproduce management’s model or calculate impairment.",12,"400",MUTED)
    p.append("</svg>")
    (OUT/"project1a_charts.svg").write_text("\n".join(p),encoding="utf-8")

def mobile_chart():
    W,H=360,1320
    p=svg_start(W,H,"GFG financial analytics — mobile chart", "Mobile-layout chart showing FY2024 and FY2025 financial trends, negative working capital values and synthetic sensitivity comparisons.")
    txt(p,16,32,"GFG Project 1A",21,"700",NAVY)
    txt(p,16,56,"Public-source analytics · €m unless stated",12,"400",MUTED)
    series,nwc,sens=get_values()
    txt(p,16,98,"Financial trends",17,"700",NAVY)
    txt(p,16,121,"FY2024 = 100 · labels show index values",11,"400",MUTED)
    txt(p,178,148,"FY2024",10,"700",BLUE); txt(p,244,148,"FY2025",10,"700",NAVY)
    bx,bw=96,180
    for i,(label,v24,v25,color) in enumerate(series):
        y=178+i*92
        txt(p,16,y,label,14,"700",NAVY)
        for j,val in enumerate((v24,v25)):
            yy=y+18+j*27; rect(p,bx,yy,bw,14,PALE,3); rect(p,bx,yy,bw*val/105,14,color if j==0 else NAVY,3)
            txt(p,346,yy+12,f"{val:.1f}",11,"700",INK,"end")
    line(p,16,462,344,462,GRID,1)
    txt(p,16,494,"GFG-defined net working capital",17,"700",NAVY)
    txt(p,16,516,"Longer bar = more negative",11,"400",MUTED)
    maxval=max(abs(v) for _,v in nwc)
    for i,(period,value) in enumerate(nwc):
        y=552+i*74
        txt(p,16,y,period,13,"700",NAVY)
        txt(p,344,y,f"−€{abs(value):.1f}m",13,"700",INK,"end")
        rect(p,16,y+12,328,19,PALE,4); rect(p,16,y+12,328*abs(value)/maxval,19,BLUE if i==0 else NAVY,4)
    txt(p,16,720,"Management-defined APM; not conventional current assets less current liabilities.",11,"400",MUTED)
    line(p,16,748,344,748,GRID,1)
    txt(p,16,781,"Illustrative ANZ sensitivity",17,"700",NAVY)
    txt(p,16,803,"Scenario change as % of published one-variable threshold",10,"400",MUTED)
    for i,(label,pct) in enumerate(sens):
        y=844+i*86
        txt(p,16,y,label,12,"700",NAVY)
        rect(p,16,y+12,260,18,PALE,4); rect(p,16,y+12,260*min(pct,100)/100,18,TEAL,4)
        txt(p,344,y+27,f"{pct:.1f}%",12,"700",INK,"end")
    txt(p,16,1210,"Synthetic assumptions only · not a forecast or impairment calculation.",10,"400",MUTED)
    txt(p,16,1240,"Validated numeric coverage: FY2024–FY2025 only.",10,"700",NAVY)
    p.append("</svg>")
    (OUT/"project1a_charts_mobile.svg").write_text("\n".join(p),encoding="utf-8")

if __name__ == "__main__":
    desktop_chart()
    mobile_chart()
    print(OUT/"project1a_charts.svg")
    print(OUT/"project1a_charts_mobile.svg")

