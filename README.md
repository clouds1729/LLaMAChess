# ♟️ LLaMAChess

LLaMAChess is a browser chess app that sends the current board state (FEN) and a natural-language question to a local LLaMA backend. It’s designed as a lightweight project showing how classic game state + local LLM prompting can produce human-readable chess explanations.

## What it does

- Renders an interactive chess board in the browser.
- Tracks game state and exports the current position as FEN.
- Accepts free-form user questions about the current position.
- Sends `{ fen, question }` to a local FastAPI backend running `llama-cpp-python`.
- Displays a natural-language response from a local GGUF model.

## Why local LLM chess explanations are interesting

Most chess tools provide engine lines and centipawn evaluations. Those are useful, but often hard for newer players to interpret quickly.

This project explores a different UX layer:

- **Private by default**: runs on your machine, no remote API required.
- **Low-friction experimentation**: easy to modify prompts and observe behavior.
- **Interpretability practice**: translate position features into plain language.
- **Bridge project**: combines frontend UI, structured game state, model serving, and prompt design in one small stack.

## Architecture

```text
Browser UI (index.html + JS)
  ├─ maintains chess state
  ├─ serializes current position to FEN
  └─ POST /ask { fen, question }
            ↓
Local FastAPI backend (Python)
  ├─ validates request
  ├─ builds prompt from FEN + user question
  └─ llama-cpp-python inference on local GGUF
            ↓
Response JSON { answer }
            ↓
Browser renders explanation in UI
```

Detailed architecture notes: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Tech stack

- **Frontend**: HTML, CSS, JavaScript
- **Chess state/utilities**: `chess.js` (and optional board UI libs)
- **Backend API**: FastAPI
- **Inference runtime**: `llama-cpp-python`
- **Model format**: GGUF (local file)

## Setup backend

> Requirements: Python 3.10+ recommended, enough RAM for your chosen model, and a local GGUF model file.

```bash
git clone https://github.com/clouds1729/LLaMAChess.git
cd LLaMAChess

# if backend code lives in ./backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Add GGUF model

1. Download a compatible GGUF chat/instruct model from a trusted source (for example, Hugging Face).
2. Place the file in your backend model directory (commonly `backend/models/`).
3. Update backend configuration/path if needed (for example, `MODEL_PATH`).
4. Restart the backend and confirm model load logs appear on startup.

Example expected location:

```text
backend/models/llama.gguf
```

## Run frontend

From repo root in a second terminal:

```bash
cd LLaMAChess
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500/index.html
```

## Example questions

Given any current position, try prompts like:

- “Who is better here and why?”
- “What are White’s top tactical ideas?”
- “What is Black threatening on the next move?”
- “Explain this position for a 900-rated player.”
- “What pawn breaks should I consider in this structure?”
- “Is there a forcing line I should calculate first?”

## Limitations

- LLM output can be plausible but incorrect (hallucinated lines/motifs).
- No guarantee of engine-strength move quality.
- Response quality depends heavily on prompt design and model choice.
- Larger GGUF models may be slow on CPU-only machines.
- FEN-only context omits deeper history unless explicitly provided.

## Roadmap

- Add optional engine cross-check mode (e.g., compare against Stockfish).
- Add move-by-move candidate line formatting in responses.
- Add prompt presets by skill level (beginner/intermediate/advanced).
- Add evaluation caching for repeated questions on same FEN.
- Add automated tests for prompt construction and API contract.
- Add Docker setup for one-command local launch.
