import os
import logging
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def health_check():
    return "Server operational!"


@app.route("/hello")
def hello():
    return "Hello, deployment works!"


@app.route("/paraphrase", methods=["POST"])
def paraphrase():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return jsonify({"error": "GROQ_API_KEY not configured"}), 500

    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        client = Groq(api_key=groq_api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a text rewriting assistant. "
                        "Rewrite the user's text to sound natural and human-written. "
                        "Preserve the original meaning exactly. "
                        "Do not add commentary, disclaimers, or explain what you did. "
                        "Return only the rewritten text."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=1024,
        )

        result = chat_completion.choices[0].message.content.strip()

        if result:
            return jsonify({"paraphrased": result, "success": True})

        return jsonify({"error": "Empty response from model"}), 500

    except Exception as e:
        logger.error(f"Error in /paraphrase: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
