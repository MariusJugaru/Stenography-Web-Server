import EncodeScript
import DecodeScript

from flask import Flask, request, render_template, send_from_directory, url_for

from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField



ALLOWED_EXTENSIONS = set(['png', 'bmp'])

app = Flask(__name__, static_folder="public")
app.config['SECRET_KEY'] = 'Efectiv'
app.config['UPLOADED_PHOTOS_DEST'] = 'Uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only .png, .bmp images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

session = {}
filename = ''

ALLOWED_USERS = { "admin": "n0h4x0rz-plz" }

DATABASE_FILE = "database.txt"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image/encode", methods=['POST', 'GET'])
def encode():
    form = UploadForm()
    if form.validate_on_submit():
        global filename 
        filename = photos.save(form.photo.data)
        msg = request.form['text']
        EncodeScript.encode(imgName=filename,message=msg)
        file_url = url_for('get_file', filename=filename)
    else:
        file_url = None
    return render_template("encode.html", form=form, file_url=file_url)

@app.route("/image/last/encoded", methods=['POST', 'GET'])
def encoded():
    file_url = url_for('get_file', filename=filename)
    return render_template("encoded.html", file_url=file_url)


@app.route("/image/decode", methods=['POST', 'GET'])
def decode():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        message = DecodeScript.decode(imgName=filename)
    else:
        message = None
    return render_template("decode.html", form=form, message=message)


# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(debug=True, port=5000)

