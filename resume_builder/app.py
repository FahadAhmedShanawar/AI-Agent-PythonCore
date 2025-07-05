import os
import json
import cohere
import gradio as gr
import pdfkit
import base64
from io import BytesIO
from PIL import Image
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

# ---------------- Load environment variables ----------------
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH", r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# ---------------- Validate environment ----------------
if not cohere_api_key:
    raise ValueError("⚠️ COHERE_API_KEY is missing in your .env file!")

if not os.path.exists(wkhtmltopdf_path):
    raise FileNotFoundError(f"⚠️ wkhtmltopdf not found at: {wkhtmltopdf_path}")

# ---------------- Initialize Cohere & PDF config ----------------
co = cohere.Client(cohere_api_key)
pdf_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

pdf_options = {
    'page-size': 'A4',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'encoding': "UTF-8",
    'enable-local-file-access': '',
    'print-media-type': '',
    'quiet': ''
}

# ---------------- Setup Jinja2 Template Engine ----------------
templates_path = "templates"
if not os.path.exists(templates_path):
    raise FileNotFoundError("⚠️ 'templates' folder not found!")

env = Environment(loader=FileSystemLoader(templates_path))

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# ---------------- Utility: Convert image to base64 ----------------
def image_to_base64(img_array):
    if img_array is None:
        return ""
    image = Image.fromarray(img_array.astype("uint8"))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

# ---------------- AI: Generate Summary and Skills ----------------
def generate_summary_and_skills(name, job_description):
    summary_prompt = f"Write a professional summary (2-3 lines) for {name} based on this job description:\n{job_description}"
    skills_prompt = f"List 5 relevant skills for this job:\n{job_description}"

    summary = co.generate(prompt=summary_prompt, max_tokens=150).generations[0].text.strip()
    skills_raw = co.generate(prompt=skills_prompt, max_tokens=60).generations[0].text.strip()
    skills = [s.strip() for s in skills_raw.replace("\n", ",").split(",") if s.strip()]

    return summary, skills

# ---------------- Core: Resume Builder ----------------
def build_resume(full_name, email, phone, address,
                 education, experience, job_description,
                 languages, references, resume_title,
                 template_name, profile_image_array):
    try:
        # Parse input strings
        education_list = json.loads(education)
        experience_list = json.loads(experience)
        references_list = json.loads(references)
        language_list = [lang.strip() for lang in languages.split(",") if lang.strip()]

        # Generate dynamic content using AI
        summary, skills = generate_summary_and_skills(full_name, job_description)
        profile_image_data = image_to_base64(profile_image_array)

        # Load template and render HTML
        template = env.get_template(template_name)
        html_content = template.render(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            education=education_list,
            experience=experience_list,
            references=references_list,
            languages=language_list,
            resume_title=resume_title,
            summary=summary,
            skills=skills,
            profile_image=profile_image_data
        )

        # Save files
        html_path = os.path.join(output_dir, "resume.html")
        pdf_path = os.path.join(output_dir, "resume.pdf")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        pdfkit.from_file(html_path, pdf_path, configuration=pdf_config, options=pdf_options)

        return html_path, pdf_path

    except json.JSONDecodeError:
        return "❌ Invalid JSON in education, experience, or references.", None
    except Exception as e:
        return f"❌ Error: {str(e)}", None

# ---------------- Gradio Interface ----------------
demo = gr.Interface(
    fn=build_resume,
    inputs=[
        gr.Textbox(label="Full Name"),
        gr.Textbox(label="Email"),
        gr.Textbox(label="Phone"),
        gr.Textbox(label="Address"),
        gr.Textbox(label="Education (JSON list)", lines=4, placeholder='[{"degree": "BS CS", "institution": "ABC University", "year": "2023"}]'),
        gr.Textbox(label="Experience (JSON list)", lines=4, placeholder='[{"title": "Developer", "company": "XYZ Inc", "duration": "2022–2024"}]'),
        gr.Textbox(label="Job Description", lines=4),
        gr.Textbox(label="Languages (comma-separated)", placeholder="English, Urdu"),
        gr.Textbox(label="References (JSON list)", lines=3, placeholder='[{"name": "John Doe", "contact": "john@example.com"}]'),
        gr.Textbox(label="Resume Title", placeholder="Software Engineer Resume"),
        gr.Dropdown(choices=os.listdir(templates_path), label="Select Template"),
        gr.Image(type="numpy", label="Upload Profile Image (optional)")
    ],
    outputs=[
        gr.File(label="📄 Download HTML Resume"),
        gr.File(label="📄 Download PDF Resume")
    ],
    title="🧠 AI Resume Builder",
    description="Create a professional resume using AI. Upload your profile picture and get PDF + HTML formats."
)

# ---------------- Launch Gradio App ----------------
if __name__ == "__main__":
    demo.launch()
