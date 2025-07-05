from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# ====== Gemini API Call Function ======
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "⚠️ No proper response.")
    except Exception as e:
        return f"⚠️ Error while calling Gemini: {str(e)}"

# ====== Word-Wrapping Function for Neat Display ======
def clean_wrap(text, width=10):
    words = text.split()
    lines, line = [], []
    for word in words:
        line.append(word)
        if len(line) >= width or word.endswith(('.', '!', '؟', '۔', '?')):
            lines.append(' '.join(line))
            line = []
    if line:
        lines.append(' '.join(line))
    return '\n'.join(lines)

# ====== Home Route ======
@app.route("/")
def home():
    return render_template("index.html")

# ====== Main Processing Route ======
@app.route("/process", methods=["POST"])
def process():
    user_msg = request.form.get("message", "").strip()
    user_reply = request.form.get("reply", "").strip()
    keypoints = request.form.get("keypoints", "").strip()
    action = request.form.get("action", "").strip()

    if not user_msg:
        return jsonify({"title": "❗ Error", "content": "User message is required."})

    # Prepare the message context
    context = f"Message:\n{user_msg}"
    if user_reply:
        context += f"\n\nUser Reply:\n{user_reply}"
    if keypoints:
        context += f"\n\nKey Points:\n{keypoints}"

    # Generate prompt based on selected action
    if action == "correction":
        prompt = (
            "Please make the following message polite, clear, and respectful:\n\n"
            f"{context}"
        )

    elif action == "simple_en":
        prompt = (
            "Kindly rewrite the following in simple, polite, and respectful English:\n\n"
            f"{context}"
        )

    elif action == "simple_ur":
        prompt = (
            "براہ کرم نیچے دیے گئے پیغام کو سادہ، باادب اور محبت بھرے اردو انداز میں لکھیے:\n\n"
            f"{context}"
        )

    elif action == "emoji_en":
        prompt = (
            "Please rewrite this for a friend in a friendly, funny, and cute tone. "
            "Start with light-hearted greetings like 'Hey! How are you?', 'What's up?', or 'Kya haal hai?'. "
            "Keep the tone sweet and respectful. Make the conversation slightly longer and playful. "
            "Add friendly and respectful emojis like 🌸😊✨🙏 where appropriate:\n\n"
            f"{context}"
        )

    elif action == "emoji_ur":
        prompt = (
            "براہ کرم نیچے دیے گئے پیغام کو اردو میں دوستانہ، باادب اور محبت بھرے انداز میں لکھیے۔ "
            "ابتداء میں ہلکی پھلکی باتیں شامل کیجیے جیسے: 'کیا حال ہے؟'، 'کیا کر رہے ہو؟' وغیرہ۔ "
            "یہ پیغام خاندان کے افراد یا 25 سے 35 سال کے عمر والے قریبی دوستوں کے لیے ہو، لہٰذا مختصر، مہذب اور عزت دار انداز اپنائیں۔ "
            "عامیانہ زبان سے پرہیز کریں اور موزوں ایموجیز جیسے 🌷🤲💖☺️ استعمال کریں:\n\n"
            f"{context}"
        )

    elif action == "elder_reply":
        prompt = (
            "Please rewrite the following message in a short, formal, polite, and respectful tone "
            "suitable for elders (e.g., a teacher or uncle). Start with respectful phrases like 'Kindly', 'Please', or 'Let me know'. "
            "Avoid casual or informal language. End with a gratitude statement like: "
            "'Thanks for your kindness', 'I am very thankful', or 'I am truly grateful'.\n\n"
            f"{context}"
        )

    else:
        return jsonify({"title": "❗ Error", "content": "Invalid action selected."})

    # Call Gemini API
    result = call_gemini(prompt)
    wrapped_result = clean_wrap(result, width=10)

    # Return response
    return jsonify({"title": "✅ Result", "content": wrapped_result})

# ====== Run App ======
if __name__ == "__main__":
    app.run(debug=True)
