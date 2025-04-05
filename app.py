from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

@app.route("/")
def index():
    return "OrionBot backend is running."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"answer": "Вопрос не получен"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Meta-Llama-3-8B-Instruct",
            "messages": [{"role": "user", "content": question}]
        }

        response = requests.post("https://api.deepinfra.com/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})

    except Exception as e:
        print(e)
        return jsonify({"answer": "Произошла ошибка. Попробуйте позже."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
