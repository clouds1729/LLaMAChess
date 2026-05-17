from fastapi.testclient import TestClient

from backend.main import MODEL_PATH, app, prompt_builder

client = TestClient(app)


VALID_PAYLOAD = {
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "question": "What should White focus on?",
    "legal_moves": ["e2e4", "d2d4"],
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_fen_rejected():
    bad = {**VALID_PAYLOAD, "fen": "bad fen"}
    response = client.post("/ask", json=bad)
    assert response.status_code == 422


def test_empty_question_rejected():
    bad = {**VALID_PAYLOAD, "question": "  "}
    response = client.post("/ask", json=bad)
    assert response.status_code == 422


def test_model_missing_returns_503(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.main.MODEL_PATH", tmp_path / "missing.gguf")
    response = client.post("/ask", json=VALID_PAYLOAD)
    assert response.status_code == 503
    assert "Model file not found" in response.json()["detail"]


def test_prompt_builder_includes_reliability_fields():
    prompt = prompt_builder(VALID_PAYLOAD["fen"], VALID_PAYLOAD["question"], VALID_PAYLOAD["legal_moves"])
    assert "FEN:" in prompt
    assert "Side to move:" in prompt
    assert "Legal moves" in prompt
    assert "Never claim a move is legal" in prompt
