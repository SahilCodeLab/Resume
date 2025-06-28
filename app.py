from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os, base64
from datetime import datetime

app = Flask(__name__)

# Folder to save uploaded photos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        photo_filename = None

        # 🔍 Check if cropped base64 photo is sent
        photo_data = request.form.get('photo_data')

        if photo_data:
            try:
                # Clean base64 header and decode
                header, encoded = photo_data.split(",", 1)
                binary_data = base64.b64decode(encoded)

                # Create unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                photo_filename = f"cropped_{timestamp}.png"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)

                with open(photo_path, "wb") as f:
                    f.write(binary_data)

            except Exception as e:
                print("Base64 decode error:", e)

        else:
            # ✨ Fallback if normal photo file uploaded
            photo = request.files.get('photo')
            if photo and photo.filename != '':
                photo_filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)

        # 💾 Form data
        data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "address": request.form['address'],
            "about": request.form['about'],
            "skills": request.form['skills'],
            "education": request.form['education'],
            "experience": request.form['experience'],
            "projects": request.form['projects'],
            "photo": photo_filename
        }

        template_choice = request.form.get('template', '1')
        template_file = f"template{template_choice}.html"

        return render_template(template_file, data=data)

    return render_template("form.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)