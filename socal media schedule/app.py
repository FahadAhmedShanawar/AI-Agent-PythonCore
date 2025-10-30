from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from scheduler import start_scheduler, load_posts, save_posts

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key_here'  # Change this in production

scheduler = start_scheduler()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/schedule', methods=['POST'])
def schedule_post():
    text = request.form.get('text')
    platform = request.form.get('platform')
    hashtags = request.form.get('hashtags')
    scheduled_time = request.form.get('scheduled_time')

    if not text or not platform or not scheduled_time:
        flash('Please fill in all required fields.')
        return redirect(url_for('index'))

    # Parse hashtags
    hashtags_list = [h.strip() for h in hashtags.split(',')] if hashtags else []

    # Handle image upload
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = f"static/uploads/{filename}"

    # Create post dict
    post = {
        'id': str(datetime.now().timestamp()),
        'text': text,
        'platform': platform,
        'hashtags': hashtags_list,
        'scheduled_time': scheduled_time,
        'image_path': image_path,
        'created_at': datetime.now().isoformat()
    }

    # Save to JSON
    posts = load_posts()
    posts.append(post)
    save_posts(posts)

    flash('Post scheduled successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    flash('Post deleted.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
