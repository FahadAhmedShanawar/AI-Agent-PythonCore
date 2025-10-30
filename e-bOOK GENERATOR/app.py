import os
import json
import requests
from flask import Flask, request, render_template_string, flash, redirect, url_for
from openai import OpenAI
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import time
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# HTML template for the form
FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Book Generator</title>
</head>
<body>
    <h1>Generate Your AI E-Book</h1>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    <form method="POST">
        <label>Email: <input type="email" name="email" required></label><br>
        <label>First Name: <input type="text" name="first_name" required></label><br>
        <label>Last Name: <input type="text" name="last_name" required></label><br>
        <label>Title: <input type="text" name="title" required></label><br>
        <label>Description: <textarea name="description" required></textarea></label><br>
        <label>Target Audience: <input type="text" name="audience" required></label><br>
        <label>Tone of Voice: <input type="text" name="tone" required></label><br>
        <label>Number of Chapters (1-10): <input type="number" name="num_chapters" min="1" max="10" required></label><br>
        <label>Reading Level: <input type="text" name="reading_level" required></label><br>
        <input type="submit" value="Generate E-Book" id="submit-btn">
    </form>
    <script>
        document.querySelector('form').addEventListener('submit', function() {
            document.getElementById('submit-btn').value = 'Generating E-Book... Please wait.';
            document.getElementById('submit-btn').disabled = true;
        });
    </script>
</body>
</html>
"""

def generate_outline(title, description, tone, audience, num_chapters, reading_level):
    system_message = {
        "role": "system",
        "content": """You are an assistant that MUST output only valid JSON. The JSON schema must exactly match the "Outline Schema" described below. Do not output any text before or after the JSON. If the model attempts commentary, return an error. Use the user inputs to create chapter titles and short descriptions. Include an "intro" chapter and a "conclusion" chapter automatically, so the total number of chapters returned equals the requested number plus intro/conclusion. Use concise human-readable titles."""
    }
    user_message = {
        "role": "user",
        "content": f"""Create an ebook outline as a JSON object following this schema:

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
- Title: {title}
- Description: {description}
- Tone: {tone}
- Target Audience: {audience}
- Number of chapters (excluding intro & conclusion): {num_chapters}
- Reading level: {reading_level}

Requirements:
- Exactly ({num_chapters} + 2) items inside "chapters": first is intro (chapter_number 0), last is conclusion (chapter_number {num_chapters}+1). Intermediate chapter_number values must be 1..{num_chapters}.
- Each chapter_description should be 12–30 words, bullet-style content hints separated by commas.
- Output only the JSON object—no explanation."""
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message, user_message],
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSONzf
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Failed to parse outline JSON")

def generate_image(chapter_title, chapter_desc):
    prompt = f"Create a high-quality, photorealistic digital painting for an ebook chapter: Chapter Title: {chapter_title}, Chapter Description: {chapter_desc}. Aspect Ratio: square (1:1). Guidance: DO NOT include any text, digits, logos, or watermarks on the image. Focus on the main subject(s) described in the chapter_description. Compose with a clear focal point and generous negative space for captions."
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url

def generate_chapter_text(chapter_number, chapter_title, chapter_desc, tone, audience, reading_level):
    system_message = {
        "role": "system",
        "content": """You are generating content that will be embedded directly into an HTML page. Output MUST contain exactly the HTML fragment for the chapter body with these constraints:
- Top-level heading for the chapter: <h2>Chapter {CHAPTER_NUMBER}: {CHAPTER_TITLE}</h2>
- Immediately after H2, insert two image placeholders (these will be replaced by actual image URLs). Use placeholders: [[IMG1]] and [[IMG2]].
- After images, include the chapter text inside <div class="chapter-text"> ... </div>.
- Use subheadings (<h3>) for 2–4 subsections.
f- Each subsection should have 1–3 short paragraphs.
- No extra surrounding HTML (no <html>, <body>, <head>).
- Do not include inline styles; keep semantic tags only.
- Do not include commentary, "note", or meta language outside the HTML."""
    }
    user_message = {
        "role": "user",
        "content": f"""Generate the HTML fragment for chapter {chapter_number} with title "{chapter_title}" and description "{chapter_desc}".
Tone: {tone}
Audience: {audience}
Reading level: {reading_level}
Include examples, a one-line actionable takeaway at the end inside <p class="takeaway">.
Remember to place the image placeholders [[IMG1]] and [[IMG2]] immediately below the <h2> and before the main content."""
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[system_message, user_message],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def aggregate_html(title, description, chapter_html_blocks):
    title_block = f"<h1>{title}</h1>\n<p>{description}</p>\n\n"
    body = "\n\n".join(chapter_html_blocks)
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; margin-top: 40px; }}
        img {{ max-width: 100%; height: auto; margin: 10px 0; }}
        .chapter-text {{ margin-bottom: 20px; }}
        .takeaway {{ font-weight: bold; }}
    </style>
</head>
<body>
{title_block}{body}
</body>
</html>"""
    return full_html

