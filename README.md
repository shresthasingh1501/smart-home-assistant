
# Voice Command Assistant

This is a simple Streamlit application that records audio commands, transcribes them using OpenAI's Whisper model, processes the command with GPT-4o, and provides a structured JSON output. The assistant also converts the response text into speech.

## Features

- **Record Audio:** Capture voice commands using your microphone.
- **Transcription:** Transcribe recorded audio to text using OpenAI's Whisper model.
- **Command Processing:** Interpret the transcribed command and generate a structured JSON response with GPT-4o.
- **Text-to-Speech:** Convert the JSON response to speech using OpenAI's text-to-speech model.
- **Streamlit Interface:** User-friendly web interface for interaction.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/voice-command-assistant.git
   cd voice-command-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install `pyaudio` (if not installed):**
   - On Windows:
     ```bash
     pip install pipwin
     pipwin install pyaudio
     ```
   - On macOS:
     ```bash
     brew install portaudio
     pip install pyaudio
     ```
   - On Linux:
     ```bash
     sudo apt-get install python3-pyaudio
     pip install pyaudio
     ```

## Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Start Recording:**
   - Click the "Start Recording" button on the web interface to record your voice command.

3. **Transcription and Command Processing:**
   - The application will transcribe your audio and generate a JSON response based on the command.

4. **Text-to-Speech:**
   - The JSON response will be converted to speech and played back through the interface.

## Example Commands

- "Play Taylor Swift on Spotify"
- "What's the weather like in New York?"

## Important Notes

- **API Key:** The application uses an OpenAI API key for processing commands. The key is hardcoded in the script for testing purposes. Replace it with your own API key and consider using environment variables or a secure vault for production environments.
- **Security Warning:** Avoid hardcoding sensitive information such as API keys in your code, especially in production.

## Contributing

Feel free to fork this repository and submit pull requests if you have any improvements or fixes.

## License

This project is licensed under the MIT License.

---

Created by Shrestha Singh

