from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


MODEL_PATH = Path(__file__).resolve().parent / "models" / "llama.gguf"

app = FastAPI(title="LLaMAChess Local Backend")


class AskRequest(BaseModel):
    fen: str = Field(..., min_length=7, max_length=120)
    question: str = Field(..., min_length=3, max_length=500)
    legal_moves: List[str] | None = Field(default=None, max_length=218)

    @field_validator("fen")
    @classmethod
    def validate_fen(cls, value: str) -> str:
        parts = value.strip().split()
        if len(parts) != 6:
            raise ValueError("FEN must contain 6 space-separated fields.")

        board, side, castling, ep, halfmove, fullmove = parts
        ranks = board.split("/")
        if len(ranks) != 8:
            raise ValueError("FEN board must contain 8 ranks.")

        valid_pieces = set("prnbqkPRNBQK")
        for rank in ranks:
            count = 0
            for char in rank:
                if char.isdigit():
                    count += int(char)
                elif char in valid_pieces:
                    count += 1
                else:
                    raise ValueError("FEN contains invalid board characters.")
            if count != 8:
                raise ValueError("Each FEN rank must describe exactly 8 squares.")

        if side not in {"w", "b"}:
            raise ValueError("FEN side-to-move must be 'w' or 'b'.")

        if castling != "-" and any(c not in "KQkq" for c in castling):
            raise ValueError("FEN castling rights are invalid.")

        if ep != "-":
            if len(ep) != 2 or ep[0] not in "abcdefgh" or ep[1] not in "36":
                raise ValueError("FEN en-passant square is invalid.")

        if not halfmove.isdigit() or not fullmove.isdigit():
            raise ValueError("FEN move counters must be integers.")

        return value.strip()

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Question must be at least 3 characters.")
        return cleaned


class AskResponse(BaseModel):
    answer: str


def prompt_builder(fen: str, question: str, legal_moves: List[str] | None = None) -> str:
    side = "White" if fen.split()[1] == "w" else "Black"
    legal_line = ", ".join(legal_moves) if legal_moves else "Unavailable"
    return (
        "You are a careful chess explainer.\n"
        f"FEN: {fen}\n"
        f"Side to move: {side}\n"
        f"Legal moves (if provided): {legal_line}\n"
        f"User question: {question}\n"
        "Never claim a move is legal unless it is in the provided legal moves list "
        "or clearly marked as a candidate requiring verification."
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask_llama(payload: AskRequest) -> AskResponse:
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail=(
                f"Model file not found at {MODEL_PATH}. "
                "Place your GGUF file there before starting inference."
            ),
        )

    prompt = prompt_builder(payload.fen, payload.question, payload.legal_moves)
    # Keep local/offline behavior simple and deterministic until inference is wired.
    return AskResponse(answer=f"Model is available. Prompt ready.\n\n{prompt}")
