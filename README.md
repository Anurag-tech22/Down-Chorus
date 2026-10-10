# Dawn Chorus Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Dawn Chorus Pro is a lightweight web application for analyzing ambient bird sounds. It processes audio recordings through open-source acoustic analysis tools, verifies detections against regional/seasonal priors, and generates a field journal summary.

## Core Features

- **Priors Verification:** Filters raw acoustic CSV outputs against geographic, seasonal, and temporal metadata to reduce false positives.
- **Audio Integration:** Fetches and streams reference audio directly from the Xeno-canto database for verified species.
- **Automated Field Journal:** Summarizes verified detections using a background language model service or falls back to a deterministic template.
- **Client-Side Rendering:** Generates SVG timelines and interaction logic entirely in vanilla JavaScript, avoiding heavy charting dependencies.

## Architecture

1. **Input:** User uploads a CSV containing timestamped acoustic detections.
2. **Verification Pipeline:** FastAPI backend parses the CSV and applies filtering rules defined in `app/species.py`.
3. **LLM Integration (Optional):** Verified metadata is passed to a background language model service to synthesize a human-readable journal entry.
4. **Presentation:** The frontend renders an interactive SVG timeline. Audio playback is routed through the backend `/api/audio` endpoint to bypass client-side CORS constraints when streaming.

## Installation & Setup

### Prerequisites
- Python 3.10+
- (Optional) Docker for containerized deployment.

### Local Development

1. **Clone the repository and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The application will be available at `http://localhost:8000`.

### Running with AI Services

To enable the AI field journal, the backend expects a local language model API to be running in the background.

**Using Docker Compose**
```bash
docker compose up --build
```
*(The docker environment automatically sets up the necessary background model services for the journal feature).*

## Testing

Run the test suite using `pytest`:

```bash
python -m pytest -q
python eval/run.py
```

## Security & Performance Notes

- **Performance:** Parses data in a single pass without relying on a database layer.
- **Security:** Implements a strict Content Security Policy (CSP), restricts file uploads to <1MB, and performs rate limiting.
- **Accessibility:** UI supports keyboard navigation, screen-reader text tables, and respects `prefers-reduced-motion`.

## Limitations

The species priors table (`app/species.py`) is currently tailored to a specific region. For global accuracy, replace this static table with dynamic frequency data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