def generate_pdf(html_content, filename):
    from bs4 import BeautifulSoup
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.units import inch
    import requests
    from io import BytesIO

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, spaceAfter=30)
    heading2_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=18, spaceAfter=20)
    heading3_style = ParagraphStyle('Heading3', parent=styles['Heading3'], fontSize=14, spaceAfter=15)
    normal_style = styles['Normal']
    takeaway_style = ParagraphStyle('Takeaway', parent=styles['Normal'], fontName='Helvetica-Bold')

    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img', 'div']):
        if element.name == 'h1':
            story.append(Paragraph(element.get_text(), title_style))
            story.append(Spacer(1, 12))
        elif element.name == 'h2':
            story.append(Paragraph(element.get_text(), heading2_style))
            story.append(Spacer(1, 12))
        elif element.name == 'h3':
            story.append(Paragraph(element.get_text(), heading3_style))
            story.append(Spacer(1, 12))
        elif element.name == 'p':
            if 'takeaway' in element.get('class', []):
                story.append(Paragraph(element.get_text(), takeaway_style))
            else:
                story.append(Paragraph(element.get_text(), normal_style))
            story.append(Spacer(1, 6))
        elif element.name == 'img':
            img_src = element.get('src')
            if img_src:
                try:
                    # Check if it's a local file or URL
                    if img_src.startswith('http'):
                        response = requests.get(img_src)
                        img_data = BytesIO(response.content)
                        img = Image(img_data, width=4*inch, height=4*inch)
                    else:
                        # Local file
                        img = Image(img_src, width=4*inch, height=4*inch)
                    story.append(img)
                    story.append(Spacer(1, 12))
                except Exception as e:
                    print(f"Failed to load image {img_src}: {e}")
        elif element.name == 'div' and 'chapter-text' in element.get('class', []):
            for p in element.find_all('p'):
                if 'takeaway' in p.get('class', []):
                    story.append(Paragraph(p.get_text(), takeaway_style))
                else:
                    story.append(Paragraph(p.get_text(), normal_style))
                story.append(Spacer(1, 6))

    doc.build(story)
    print(f"PDF generated: {filename}")

