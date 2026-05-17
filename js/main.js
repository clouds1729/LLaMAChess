(function () {
  const submitBtn = document.getElementById('llamaSubmit');
  const queryInput = document.getElementById('llamaQuery');
  const output = document.getElementById('llamaResponse');

  if (!submitBtn || !queryInput || !output) {
    return;
  }

  const BACKEND_URL = 'http://127.0.0.1:8000';

  async function askLlama() {
    const question = queryInput.value.trim();
    if (!question) {
      output.textContent = 'Please enter a question before submitting.';
      return;
    }

    const fen = typeof window.game?.fen === 'function'
      ? window.game.fen()
      : 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

    const legalMoves = typeof window.game?.moves === 'function' ? window.game.moves({ verbose: false }) : [];

    output.textContent = 'Thinking...';

    try {
      const response = await fetch(`${BACKEND_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fen, question, legal_moves: legalMoves })
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 503 && String(data.detail || '').includes('Model file not found')) {
          output.textContent = 'Backend is running, but no GGUF model file was found. Add model file and restart backend.';
          return;
        }
        output.textContent = data.detail || 'Request failed. Please verify backend logs.';
        return;
      }

      output.textContent = data.answer || 'No answer returned.';
    } catch (_err) {
      output.textContent = 'Cannot reach backend at http://127.0.0.1:8000. Start the local backend and try again.';
    }
  }

  submitBtn.addEventListener('click', askLlama);
})();
