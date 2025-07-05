from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY is missing in .env")

# Initialize Cohere client
co = cohere.Client(api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    topic = data.get('topic', '').strip()
    primary_keyword = data.get('primary_keyword', '').strip()
    keywords = data.get('keywords', '').strip()
    tone = data.get('tone', 'Professional')
    length_choice = data.get('length', '500-word SEO content')
    mode = data.get('mode', 'Blog & Article')

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    length_map = {
        "300-word catchy content": 300,
        "500-word SEO content": 500,
        "Blog & Article (1200–1500 words)": 1400
    }

    max_words = length_map.get(length_choice, 700)
    max_tokens = int(max_words * 1.3)

    if mode == "Blog & Article":
        prompt = f"""
Write a professional SEO-, AEO-, and VSO-optimized blog of {max_words} words about "{topic}".

✅ Use the primary keyword "{primary_keyword}" and secondary keywords: {keywords}.
✅ Requirements:
- <h1> main title (bold)
- Bold <h2> sections
- Bold <h3> sub-sections
- Table of Contents with 5–6 points
- 4 FAQs before the conclusion
- Primary keyword density 4–5%
- Use the primary keyword every ~100 words
- Conversational, human-like tone with transactional intent

✅ Meta:
- 3–5 title tags under 55 characters, include the primary keyword and CTA
- 3–5 meta descriptions under 150 characters, include the primary keyword and CTA

Return clean, well-formatted HTML content.
"""
    elif mode == "Product Description":
        prompt = f"""
Write a product description under 80 words about "{topic}".
✅ Format:
- Start with a powerful hook
- Use bullet points or short sentences
- Include 1–2 unique selling points
- Strong CTA
- Mobile-friendly style
"""
    elif mode == "300-word catchy content":
        prompt = f"""
Write a 300-word catchy content piece about "{topic}".
✅ Use a hook, emotional appeal, short sentences, and a strong CTA.
✅ Conversational and engaging style.
"""
    elif mode == "500-word SEO content":
        prompt = f"""
Write a 500-word SEO-, AIO-, AEO-optimized article about "{topic}".
✅ Use the primary keyword "{primary_keyword}" and secondary keywords: {keywords}.
✅ Requirements:
- Subheadings every ~100 words
- Primary keyword used 10+ times (aiming for 4–5% density)
- Clear CTA at the end
- Conversational, human tone
"""
    else:
        return jsonify({"error": "Invalid mode selected."}), 400

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=min(max_tokens, 2000),
            temperature=0.7
        )
        content = response.generations[0].text.strip()
        return jsonify({"content": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
