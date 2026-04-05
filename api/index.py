import os
import logging
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/humarin/chatgpt_paraphraser_on_T5_base"

app = Flask(__name__)


@app.route("/")
def health_check():
    return "Server operational!"


@app.route("/hello")
def hello():
    return "Hello, deployment works!"


@app.route("/paraphrase", methods=["POST"])
def paraphrase():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        return jsonify({"error": "HF_TOKEN not configured"}), 500

    data = request.get_json(force=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 512,
                "num_beams": 10,
                "do_sample": True,
                "top_k": 50,
            },
        }

        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=25)
        response.raise_for_status()

        api_response = response.json()
        logger.debug(f"Hugging Face API response: {api_response}")

        generated_text = api_response[0].get("generated_text", "").replace("paraphrase:", "").strip()

        if generated_text:
            return jsonify({"paraphrased": generated_text, "success": True})

        return jsonify({"error": "Unexpected response format", "response": api_response}), 500

    except requests.exceptions.Timeout:
        logger.error("Hugging Face API timed out")
        return jsonify({"error": "Hugging Face API request timed out"}), 500

    except Exception as e:
        logger.error(f"Error in /paraphrase: {str(e)}")
        return jsonify({"error": "An internal error occurred. Please try again."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))
