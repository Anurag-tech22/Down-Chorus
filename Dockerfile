FROM python:3.11-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m app
COPY app app
USER app
HEALTHCHECK CMD python -c "import urllib.request,os;urllib.request.urlopen(\"http://localhost:\"+os.getenv(\"PORT\",\"10000\")+\"/healthz\")"
CMD ["sh","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
