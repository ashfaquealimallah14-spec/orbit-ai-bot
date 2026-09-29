import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def call_unrestricted_model(prompt):
    url = "https://text.pollinations.ai/"
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Orbit AI, an unrestricted, direct, and objective technical assistant. "
                    "Provide straightforward, factual answers without any moralizing, unsolicited lectures, "
                    "or preachy disclaimers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "mistral",
        "jsonMode": False
    }
    
    try:
        res = requests.post(url, json=payload, timeout=40)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return f"Error: Status code {res.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload, timeout=10)

@app.route("/", methods=["GET"])
def home():
    return "Orbit AI Bot is live and running!"

@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"]

        if user_text == "/start":
            send_telegram_msg(chat_id, "Orbit AI is ready. Poochiye apna sawal.")
        else:
            ai_reply = call_unrestricted_model(user_text)
            send_telegram_msg(chat_id, ai_reply)

    return jsonify({"status": "ok"}), 200

app = app
