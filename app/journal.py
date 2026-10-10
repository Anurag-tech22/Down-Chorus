import os,httpx
MODEL=os.getenv("LLM_MODEL","gemma3:1b")  # Ollama tag; llama-server ignores it
def draft(place,date,start,rows):
    kept=sorted({r["name"] for r in rows if r["status"]=="keep"});chk=sorted({r["name"] for r in rows if r["status"]=="check"})
    if not kept:return f"{date}, {place}. A quiet walk: nothing I can vouch for yet."
    s=f"{date}, {place}. I set out at {start} and logged {len(kept)} species by ear: "+", ".join(kept)+"."
    if chk:s+=f" Worth a second listen before I trust them: {', '.join(chk)}."
    return s
async def polish(text,url,names=()):
    """Ask Gemma for a warmer journal. Returns None on any failure, or if it dropped a species name."""
    if not url:return None
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r=await c.post(f"{url}/v1/chat/completions",json={"model":MODEL,"messages":[{"role":"user","content":"Rewrite as a warm four-sentence field-journal entry. Keep every bird name exactly. Do not add species or facts:\n"+text}],"max_tokens":220,"temperature":0.4})
            out=r.json()["choices"][0]["message"]["content"].strip()
    except Exception:return None
    return out if out and all(n in out for n in names) else None
