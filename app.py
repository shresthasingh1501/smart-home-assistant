import streamlit as st
import json
from openai import OpenAI
from pathlib import Path
import tempfile
import pyaudio
import wave
# Initialize OpenAI client with hardcoded API key
# WARNING: This is not secure and should only be used for testing
client = OpenAI(api_key="sk-GeJ-zPXVgIGC2UIhA42dvW2g6lsc9SXjkHMsU9S5EgT3BlbkFJiG94ZfVUll-OgSkIivuBYEa3xGIErTL_u6DSQDUt4A")

# System prompt for GPT-4
SYSTEM_PROMPT = """
You are an AI assistant that converts user commands into structured JSON data. Your task is to interpret the user's intent and create a JSON object with relevant fields. Always include a 'response' field in the JSON with a friendly, conversational reply to the user's command.

For example:
User: "Play Taylor Swift on Spotify"
JSON: {
    "action": "play music",
    "application": "Spotify",
    "artist": "Taylor Swift",
    "response": "Sure, I'm playing Taylor Swift on Spotify for you now. Enjoy the music!"
}

User: "What's the weather like in New York?"
JSON: {
    "action": "check weather",
    "location": "New York",
    "response": "I'm checking the weather in New York for you. One moment please."
}

Adapt the JSON structure to fit the context of the command, but always include the 'response' field.
"""

def record_audio(duration=5, sample_rate=44100, chunk=1024, channels=1):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        wf = wave.open(temp_audio_file.name, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return temp_audio_file.name

def transcribe_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def process_command(command):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command}
        ]
    )
    return json.loads(response.choices[0].message.content)

def text_to_speech(text):
    speech_file_path = Path(tempfile.gettempdir()) / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

st.title("Voice Command Assistant")

if st.button("Start Recording"):
    with st.spinner("Recording for 5 seconds..."):
        audio_file_path = record_audio()
    st.success("Recording complete!")

    # Transcribe audio
    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(audio_file_path)
    st.write("Transcription:", transcription)

    # Process command
    with st.spinner("Processing command..."):
        result = process_command(transcription)
    
    # Display JSON result
    st.json(result)

    # Extract response and convert to speech
    response_text = result["response"]
    with st.spinner("Generating speech..."):
        speech_file = text_to_speech(response_text)

    # Play the generated speech
    st.audio(str(speech_file))

st.markdown("---")
st.write("Created by Shrestha Singh")
