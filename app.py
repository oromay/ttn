import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- HARDCODED TOKENS (Added per your request) ---

# -------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return "Telegram-Notion Bot is active!", 200

# We use the token directly in the route URL
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    
    # Check if the update contains a text message
    if "message" in update and "text" in update["message"]:
        text = update["message"]["text"]
        send_to_notion(text)
        
    return jsonify({"status": "ok"}), 200

def send_to_notion(text):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": { # Assumes your title column in Notion is named 'Name'
                "title": [
                    {
                        "text": {
                            "content": text
                        }
                    }
                ]
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
