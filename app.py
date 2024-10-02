from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os, shutil
from whisper_trans import translate_whisper, valid_key


app = Flask(__name__)

# Set the directory where files will be stored
UPLOAD_FOLDER = r'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 5000 * 5000
app.config['UPLOAD_EXTENSIONS'] = ['mp3', 'mp4']



@app.route('/')
def index():
    return render_template('index.html')


def delete_folder():
    # Remove all files in the upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            os.remove(file_path)




@app.route('/', methods=['POST'])
def upload_file():
    delete_folder()
    uploaded_file = request.files.get('file')
    model_size = request.form.get('model_size')
    deepl_key = request.form.get('DeepL_Key')
    target = request.form.get('language')

    #get extension of uploaded file
    file_name_without_extension = uploaded_file.filename.rsplit('.', 1)[1]
    print(file_name_without_extension)

    #Refuse files that have not the correct extension
    if file_name_without_extension not in app.config['UPLOAD_EXTENSIONS']:
        flash('Wrong file type. Please choose a valid mp3/mp4 file.')
        return redirect(url_for('index'))

    #Check whether key is valid or not
    if not valid_key(deepl_key):
        flash('Invalid DeepL API key. You can obtain a key at https://www.deepl.com/en/pro-api')
        return redirect(url_for('index'))

    #Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

    # Translate the file and get the new filename
    try:
        filename = translate_whisper(file_path, app.config['UPLOAD_FOLDER'], model_size, deepl_key,target)
    except Exception as e:
        flash(f'Error during processing: {str(e)}')
        os.remove(file_path)  # Clean up uploaded file on error
        return redirect(url_for('index'))

    #Remove the saved file
    os.remove(file_path)
    return redirect(url_for('download_file', filename=filename))


@app.route('/downloads/<filename>')
def download_file(filename):
    # Send the file
    response = send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    return response

if __name__ == '__main__':
    app.run(debug=True)

#flask run --host=0.0.0.0 --port=5000