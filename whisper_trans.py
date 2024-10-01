import subprocess
import os
import deepl
import whisper
import torch
from googletrans import Translator
auth_key = "d36d6d0f-3a89-4a01-9437-7da88f7ac1c8:fx"

from datetime import timedelta


def whisper_transcribe(file, output):
    # Configuration
    model_size = "medium"
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Load the model
    model = whisper.load_model(model_size).to(device)

    # Your audio file

    # Transcribe the audio
    result = model.transcribe(file)

    # Create SRT file
    srt_file_path = os.path.join(output,
                                 os.path.basename(file).replace('.mp3', '.srt'))  # Adjust the extension as needed

    segments = result['segments']

    with open(srt_file_path, 'w', encoding='utf-8') as srtFile:
        pass  # Clear the file

    for segment in segments:
        start_time = str(timedelta(seconds=segment['start'])).replace('.', ',')
        end_time = str(timedelta(seconds=segment['end'])).replace('.', ',')
        text = segment['text'].lstrip()  # Remove leading space
        segment_id = segment['id'] + 1

        segment_text = f"{segment_id}\n{start_time} --> {end_time}\n{text}\n\n"

        with open(srt_file_path, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment_text)

    print(f"SRT file created at: {srt_file_path}")
    return srt_file_path


def convert_srt_txt(file):
    with open(file,encoding="utf8") as f:
        file_contents = f.read()
        # Extract file name without extension
    file_name_without_extension = file.rsplit('.', 1)[0]

    # Create new file with the desired extension
    new_file = f"{file_name_without_extension}.txt"

    with open(new_file, 'w',encoding='utf-8') as f:
        # Write the contents to the new file
        f.write(file_contents)
    return new_file


def convert_txt_srt(file):
    with open(file,encoding="utf8") as f:

        file_contents = f.read()
        # Extract file name without extension
    file_name_without_extension = file.rsplit('.', 1)[0]

    # Create new file with the desired extension
    new_file = f"{file_name_without_extension}.srt"

    with open(new_file, 'w', encoding='utf-8') as f:
        # Write the contents to the new file
        f.write(file_contents)

def translate(file,file_trans):
    filename = os.path.basename(file)

    translator = deepl.Translator(auth_key)
    filename = "deepl_" + filename
    output = os.path.join(file_trans,
                             filename)  # Adjust the extension as needed

    try:
        # Using translate_document_from_filepath() with file paths
        translator.translate_document_from_filepath(
            file,
            output,
            target_lang="EN-US",
        )
    except deepl.DocumentTranslationException as error:
        # If an error occurs during document translation after the document was
        # already uploaded, a DocumentTranslationException is raised. The
        # document_handle property contains the document handle that may be used to
        # later retrieve the document from the server, or contact DeepL support.
        doc_id = error.document_handle.id
        doc_key = error.document_handle.key
        print(f"Error after uploading ${error}, id: ${doc_id} key: ${doc_key}")
    except deepl.DeepLException as error:
        # Errors during upload raise a DeepLException
        print(error)


if __name__ == '__main__':
    file = r"C:\Users\david\PycharmProjects\whisper\MP3\video.mp4"
    output = r"C:/Users/david/PycharmProjects/whisper/transcriptions"
    # srt_file = whisper_transcribe(file, output)
    # txt_file = convert_srt_txt(srt_file)
    txt_file = r"C:\Users\david\PycharmProjects\whisper\transcriptions\video.txt"
    txt_file_trans = r"C:\Users\david\PycharmProjects\whisper\transcriptions"

    translate(txt_file,txt_file_trans)
    convert_txt_srt(txt_file_trans)
