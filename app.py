from flask import Flask, render_template, request, send_file, url_for
import pdfkit
import os

app = Flask(__name__)

# Configure pdfkit
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "address": request.form['address'],
            "about": request.form['about'],
            "skills": request.form['skills'],
            "education": request.form['education'],
            "experience": request.form['experience'],
            "projects": request.form['projects']
        }

        template_choice = request.form['template']
        template_file = f"template{template_choice}.html"

        rendered = render_template(template_file, data=data)

        with open("resume_temp.html", "w", encoding='utf-8') as f:
            f.write(rendered)

        pdfkit.from_file("resume_temp.html", "resume.pdf", configuration=PDFKIT_CONFIG)

        return send_file("resume.pdf", as_attachment=True)

    return render_template("form.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)