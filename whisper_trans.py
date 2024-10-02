import os
import deepl
import whisper
import torch

from datetime import timedelta
# deepl_key = "d36d6d0f-3a89-4a01-9437-7da88f7ac1c8:fx"

def whisper_transcribe(file, output, model_size):
    # Configuration
    try:
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
    except Exception as e:
        return e


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
    return new_file


def translate(file, file_trans,deepl_key):
    filename = os.path.basename(file)
    translator = deepl.Translator(deepl_key)

    # Generate new filename
    translated_filename = "deepl_" + filename
    output = os.path.join(file_trans, translated_filename)  # Adjust the extension as needed

    try:
        # Translate the document
        translator.translate_document_from_filepath(file, output, target_lang="EN-US")
    except deepl.DocumentTranslationException as error:
        print(f"Error after uploading: {error}, id: {error.document_handle.id} key: {error.document_handle.key}")
    except deepl.DeepLException as error:
        print(error)

    return output  # Return the translated file path

def valid_key(key):
    try:
        translator = deepl.Translator(key)
        translator.translate_text("test", target_lang="EN-US")
        return True
    except:
        return False

def translate_whisper(file, output, model_size,deepl_key):
    # Step 1: Transcribe the audio to SRT
    srt_file = whisper_transcribe(file, output,model_size)

    # Step 2: Convert the SRT file to TXT
    txt_file = convert_srt_txt(srt_file)

    # Step 3: Translate the TXT file
    translated_txt_file = translate(txt_file, output,deepl_key)

    # Step 4: Convert the translated TXT back to SRT
    final_srt_file = convert_txt_srt(translated_txt_file)

    os.remove(srt_file)
    os.remove(txt_file)
    os.remove(translated_txt_file)
    # Return just the filename of the final translated SRT file
    return os.path.basename(final_srt_file)
#
# if __name__ == '__main__':
#     file = r"C:\Users\david\PycharmProjects\whisper\MP3\video.mp4"
#     output = r"C:/Users/david/PycharmProjects/whisper/transcriptions"
#     # srt_file = whisper_transcribe(file, output)
#     # txt_file = convert_srt_txt(srt_file)
#     txt_file = r"C:\Users\david\PycharmProjects\whisper\transcriptions\video.txt"
#     txt_file_trans = r"C:\Users\david\PycharmProjects\whisper\transcriptions"
#
#     translate(txt_file,txt_file_trans)
#     convert_txt_srt(txt_file_trans)
