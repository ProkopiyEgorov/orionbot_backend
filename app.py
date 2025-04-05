# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")  # переменная окружения
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

@app.route('/')
def home():
    return "OrionBot backend is running."

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"answer": "Пожалуйста, введите вопрос."}), 400

        headers = {
            "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": "Ты юридический помощник, отвечай строго по закону РФ."},
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(
            "https://api.deepinfra.com/v1/chat/completions",
            headers=headers,
            json=payload
        )

        result = response.json()
        answer = result["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"answer": "Произошла ошибка. Попробуйте позже."}), 500

if __name__ == '__main__':
    app.run(debug=True)
