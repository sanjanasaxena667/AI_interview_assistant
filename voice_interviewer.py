import whisper
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
from playsound import playsound
import streamlit as st
import numpy as np
import soundfile as sf
import os
import edge_tts
import asyncio
import webrtcvad
import collections
import wave
import time
import collections
import io
import re
import tempfile
import base64

# Load Whisper model once
model = whisper.load_model("small")

async def generate_voice(text):

    voice = "en-IN-NeerjaNeural"   # sounds like professional interviewer

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        communicate = edge_tts.Communicate(text, voice, rate="-8%", pitch="-2Hz")
        await communicate.save(fp.name)
        return fp.name

# TEXT → SPEECH
def speak(text):
    text = re.sub(r"\*+", "", text)   # remove *
    text = re.sub(r"\#+", "", text)   # remove #
    text = re.sub(r"\-+", "", text)   # remove -
    text = re.sub(r"\`+", "", text)   # remove `
    audio_path = asyncio.run(generate_voice(text))

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)


# RECORD MICROPHONE AUDIO

def record_audio(filename="input.wav", fs=16000):

    vad = webrtcvad.Vad(2)

    frame_duration = 30
    frame_size = int(fs * frame_duration / 1000)

    ring_buffer = collections.deque(maxlen=30)
    voiced_frames = []

    triggered = False

    max_duration = 60
    start_time = time.time()

    print("Speak your answer...")

    with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:

        while True:

            # 🔴 safety stop
            if time.time() - start_time > max_duration:
                print("Max duration reached")
                break

            frame, _ = stream.read(frame_size)
            frame_bytes = frame.tobytes()

            is_speech = vad.is_speech(frame_bytes, fs)

            if not triggered:

                ring_buffer.append((frame_bytes, is_speech))

                num_voiced = len([f for f, speech in ring_buffer if speech])

                if num_voiced > 0.6 * ring_buffer.maxlen:
                    triggered = True
                    print("Recording started")

                    for f, s in ring_buffer:
                        voiced_frames.append(f)

                    ring_buffer.clear()

            else:

                voiced_frames.append(frame_bytes)

                ring_buffer.append((frame_bytes, is_speech))

                num_unvoiced = len([f for f, speech in ring_buffer if not speech])

                if num_unvoiced > 0.8 * ring_buffer.maxlen:
                    print("Recording stopped")
                    break

    wf = wave.open(filename, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(fs)
    wf.writeframes(b''.join(voiced_frames))
    wf.close()

    return filename


def remove_silence(input_file, threshold=0.01):

    audio, sr = sf.read(input_file)

    mask = np.abs(audio) > threshold

    cleaned = audio[mask]

    sf.write("cleaned.wav", cleaned, sr)

    return "cleaned.wav"

# SPEECH → TEXT
def speech_to_text(audio_file):

    try:
        result = model.transcribe(audio_file, fp16=False, language="en",temperature=0,no_speech_threshold=0.6)
        return result["text"].strip()

    except Exception as e:
        print("Whisper error:", e)
        return ""