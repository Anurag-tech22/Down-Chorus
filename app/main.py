import csv,io,os,time,collections
from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel,Field
from .verify import verify,summary
from .journal import draft,polish
from .demo_data import DEMO,META
LLAMA=os.getenv("LLAMA_URL","");LLAMA=("http://"+LLAMA) if LLAMA and not LLAMA.startswith("http") else LLAMA
LIMIT=int(os.getenv("RATE_LIMIT","60"));MAXROWS=5000
app=FastAPI(title="Dawn Chorus Pro",docs_url=None,redoc_url=None);app.add_middleware(GZipMiddleware,minimum_size=800)
hits=collections.defaultdict(collections.deque)
CSP="default-src 'self'; media-src 'self' https://xeno-canto.org blob:; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
@app.middleware("http")
async def guard(req:Request,call):
    if req.url.path.startswith("/api/"):
        ip=req.headers.get("x-forwarded-for",req.client.host if req.client else "?").split(",")[0].strip();q=hits[ip];now=time.time()
        while q and now-q[0]>60:q.popleft()
        if len(q)>=LIMIT:return JSONResponse({"detail":"Too many requests. Wait a minute."},429)
        q.append(now)
    r=await call(req)
    r.headers.update({"Content-Security-Policy":CSP,"X-Content-Type-Options":"nosniff","Referrer-Policy":"no-referrer","Permissions-Policy":"camera=(),microphone=(),geolocation=()","X-Frame-Options":"DENY"})
    return r
class Walk(BaseModel):
    csv:str=Field(max_length=1_000_000);date:str=Field(pattern=r"^\d{4}-\d{2}-\d{2}$");start:str=Field(pattern=r"^\d{2}:\d{2}$");place:str=Field(default="",max_length=80)
def parse(text):
    rd=csv.DictReader(io.StringIO(text));f=rd.fieldnames or []
    need={"Start (s)","Common name","Confidence"}
    if not need<=set(f):raise HTTPException(422,"CSV needs columns: Start (s), Common name, Confidence (BirdNET-Analyzer output).")
    rows=[]
    for i,r in enumerate(rd):
        if i>=MAXROWS:raise HTTPException(422,f"Too many rows (max {MAXROWS}).")
        try:rows.append({"name":r["Common name"].strip()[:60],"conf":min(1.0,max(0.0,float(r["Confidence"]))),"t":max(0.0,float(r["Start (s)"]))})
        except(ValueError,TypeError):raise HTTPException(422,f"Bad number on row {i+2}.")
    if not rows:raise HTTPException(422,"No detections found in the CSV.")
    return rows
async def run(dets,date,start,place):
    rows=verify(dets,int(date[5:7]),int(start[:2])+int(start[3:])/60)
    s=summary(rows);j=draft(place or "the trail",date,start,rows)
    return {"rows":rows,"summary":s,"journal":j,"journal_ai":await polish(j,LLAMA,s["species_kept"]),"minutes":round(max(r["t"] for r in rows)/60)}
@app.post("/api/analyze")
async def analyze(w:Walk):return await run(parse(w.csv),w.date,w.start,w.place)
@app.get("/api/demo")
async def demo():return await run([{"name":n,"conf":c,"t":t} for n,c,t,_ in DEMO],META["date"],META["start"],META["place"])|{"demo":True}
@app.get("/api/gemma-check")
async def gemma_check():
    out=await polish("Test entry. I logged 1 species by ear: Common Myna.",LLAMA,["Common Myna"])
    return {"configured":bool(LLAMA),"ok":out is not None,"sample":out}
@app.get("/healthz")
def hz():return {"ok":True,"gemma":bool(LLAMA)}
@app.get("/api/audio")
async def get_audio(bird: str):
    import httpx, re
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            r = await client.get(f"https://xeno-canto.org/explore?query={bird.replace(' ','+')}", timeout=5)
            m = re.search(r"src='(https://xeno-canto\.org/sounds/uploaded/[^']+\.mp3)'", r.text)
            if m: return {"url": m.group(1)}
            return JSONResponse({"url": ""}, 404)
        except Exception as e:
            return JSONResponse({"url": "", "error": str(e)}, 500)

@app.get("/")
def index():return FileResponse("app/static/index.html")
app.mount("/static",StaticFiles(directory="app/static"),name="s")
