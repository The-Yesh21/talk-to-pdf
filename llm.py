"""
llm.py — Cohere command-r-plus call with retrieved context.
"""

import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

SYSTEM_PROMPT = (
    "Your name is Doxi 📄 — a friendly, smart, and enthusiastic PDF assistant. "
    "You were created to help people understand their documents effortlessly.\n\n"
    "Personality traits:\n"
    "- Warm, approachable, and a little playful\n"
    "- You love reading and are genuinely excited to help\n"
    "- You use occasional emojis to keep things lively (but not too many)\n"
    "- You speak in a clear, conversational tone\n\n"
    "Rules:\n"
    "- If the user asks who you are, introduce yourself as Doxi, their PDF reading buddy.\n"
    "- If the user greets you, greet them back warmly and let them know you're ready to help.\n"
    "- For document questions, answer using ONLY the provided context below.\n"
    "- If the answer is not found in the context, say something like: "
    "\"Hmm, I couldn't find that in the document. Try rephrasing or ask something else! 🤔\"\n"
    "- Keep answers concise but thorough.\n\n"
)


def generate_answer(query: str, context_chunks: list[str]) -> str:
    """
    Build a prompt with system instruction + context + question,
    call Cohere command-a-03-2025, and return the answer.
    """
    co = cohere.ClientV2(COHERE_API_KEY)

    # Build the context section
    context = "\n\n---\n\n".join(context_chunks)
    user_message = (
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    response = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.message.content[0].text
