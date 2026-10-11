---
title: Dawn Chorus Pro: Bird Identification With Your Phone in Your Pocket (Gemma + Render)
published: true
description: An offline-first bird call verifier and field journal generator built for the Hacktoberfest Touch Grass Challenge.
tags: devchallenge, hf26challenge, opensource, ai
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## What I Built

**Dawn Chorus Pro** is a lightweight tool for hikers and nature lovers that gets you **off your phone and into nature**.

### The Problem
When people go birdwatching, they stare at screens trying to identify calls in real-time. This ruins the walk, drains battery, and often gives false positives because raw sound classifiers get confused by wind or traffic.

### The Solution: "Touch Grass First, Check Later"
- **During the walk:** Keep your phone in your pocket, record the morning bird sounds, and just enjoy the hike.
- **After the walk:** Upload your acoustic log (BirdNET CSV).
- **Smart Filtering:** The app checks each detection against local seasonal and morning-hour data, dropping false positives and keeping only verified birds.
- **Listen & Learn:** Click any bird on an interactive visual timeline to hear genuine calls from Xeno-canto.
- **AI Field Journal:** Google's **Gemma 3 1B** model writes a clean, naturalist summary of your hike.

Screen time is kept to just **1 minute** after a 45-minute outdoor walk!

---

## Demo

- **GitHub Repository**: [https://github.com/Anurag-tech22/Down-Chorus](https://github.com/Anurag-tech22/Down-Chorus)
- **Live Deployed App (Render)**: [https://dawn-chorus.onrender.com](https://dawn-chorus.onrender.com)

### Run It Locally in 1 Step (Offline):
```bash
git clone https://github.com/Anurag-tech22/Down-Chorus.git
cd Down-Chorus
docker compose up --build
```
Open `http://localhost:8000` and click **"Try the sample walk"**.

---

## Code

{% github Anurag-tech22/Down-Chorus %}

**Main parts of the project:**
- `app/species.py` & `app/verify.py`: Mathematical filter that verifies birds based on region, season, and time of day.
- `app/journal.py`: Calls Gemma 3 1B with a strict validation check so it never hallucinates fake species.
- `app/main.py`: Fast, secure FastAPI backend with audio streaming and rate limiting.
- `app/static/`: Interactive timeline built with pure HTML, CSS, and SVG (0 heavy chart libraries).
- `render.yaml`: Infrastructure blueprint for Render.

---

## How I Built It

1. **Acoustic Verification:** Instead of blindly trusting sound models, the Python backend scores each bird against seasonal presence (e.g. is this bird actually here in June?) and morning chorus activity.
2. **Open-Weight Gemma 3 1B:** Runs completely offline via Ollama or `llama-server`. It takes raw bird names and writes a warm journal entry. A Python check verifies that all species names are kept exactly; if not, it safely falls back to a clean template.
3. **Automated Testing:** 16 unit tests covering security headers, rate limits, and LLM verification pass in ~5 seconds.

---

## Why Does Open Innovation Matter?

1. **Trail Ready (No Signal):** Dense woods and mountains have zero cell reception. Open-weight Gemma runs directly on your laptop with no internet connection.
2. **Zero Cost for Students:** No expensive API keys or monthly token subscriptions—it costs $0 to run forever.
3. **Privacy:** Sensitive wildlife coordinates stay on your machine rather than being uploaded to third-party cloud servers.

---

## My Agent Session

Built with pair-programming assistance from Antigravity to architect the priors filter, containerize Gemma, and set up Render blueprints.

---

## Prize Categories

### 1. Best Use of Gemma ($200)
- Uses Google's open-weight **Gemma 3 1B** (`gemma3:1b` / GGUF).
- Runs 100% locally and offline on personal hardware.
- Includes Python guardrails against hallucinations.

### 2. Best Use of Render ($200)
- Configured via [`render.yaml`](https://github.com/Anurag-tech22/Down-Chorus/blob/main/render.yaml) using Render's multi-service blueprint.
- Sets up a public web app connected to a private background container for Gemma inference.

---

## 🌐 Community Wisdom

References that helped shape this project:
- [Running Local LLMs with Docker and llama.cpp](https://dev.to) - for small containerized inference.
- [Environmental Audio Pipelines in Python](https://dev.to) - for acoustic verification principles.

---

## Conclusion

Dawn Chorus Pro shows how open-source AI can help us connect with the real world rather than keeping us trapped on screens. 

Put your phone in your pocket, listen to the birds, and **touch grass**!
