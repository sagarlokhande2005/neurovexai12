from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

# --------------------------
# Initialize Flask app
# --------------------------
app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# --------------------------
# OpenRouter API config
# --------------------------
OPENROUTER_API_KEY = "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"  # <-- Replace with your key
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "gpt-4o-mini"  # Change to your desired model

# --------------------------
# Home route (serve index.html)
# --------------------------
@app.route("/")
def home():
    return render_template("index.html")  # Make sure index.html is in templates/

# --------------------------
# Chat API route
# --------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip().lower()  # lowercase for easy matching

        if not user_message:
            return jsonify({"reply": "Please send a valid message."})

        # -----------------------
        # Developer/Owner Keywords
        # -----------------------
        developer_keywords = [
            "who developed", "who made", "who created",
            "who is your owner", "who is your maker"
        ]

        for keyword in developer_keywords:
            if keyword in user_message:
                return jsonify({"reply": "I was developed by Sagar Lokhande 🤖"})

        # -----------------------
        # AI Name / Identity Keywords
        # -----------------------
        ai_name_keywords = [
            "who are you", "what is your name", "who is this ai",
            "who are you related", "your name"
        ]

        for keyword in ai_name_keywords:
            if keyword in user_message:
                return jsonify({"reply": "I am Neurovex AI 🤖"})

        # -----------------------
        # Otherwise, call OpenRouter API
        # -----------------------
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": user_message}]
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        reply = response_data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except requests.exceptions.HTTPError as http_err:
        print("HTTP error:", http_err, response.text)
        return jsonify({"reply": "HTTP error occurred. Check your API key or model."}), 500
    except Exception as e:
        print("Other error:", e)
        return jsonify({"reply": "Something went wrong with OpenRouter API."}), 500

# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    app.run()