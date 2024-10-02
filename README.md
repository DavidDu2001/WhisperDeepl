# Audio/Video Transcription and Translation Tool

This project uses OpenAI's Whisper model to transcribe audio and video files and then utilizes the DeepL API to translate the transcripts into any desired language. 

## Features
- Transcribe audio and video files (MP3/MP4).
- Translate the transcriptions using DeepL API.
- Download the translated transcript as an SRT file.

## Prerequisites
- Python 3.x
- Flask
- OpenAI Whisper
- DeepL API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DavidDu2001/whisper_deepl.git
   cd whisper_deepl
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install pytorch. If you want to use your GPU for the whisper model, you will need to install pytorch with CUDA support which can be obtained from here: https://pytorch.org/get-started/locally/.

## Usage

1. Open your terminal and navigate to the main directory.
2. Run the Flask application:
   ```bash
   python app.py
   ```
   (Make sure your Python environment is activated.)

3. Open your web browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000).

4. Upload your MP3 or MP4 file and select the desired model size. Note that larger models yield better results but require more GPU power.

5. Input your DeepL API key,  you can  obtain your API key from [DeepL](https://www.deepl.com/pro-api).

6. After the transcription and translation are complete, you will be able to download the translated transcript as an SRT file.

## Supported Models
You can choose from different model sizes based on your needs. Keep in mind that larger models will consume more resources.

## Contributing
Contributions are welcome! If you have suggestions for improvements or features, feel free to create an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [OpenAI](https://openai.com) for the Whisper model.
- [DeepL](https://www.deepl.com) for their translation API.

---
