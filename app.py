
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

DEEPINFRA_API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7
    }

    response = requests.post(DEEPINFRA_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        answer = response.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": response.text}), 500

@app.route("/", methods=["GET"])
def index():
    return "OrionBot backend is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
