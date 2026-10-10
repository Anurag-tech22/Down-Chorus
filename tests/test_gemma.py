import asyncio
from app import journal
class Resp:
    def __init__(s,t):s.t=t
    def json(s):return {"choices":[{"message":{"content":s.t}}]}
def fake(text,seen):
    class C:
        def __init__(s,**k):pass
        async def __aenter__(s):return s
        async def __aexit__(s,*a):pass
        async def post(s,url,json):seen.append(json);return Resp(text)
    return C
def test_sends_model_and_accepts(monkeypatch):
    seen=[];monkeypatch.setattr(journal.httpx,"AsyncClient",fake("A calm walk with Common Myna.",seen))
    assert asyncio.run(journal.polish("x","http://h",["Common Myna"])) and seen[0]["model"]==journal.MODEL
def test_rejects_dropped_species(monkeypatch):
    monkeypatch.setattr(journal.httpx,"AsyncClient",fake("A calm walk.",[]))
    assert asyncio.run(journal.polish("x","http://h",["Common Myna"])) is None
def test_none_without_url():assert asyncio.run(journal.polish("x","",[])) is None