def send_email(to_email, first_name, title, pdf_path):
    from_email = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Your E-Book: {title}"
    body = f"Hi {first_name},\n\nYour e-book '{title}' is attached.\n\nBest regards,\nE-Book Generator"
    msg.attach(MIMEText(body, 'plain'))
    with open(pdf_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(pdf_path)}")
        msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_payload = {
            'email': request.form['email'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'title': request.form['title'],
            'description': request.form['description'],
            'audience': request.form['audience'],
            'tone': request.form['tone'],
            'num_chapters': int(request.form['num_chapters']),
            'reading_level': request.form['reading_level']
        }
        try:
            # Generate outline
            outline = generate_outline(
                title=form_payload['title'],
                description=form_payload['description'],
                tone=form_payload['tone'],
                audience=form_payload['audience'],
                num_chapters=form_payload['num_chapters'],
                reading_level=form_payload['reading_level']
            )
            chapters = outline['chapters']
            chapter_html_blocks = []
            image_files = []  # To keep track of local image files for cleanup
            for chapter in chapters:
                # Generate images
                img1_url = generate_image(chapter['chapter_title'], chapter['chapter_description'])
                img2_url = generate_image(chapter['chapter_title'] + " alternate version", chapter['chapter_description'])

                # Download images locally to avoid URL expiration
                img1_local = f"img_{chapter['chapter_number']}_1.jpg"
                img2_local = f"img_{chapter['chapter_number']}_2.jpg"
                try:
                    response1 = requests.get(img1_url)
                    with open(img1_local, 'wb') as f:
                        f.write(response1.content)
                    image_files.append(img1_local)
                except Exception as e:
                    print(f"Failed to download image 1 for chapter {chapter['chapter_number']}: {e}")
                    img1_local = None

                try:
                    response2 = requests.get(img2_url)
                    with open(img2_local, 'wb') as f:
                        f.write(response2.content)
                    image_files.append(img2_local)
                except Exception as e:
                    print(f"Failed to download image 2 for chapter {chapter['chapter_number']}: {e}")
                    img2_local = None

                # Generate text
                html_fragment = generate_chapter_text(chapter['chapter_number'], chapter['chapter_title'], chapter['chapter_description'], form_payload['tone'], form_payload['audience'], form_payload['reading_level'])
                # Replace placeholders with local paths
                img1_tag = f'<img src="{img1_local}" alt="{chapter["chapter_title"]} Image 1">' if img1_local else ''
                img2_tag = f'<img src="{img2_local}" alt="{chapter["chapter_title"]} Image 2">' if img2_local else ''
                html_fragment = html_fragment.replace('[[IMG1]]', img1_tag)
                html_fragment = html_fragment.replace('[[IMG2]]', img2_tag)
                chapter_html_blocks.append(html_fragment)
                time.sleep(1)  # Rate limit
            # Aggregate
            full_html = aggregate_html(form_payload['title'], form_payload['description'], chapter_html_blocks)
            # Generate PDF
            pdf_filename = f"{form_payload['title'].replace(' ', '_')}_{int(time.time())}.pdf"
            generate_pdf(full_html, pdf_filename)
            # Clean up local image files
            for img_file in image_files:
                try:
                    os.remove(img_file)
                except OSError:
                    pass
            # Send email
            send_email(form_payload['email'], form_payload['first_name'], form_payload['title'], pdf_filename)
            flash('E-Book generated and emailed successfully!')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('index'))
    return render_template_string(FORM_HTML)

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    if not data:
        return {'error': 'No data provided'}, 400
    form_payload = {
        'email': data.get('Email'),
        'first_name': data.get('First Name'),
        'last_name': data.get('Last Name'),
        'title': data.get('Title'),
        'description': data.get('Description'),
        'audience': data.get('Target Audience'),
        'tone': data.get('Tone of Voice'),
        'num_chapters': int(data.get('Number of Chapters (1-10)', 1)),
        'reading_level': data.get('Reading Level')
    }
    try:
        # Generate outline
        outline = generate_outline(
            title=form_payload['title'],
            description=form_payload['description'],
            tone=form_payload['tone'],
            audience=form_payload['audience'],
            num_chapters=form_payload['num_chapters'],
            reading_level=form_payload['reading_level']
        )
        chapters = outline['chapters']
        chapter_html_blocks = []
        image_files = []  # To keep track of local image files for cleanup
        for chapter in chapters:
            # Generate images
            img1_url = generate_image(chapter['chapter_title'], chapter['chapter_description'])
            img2_url = generate_image(chapter['chapter_title'] + " alternate version", chapter['chapter_description'])

            # Download images locally to avoid URL expiration
            img1_local = f"img_{chapter['chapter_number']}_1.jpg"
            img2_local = f"img_{chapter['chapter_number']}_2.jpg"
            try:
                response1 = requests.get(img1_url)
                with open(img1_local, 'wb') as f:
                    f.write(response1.content)
                image_files.append(img1_local)
            except Exception as e:
                print(f"Failed to download image 1 for chapter {chapter['chapter_number']}: {e}")
                img1_local = None

            try:
                response2 = requests.get(img2_url)
                with open(img2_local, 'wb') as f:
                    f.write(response2.content)
                image_files.append(img2_local)
            except Exception as e:
                print(f"Failed to download image 2 for chapter {chapter['chapter_number']}: {e}")
                img2_local = None

            # Generate text
            html_fragment = generate_chapter_text(chapter['chapter_number'], chapter['chapter_title'], chapter['chapter_description'], form_payload['tone'], form_payload['audience'], form_payload['reading_level'])
            # Replace placeholders with local paths
            img1_tag = f'<img src="{img1_local}" alt="{chapter["chapter_title"]} Image 1">' if img1_local else ''
            img2_tag = f'<img src="{img2_local}" alt="{chapter["chapter_title"]} Image 2">' if img2_local else ''
            html_fragment = html_fragment.replace('[[IMG1]]', img1_tag)
            html_fragment = html_fragment.replace('[[IMG2]]', img2_tag)
            chapter_html_blocks.append(html_fragment)
            time.sleep(1)  # Rate limit
        # Aggregate
        full_html = aggregate_html(form_payload['title'], form_payload['description'], chapter_html_blocks)
        # Generate PDF
        pdf_filename = f"{form_payload['title'].replace(' ', '_')}_{int(time.time())}.pdf"
        generate_pdf(full_html, pdf_filename)
        # Clean up local image files
        for img_file in image_files:
            try:
                os.remove(img_file)
            except OSError:
                pass
        # Send email
        send_email(form_payload['email'], form_payload['first_name'], form_payload['title'], pdf_filename)
        return {'status': 'E-Book generated and emailed successfully!'}, 200
    except Exception as e:
        print(f'Error: {str(e)}')
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
