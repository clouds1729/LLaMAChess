# LLaMAChess Architecture

## Overview

LLaMAChess uses a simple two-tier local architecture:

1. **Browser frontend** for chess interaction and question input.
2. **Local FastAPI backend** for prompt assembly and model inference using `llama-cpp-python`.

## Component diagram

```text
[User]
  ↓
[Browser UI]
  - Board interaction
  - Position tracking
  - FEN extraction
  - Question input
  ↓ HTTP POST /ask
[FastAPI Backend]
  - Request validation
  - Prompt construction
  - llama-cpp-python model call
  ↓
[GGUF Model on local disk]
  ↓
[FastAPI JSON response]
  ↓
[Browser answer panel]
```

## Request/response contract

### Request

`POST /ask`

```json
{
  "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 2 3",
  "question": "What is Black's best plan here?"
}
```

### Response

```json
{
  "answer": "<model-generated explanation>"
}
```

## Data flow details

1. Frontend updates chess state after each move.
2. Frontend derives current FEN from the board state.
3. User submits a natural-language question.
4. Frontend sends `{ fen, question }` to backend endpoint.
5. Backend validates payload and builds the model prompt.
6. Backend runs local inference through `llama-cpp-python`.
7. Backend returns text answer JSON.
8. Frontend renders answer to the user.

## Runtime dependencies

- Python environment with FastAPI and `llama-cpp-python`
- Local GGUF model file readable by backend
- Browser capable of running chess UI JavaScript

## Design trade-offs

- **Pros**
  - Fully local execution and privacy.
  - No paid inference API needed.
  - Easy to inspect and tune prompts.
- **Cons**
  - Quality and speed constrained by local hardware/model size.
  - LLM analysis is not a substitute for deterministic engine search.
  - Need manual model management (download, storage, config).

## Suggested future architecture improvements

- Add optional engine-validation microservice for tactical verification.
- Add caching by `(fen, question)` hash to reduce repeated inference.
- Add structured response schema (evaluation, plans, candidate moves).
- Add telemetry hooks for latency and token usage in local dev mode.
