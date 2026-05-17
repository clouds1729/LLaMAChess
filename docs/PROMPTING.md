# Prompt Construction (FEN + User Question)

This document describes how LLaMAChess should build prompts before sending them to the local GGUF model.

## Inputs

The backend receives a JSON payload:

```json
{
  "fen": "<current position in Forsyth-Edwards Notation>",
  "question": "<natural-language user question>"
}
```

## Prompting goals

- Keep the model grounded in the exact board position.
- Keep answers chess-focused and instructional.
- Reduce hallucinated certainty and unsupported tactical claims.
- Encourage concise, structured explanations.

## Recommended prompt template

Use a system-style instruction plus a user block that includes FEN and question.

```text
You are a chess analysis assistant.
Use ONLY the provided FEN position as the source of truth.
If uncertain, say what must be calculated and avoid fabricating forced lines.
Explain ideas clearly and concretely.

Position (FEN):
{fen}

User question:
{question}

Answer format:
1) Short evaluation (who is better / equal and why)
2) Key tactical and positional ideas
3) Candidate moves to consider (with brief rationale)
4) Practical advice for a human player
```

## Guardrails

- Reject empty or malformed FEN before inference.
- Reject empty question strings.
- Optionally cap question length (to avoid prompt abuse).
- Avoid claiming forced mates unless the model clearly demonstrates a legal line.

## Response style recommendations

- Prefer plain language over notation-heavy dumps.
- Mention uncertainty explicitly where relevant.
- Keep answers bounded (for example, 120–250 words) unless user asks for deep analysis.
- Separate tactical threats from long-term plans.

## Optional enhancements

- Add a “skill level” field and adapt depth/tone accordingly.
- Add move history when available (FEN alone does not encode full history).
- Add post-processing to normalize bullet formatting.
- Add optional engine verification pass for critical claims.
