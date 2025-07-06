import random
import numpy as np
import pandas as pd
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
from transformers import pipeline

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

sentiment_analyzer = pipeline("sentiment-analysis")

QUESTIONS = {
    "SEO Expert": [
        "How do you approach keyword research?",
        "What is the importance of backlinks?",
        "How do you measure SEO success?",
        "Explain technical SEO.",
        "What are meta tags and why are they important?",
        "How do you optimize for mobile search?",
        "Explain schema markup.",
        "How do you stay updated with Google algorithm updates?",
        "What tools do you use for SEO audits?",
        "How do you handle duplicate content?",
        "Explain canonical URLs.",
        "How do you improve website load speed?",
        "What is local SEO?",
        "Describe your link-building strategy.",
        "How do you perform competitor analysis?"
    ],
    "Web Developer": [
        "What is MVC architecture in Laravel?",
        "How do you prevent SQL injection?",
        "Explain responsive web design.",
        "What is AJAX?",
        "How do you debug JavaScript?",
        "Explain CSS Flexbox.",
        "How do you manage sessions in PHP?",
        "What are migrations in Laravel?",
        "Explain REST APIs.",
        "How do you optimize web performance?",
        "What is CSRF protection?",
        "How do you use Bootstrap Grid?",
        "Explain Eloquent ORM.",
        "How do you deploy a Laravel project?",
        "What is version control, and why is it important?"
    ],
    "Data Analyst": [
        "How do you clean and preprocess data?",
        "Explain exploratory data analysis.",
        "How do you handle missing values?",
        "Explain the use of Pandas library.",
        "What is data visualization?",
        "How do you create dashboards in Power BI?",
        "Explain data normalization.",
        "What is a pivot table?",
        "How do you detect outliers?",
        "How do you use SQL for analysis?",
        "What is the role of NumPy?",
        "Explain the difference between variance and standard deviation.",
        "How do you present findings to stakeholders?",
        "Explain data aggregation.",
        "Describe your experience with Seaborn."
    ],
    "Machine Learning Engineer": [
        "What is overfitting?",
        "Explain the bias-variance tradeoff.",
        "How do you handle imbalanced datasets?",
        "Describe cross-validation.",
        "Explain supervised learning.",
        "What is feature engineering?",
        "How do you tune hyperparameters?",
        "Explain ensemble methods.",
        "What is PCA?",
        "How do you evaluate model performance?",
        "Explain classification vs regression.",
        "Describe a machine learning project you built.",
        "What is ROC curve?",
        "How do you deploy ML models?",
        "What is scikit-learn?"
    ],
    "Facebook Ads Specialist": [
        "How do you set up a Facebook campaign?",
        "What are Custom Audiences?",
        "Explain Lookalike Audiences.",
        "How do you measure ROI?",
        "What bidding strategies have you used?",
        "How do you optimize ad creatives?",
        "How do you retarget website visitors?",
        "Explain Facebook Pixel.",
        "Describe your approach to A/B testing.",
        "How do you scale successful campaigns?",
        "What metrics do you track?",
        "How do you budget for campaigns?",
        "Explain Dynamic Ads.",
        "How do you stay updated with Facebook Ads changes?",
        "How do you report campaign performance?"
    ],
    "Google/YouTube Ads Specialist": [
        "Explain Quality Score.",
        "How do you conduct keyword research?",
        "Describe campaign structure.",
        "What bidding strategies do you use?",
        "How do you optimize ads for conversions?",
        "Explain ad extensions.",
        "How do you measure ad performance?",
        "What is Smart Bidding?",
        "How do you retarget users?",
        "How do you set up YouTube ads?",
        "Describe your approach to video ads.",
        "How do you improve CTR?",
        "What is negative keyword targeting?",
        "How do you use Google Analytics with Ads?",
        "How do you report results to clients?"
    ],
    "AI Agent Developer": [
        "How do you integrate LLMs into apps?",
        "Describe prompt engineering.",
        "How do you design Streamlit apps?",
        "What experience do you have with n8n?",
        "Explain JSON APIs.",
        "How do you manage API rate limits?",
        "What is tokenization?",
        "How do you secure API keys?",
        "How do you deploy an AI agent?",
        "What is caching and why is it important?",
        "How do you handle large responses?",
        "How do you monitor usage?",
        "How do you manage errors?",
        "Describe an AI project you built.",
        "How do you customize LLM outputs?"
    ]
}

@app.route("/")
def index():
    return render_template("index.html", roles=list(QUESTIONS.keys()))

@app.route("/start_interview", methods=["POST"])
def start_interview():
    data = request.json
    role = data.get("role")
    num_questions = int(data.get("num_questions", 5))
    selected_questions = QUESTIONS.get(role, [])
    random.shuffle(selected_questions)
    questions = selected_questions[:num_questions]
    return jsonify({"questions": questions})

@app.route("/analyze_responses", methods=["POST"])
def analyze_responses():
    data = request.json
    responses = data.get("responses", [])

    if not responses:
        return jsonify({"error": "I didn’t receive any answers. Could you please try again?"}), 400

    all_texts = [r["answer"] for r in responses]

    # Sentiment ratings
    sentiments = sentiment_analyzer(all_texts)
    ratings = [round(s["score"] * 10) for s in sentiments]

    # Cohere classification
    try:
        cohere_resp = requests.post(
            "https://api.cohere.ai/v1/classify",
            headers={"Authorization": f"Bearer {COHERE_API_KEY}"},
            json={
                "inputs": all_texts,
                "examples": [
                    {"text": "I feel confident about this.", "label": "good"},
                    {"text": "I'm unsure about this.", "label": "needs improvement"}
                ]
            }
        )
        cohere_resp.raise_for_status()
        cohere_labels = [c["prediction"] for c in cohere_resp.json().get("classifications", [])]
    except Exception:
        cohere_labels = ["neutral"] * len(responses)

    # Gemini feedback
    combined_text = "\n\n".join(
        f"Q: {r['question']}\nA: {r['answer']}" for r in responses
    )
    try:
        gemini_payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "Please write a friendly, conversational summary and some suggestions. "
                                "Be natural, as if you're casually giving tips.\n\n" + combined_text
                            )
                        }
                    ]
                }
            ]
        }
        gemini_resp = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent",
            headers={
                "Content-Type": "application/json",
                "X-goog-api-key": GEMINI_API_KEY
            },
            json=gemini_payload
        )
        gemini_resp.raise_for_status()
        raw_feedback = gemini_resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raw_feedback = (
            "I wasn’t able to gather detailed notes this time, but overall you did a thoughtful job. "
            "Keep practicing, and feel free to revisit these questions anytime."
        )

    # Occasionally add personal encouragement
    if random.random() < 0.3:
        raw_feedback += "\n\nBy the way, it's completely normal to have mixed feelings—you're doing better than you think!"

    avg_rating = sum(ratings) / len(ratings) if ratings else 5.0
    overall_label = max(set(cohere_labels), key=cohere_labels.count)

    return jsonify({
        "average_rating": round(avg_rating, 1),
        "overall_label": overall_label,
        "gemini_feedback": raw_feedback
    })

if __name__ == "__main__":
    app.run(debug=True)
