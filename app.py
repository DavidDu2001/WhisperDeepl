from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
import torch
import deepl
from googletrans import Translator
from datetime import timedelta
from whisper_trans import translate_whisper
auth_key = "d36d6d0f-3a89-4a01-9437-7da88f7ac1c8:fx"

app = Flask(__name__)

# Set the directory where files will be stored
UPLOAD_FOLDER = r'C:\Users\david\PycharmProjects\whisper\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 5000 * 5000
app.config['UPLOAD_EXTENSIONS'] = ['.mp3', '.mp4']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    model_size = request.form['model_size']  # Get the selected model size
    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        # Translate the file and get the new filename
        filename = translate_whisper(file_path, app.config['UPLOAD_FOLDER'], model_size)
        os.remove(file_path)
        # Redirect to download the new SRT file
        return redirect(url_for('download_file', filename=filename))
    # Iterate over all files in the directory
    folder_path = r"C:\Users\david\PycharmProjects\whisper\uploads"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if it is a file (and not a directory)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file
    return redirect(url_for('index'))


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

# Include your existing functions for transcribing, translating, etc.
#flask run --host=0.0.0.0 --port=5000