import pytest
from fastapi.testclient import TestClient
from app import main
from app.species import prior
from app.verify import verify
c=TestClient(main.app)
def setup_function():main.hits.clear()
def test_prior_unknown_and_season():
    assert prior("Mystery Bird",6,6)<0.05 and prior("Asian Koel",12,6)<prior("Asian Koel",6,6)
def test_verify_drops_out_of_region():
    r=verify([{"name":"Himalayan Bulbul","conf":.9,"t":0}],6,6)[0];assert r["status"]!="keep"
def test_demo_ok_and_headers():
    r=c.get("/api/demo");assert r.status_code==200 and r.json()["summary"]["keep"]>=8
    assert "default-src 'self'" in r.headers["content-security-policy"] and r.headers["x-content-type-options"]=="nosniff"
def good():return {"csv":"Start (s),Common name,Confidence\n1,Common Myna,0.9\n","date":"2026-06-14","start":"06:00","place":"x"}
def test_analyze_ok():assert c.post("/api/analyze",json=good()).status_code==200
@pytest.mark.parametrize("patch",[{"csv":"a,b\n1,2"},{"csv":"Start (s),Common name,Confidence\nx,Myna,y"},{"date":"14-06-2026"},{"csv":"Start (s),Common name,Confidence\n"},{"csv":"x"*1_000_001}])
def test_rejects_bad_input(patch):assert c.post("/api/analyze",json={**good(),**patch}).status_code==422
def test_row_cap(monkeypatch):
    monkeypatch.setattr(main,"MAXROWS",2);big="Start (s),Common name,Confidence\n"+"1,Common Myna,0.9\n"*3
    assert c.post("/api/analyze",json={**good(),"csv":big}).status_code==422
def test_rate_limit(monkeypatch):
    monkeypatch.setattr(main,"LIMIT",2);codes=[c.get("/api/demo").status_code for _ in range(3)];assert codes==[200,200,429]
def test_no_docs_exposed():assert c.get("/docs").status_code==404
