import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os

st.set_page_config(page_title="Speech2Script AI", layout="centered")

st.title("🎙️ Speech2Script AI")
st.write("Convert your voice into text easily!")

audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    file_name = audio_file.name
    with open(file_name, "wb") as f:
        f.write(audio_file.read())

    # Convert to wav
    if file_name.endswith(".mp3"):
        sound = AudioSegment.from_mp3(file_name)
        file_name = file_name.replace(".mp3", ".wav")
        sound.export(file_name, format="wav")
    elif file_name.endswith(".m4a"):
        sound = AudioSegment.from_file(file_name, format="m4a")
        file_name = file_name.replace(".m4a", ".wav")
        sound.export(file_name, format="wav")

    st.success("Audio file ready for transcription!")

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            st.subheader("📝 Transcription:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError:
            st.error("Request failed. Please check your internet.")

    os.remove(file_name)
