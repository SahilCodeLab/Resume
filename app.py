from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from io import BytesIO
from PIL import Image
import os, base64

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        photo_filename = None

        # ✅ Step 1: Check for base64 cropped image
        photo_data = request.form.get('photo_data')
        if photo_data and "base64" in photo_data:
            try:
                header, encoded = photo_data.split(",", 1)
                image_data = base64.b64decode(encoded)

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                photo_filename = f"cropped_{timestamp}.png"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)

                # Save using PIL
                image = Image.open(BytesIO(image_data)).convert("RGB")
                image.save(photo_path, format="PNG")

            except Exception as e:
                print("❌ Failed to process base64 image:", e)

        # ✅ Step 2: If no base64, check for uploaded file
        elif 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename:
                filename = secure_filename(photo.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                photo_filename = f"{timestamp}_{filename}"
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)

        # ✅ Step 3: Collect form data
        data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "address": request.form.get('address'),
            "about": request.form.get('about'),
            "skills": request.form.get('skills'),
            "education": request.form.get('education'),
            "experience": request.form.get('experience'),
            "projects": request.form.get('projects'),
            "photo": photo_filename
        }

        # ✅ Step 4: Select resume template
        template_choice = request.form.get('template', '1')
        template_file = f"template{template_choice}.html"

        return render_template(template_file, data=data)

    return render_template("form.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)