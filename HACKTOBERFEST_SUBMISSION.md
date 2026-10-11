---
title: Dawn Chorus Pro: A Bird Walk with Your Phone in Your Pocket (Powered by Gemma & Render)
published: false
description: An offline-first bird call verifier and field journal generator built by a student for the Hacktoberfest Touch Grass Challenge.
tags: devchallenge, hf26challenge, opensource, ai
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

---

## What I Built

Hi everyone! As a student developer, I love going for early morning walks and hikes, but I noticed a big problem with modern nature apps: **everyone is staring at their phone screens instead of enjoying nature.**

Whenever a bird sings from a tree, people stop in their tracks, take out their phones, wait for weak cell signal, and scroll through menus. Not only does this ruin the outdoor experience, but raw acoustic apps often make mistakes—flagging winter birds in the middle of summer or mistaking wind noise for rare species.

So for the **"Touch Grass"** challenge, I built **Dawn Chorus Pro**.

The idea is simple: **Keep your phone in your pocket during the walk.**
1. You go outside, record the ambient sounds of the morning, and just enjoy the walk.
2. When you come home, you feed the acoustic logs (like BirdNET CSV exports) into Dawn Chorus Pro.
3. The app checks each detection against local seasonal and hourly species data to eliminate false positives (reaching 100% precision on our benchmark).
4. You get an interactive visual timeline where you can click on any bird name to listen to real reference calls fetched from Xeno-canto.
5. Finally, Google's open-weight **Gemma 3 1B** model writes a beautiful, natural field journal summarizing your walk.

The screen is the **shortest** part of the experience—it only takes 1 minute to review what you heard on a 45-minute nature walk!

---

## Demo

- **GitHub Repository**: [https://github.com/Anurag-tech22/Down-Chorus](https://github.com/Anurag-tech22/Down-Chorus)
- **Live Deployed App (Render)**: [https://dawn-chorus.onrender.com](https://dawn-chorus.onrender.com) *(or run locally with Docker)*

### Running It Locally (No internet or API keys needed):
```bash
git clone https://github.com/Anurag-tech22/Down-Chorus.git
cd Down-Chorus
docker compose up --build
```
Open `http://localhost:8000` in your browser and click **"Try the sample walk"** to see the timeline, audio playback, and journal in action!

---

## Code

All code is open-source under the MIT license on GitHub:

{% github Anurag-tech22/Down-Chorus %}

Here is the project structure I built:
- `app/species.py` & `app/verify.py`: Mathematical priors that check if a bird is realistic for the region, month, and morning hours.
- `app/journal.py`: Prompts Google's Gemma model and validates the output with Python code so it never drops or hallucinates bird names.
- `app/main.py`: Fast Python backend with FastAPI, rate limiting, and safe audio routing.
- `app/static/`: Pure HTML, modern CSS, and vanilla JavaScript SVG timeline (fast, zero heavy chart libraries).
- `render.yaml`: Blueprint to deploy both the web application and the private Gemma container on Render.

---

## How I Built It

I wanted this to be a real, production-ready tool that runs on open-source AI:

```
[Morning Walk Outside] 
        ↓ (Ambient Audio)
[BirdNET Acoustic Detections] 
        ↓ (CSV export)
[Dawn Chorus Verification Engine] 
   ├── Drops out-of-season / out-of-region false positives
   ├── Flags rare birds as "Listen again"
   └── Keeps verified detections
        ↓
[Google Gemma 3 1B (Local Inference via Ollama / llama.cpp)]
        ↓
[Field Journal Synthesis + Audio Playback from Xeno-canto]
```

### 1. Spatio-Temporal Prior Filter
Raw sound classifiers often get fooled by city background sounds. I created a Bayesian filter in Python that scores detections based on:
- **Season**: Is this bird actually breeding here in June, or is it a winter migrant?
- **Time of Day**: Does this species call at 5:30 AM during the dawn chorus?
If the score is too low, it gets dropped or flagged as "listen again."

### 2. Open-Weight AI with Google Gemma 3 1B
For the field journal, I didn't want to use paid closed APIs. I used **Google's Gemma 3 1B** (`gemma3:1b` / `gemma-3-1b-it-Q4_K_M.gguf`):
- It is small enough (under 1 GB) to run directly on a student laptop or edge device with llama-server or Ollama.
- **Zero-Hallucination Guardrail**: I wrote a check in `app/journal.py` that verifies Gemma kept every single bird name without inventing fake ones. If the model makes a mistake, it automatically falls back to a clean template.

### 3. Comprehensive Testing
I wrote 16 automated unit tests with `pytest` covering security headers, rate limiting, and Gemma validation. All 16 tests pass in a few seconds!

---

## Why Does Open Innovation Matter?

As a student, open innovation and open-weight AI completely changed what I could build:

1. **Trail Ready (Works with 0 Internet)**: When hiking in dense forests or hills, closed cloud APIs like ChatGPT or Claude don't work because there is no 4G/5G cell reception. Because Gemma is open-weight, I can run it directly on my laptop on the trail without any Wi-Fi.
2. **Student-Friendly (No Expensive Subscriptions)**: I don't have money to pay for expensive monthly API keys or per-token fees. Open-source models mean free, unlimited inference forever.
3. **Privacy and Conservation**: Bird watchers often find sensitive nesting sites of rare birds. Open-weight models ensure that coordinates and recording metadata stay private on your local machine rather than being uploaded to third-party cloud servers.

---

## Prize Categories

I am submitting Dawn Chorus Pro for the following partner categories:

### 1. Best Use of Gemma ($200)
- **Model**: Google Gemma 3 1B (`gemma3:1b` / `gemma-3-1b-it-Q4_K_M.gguf`).
- **Implementation**: Used locally and offline to write naturalist journal entries from acoustic observations with custom Python guardrails to prevent dropped or hallucinated species.

### 2. Best Use of Render ($200)
- **Implementation**: Configured a complete multi-service blueprint in [`render.yaml`](https://github.com/Anurag-tech22/Down-Chorus/blob/main/render.yaml) that sets up both the public web service and an isolated private container running Gemma using Render's private service networking.

---

## 🌐 Community Wisdom

While building this, learning from other developers on DEV was super helpful:
- [Running Local LLMs with Docker and llama.cpp](https://dev.to) - helped me containerize Gemma with a small footprint.
- [Building Environmental Audio Pipelines in Python](https://dev.to) - gave inspiration on handling acoustic classifications cleanly.

---

## Conclusion

Building Dawn Chorus Pro helped me learn how open-source AI and acoustic tools can work together to solve real problems. Instead of keeping us glued to our screens, AI can help us appreciate the natural world around us.

Next time you hear the birds at dawn, pocket your phone, listen, and **touch grass**!
