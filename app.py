from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
PICTURE_FOLDER = 'static/pictures/Pics/class0'  # Folder For Predictions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PICTURE_FOLDER'] = PICTURE_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return redirect(request.url)

    file = request.files['video']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return render_template('index.html', video_path=filepath)

    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve images from the specified folder
    anomaly_images = [
        os.path.join(app.config['PICTURE_FOLDER'], filename)
        for filename in os.listdir(app.config['PICTURE_FOLDER'])
        if filename.lower().endswith(('png', 'jpg', 'jpeg'))
    ]
    return render_template('index.html', anomaly_images=anomaly_images[:1])  # Limit to first 4 images

if __name__ == '__main__':
    app.run(debug=True)
