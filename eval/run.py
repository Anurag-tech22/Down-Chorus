import sys,os;sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.verify import verify
from app.demo_data import DEMO
rows=verify([{"name":n,"conf":c,"t":t} for n,c,t,_ in DEMO],6,5.75);truth=[x[3] for x in DEMO]
def pr(sel):
    tp=sum(1 for r,t in zip(rows,truth) if r["status"] in sel and t);n=sum(1 for r in rows if r["status"] in sel)
    return tp,n,sum(truth)
a=pr({"keep","check","drop"});b=pr({"keep"})
print("| Stage | Detections | False positives | Precision | Real birds found |\n|---|---|---|---|---|")
print(f"| Raw BirdNET output | {a[1]} | {a[1]-a[0]} | {a[0]/a[1]:.0%} | {a[0]}/{a[2]} |")
print(f"| After verifier (kept only) | {b[1]} | {b[1]-b[0]} | {b[0]/b[1]:.0%} | {b[0]}/{b[2]} |")
print("\nSample set is hand-made, not a real recording. Replace with a labelled walk.")
