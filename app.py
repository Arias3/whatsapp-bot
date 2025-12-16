from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_ID = os.environ["PHONE_NUMBER_ID"]

def send_message(to, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    entry = data["entry"][0]["changes"][0]["value"]
    messages = entry.get("messages")

    if messages:
        msg = messages[0]
        phone = msg["from"]
        text = msg["text"]["body"].lower()

        send_message(phone, "Hola 👋 Ya estoy funcionando.")
    return "ok", 200
