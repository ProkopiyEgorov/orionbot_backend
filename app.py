from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DEEPINFRA_API_KEY = os.environ.get("DEEPINFRA_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = requests.post(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "meta-llama/Meta-Llama-3-8B-Instruct",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7
        }
    )

    if response.status_code != 200:
        return jsonify({"error": f"DeepInfra error: {response.text}"}), 500

    result = response.json()
    answer = result["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

@app.route("/", methods=["GET"])
def index():
    return "OrionBot backend is running."

