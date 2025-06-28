from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

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
        # Save photo if uploaded
        photo = request.files.get('photo')
        photo_filename = None

        if photo and photo.filename != '':
            photo_filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(photo_path)

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

        template_choice = request.form.get('template', '1')  # default template1
        template_file = f"template{template_choice}.html"

        return render_template(template_file, data=data)

    return render_template("form.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)