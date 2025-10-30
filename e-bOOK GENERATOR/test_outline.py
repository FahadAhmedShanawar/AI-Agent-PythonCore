import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Test outline generation
form_payload = {
    'title': 'Test E-Book',
    'description': 'A test e-book about AI.',
    'tone': 'Professional',
    'audience': 'Developers',
    'num_chapters': 2,
    'reading_level': 'Intermediate'
}

system_message = {
    'role': 'system',
    'content': 'You are an assistant that MUST output only valid JSON. The JSON schema must exactly match the "Outline Schema" described below. Do not output any text before or after the JSON. If the model attempts commentary, return an error. Use the user inputs to create chapter titles and short descriptions. Include an "intro" chapter and a "conclusion" chapter automatically, so the total number of chapters returned equals the requested number plus intro/conclusion. Use concise human-readable titles.'
}
user_message = {
    'role': 'user',
    'content': f'''Create an ebook outline as a JSON object following this schema:

Outline Schema:
{{
  "title": "<ebook title>",
  "description": "<ebook short description>",
  "tone": "<tone of voice provided>",
  "audience": "<target audience>",
  "reading_level": "<reading level>",
  "chapters": [
    {{
      "chapter_number": 0,
      "chapter_type": "intro",
      "chapter_title": "Introduction",
      "chapter_description": "<short description of this chapter>"
    }},
    {{
      "chapter_number": 1,
      "chapter_type": "chapter",
      "chapter_title": "<Chapter 1 title>",
      "chapter_description": "<one-line description / bullet topics>"
    }},
    ...
    {{
      "chapter_number": N,
      "chapter_type": "conclusion",
      "chapter_title": "Conclusion",
      "chapter_description": "<one-line summary + call-to-action>"
    }}
  ]
}}

Use the inputs:
- Title: {form_payload['title']}
- Description: {form_payload['description']}
- Tone: {form_payload['tone']}
- Target Audience: {form_payload['audience']}
- Number of chapters (excluding intro & conclusion): {form_payload['num_chapters']}
- Reading level: {form_payload['reading_level']}

Requirements:
- Exactly ({form_payload['num_chapters']} + 2) items inside "chapters": first is intro (chapter_number 0), last is conclusion (chapter_number {form_payload['num_chapters']}+1). Intermediate chapter_number values must be 1..{form_payload['num_chapters']}.
- Each chapter_description should be 12–30 words, bullet-style content hints separated by commas.
- Output only the JSON object—no explanation.'''
}

try:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[system_message, user_message],
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    print('Raw response:', content)
    outline = json.loads(content)
    print('Outline generated successfully:')
    print(json.dumps(outline, indent=2))
except Exception as e:
    print(f'Error: {e}')
