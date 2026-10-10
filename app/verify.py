from .species import prior,S
KEEP,FLAG=0.45,0.25
def verify(dets,month,start_hour):
    """dets: list of dict(name,conf,t). Adds prior, score, status (keep|check|drop) and a reason."""
    out=[]
    for d in dets:
        hour=int((start_hour*3600+d["t"])//3600)%24
        p=prior(d["name"],month,hour);score=round(d["conf"]*(0.3+0.7*p),3)
        status="keep" if score>=KEEP else "check" if score>=FLAG else "drop"
        why=("not expected in this region" if d["name"] not in S else "unlikely this season or hour" if p<0.3 else "plausible here and now")
        out.append({**d,"prior":p,"score":score,"status":status,"why":why})
    return out
def summary(rows):
    c={k:sum(r["status"]==k for r in rows) for k in("keep","check","drop")}
    kept={r["name"] for r in rows if r["status"]=="keep"}
    return {**c,"total":len(rows),"species_kept":sorted(kept)}
