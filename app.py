from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename
from datetime import datetime
from io import BytesIO
from PIL import Image
import os, base64

app = Flask(__name__)
app.secret_key = "sahil_secret_key_2025"  # Session use karne ke liye

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Folder create if not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Limit text function
def limit_text(text, limit):
    return text[:limit] if text else ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        photo_filename = None
        photo_data = request.form.get('photo_data')

        # 🔁 If user already uploaded/cropped, reuse
        if not photo_data and 'last_photo' in session:
            photo_filename = session['last_photo']

        elif photo_data and "base64" in photo_data:
            try:
                header, encoded = photo_data.split(",", 1)
                image_data = base64.b64decode(encoded)

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                photo_filename = f"cropped_{timestamp}.png"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)

                image = Image.open(BytesIO(image_data)).convert("RGB")
                image.save(photo_path, format="PNG")

                session['last_photo'] = photo_filename  # 🧠 Save to session

            except Exception as e:
                print("❌ Error cropping image:", e)

        elif 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                photo_filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)
                session['last_photo'] = photo_filename  # 🧠 Save to session

        # ✅ Form data with character limit
        data = {
            "name": limit_text(request.form.get('name'), 50),
            "email": limit_text(request.form.get('email'), 100),
            "phone": limit_text(request.form.get('phone'), 20),
            "address": limit_text(request.form.get('address'), 100),
            "about": limit_text(request.form.get('about'), 300),
            "skills": limit_text(request.form.get('skills'), 200),
            "education": limit_text(request.form.get('education'), 400),
            "experience": limit_text(request.form.get('experience'), 400),
            "projects": limit_text(request.form.get('projects'), 300),
            "photo": photo_filename
        }

        # 🎨 Template
        template_choice = request.form.get('template', '1')
        template_file = f"template{template_choice}.html"

        return render_template(template_file, data=data)

    return render_template("form.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)