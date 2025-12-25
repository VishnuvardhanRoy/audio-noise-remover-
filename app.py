import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np
import os
import tempfile

st.title("🎧 Audio Noise Remover")
st.write("Upload your noisy audio file below.")

uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "mpeg", "ogg", "m4a"])

if uploaded_file is not None:
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            temp_filename = tmp_file.name

        st.write("### Original Audio:")
        st.audio(uploaded_file)
        
        st.info("🔄 Processing... this might take 10-20 seconds...")

        # Load audio
        data, rate = librosa.load(temp_filename, sr=None)
        
        # Remove noise
        reduced_noise = nr.reduce_noise(y=data, sr=rate, stationary=True)
        
        # Save clean audio
        output_filename = "clean_audio.wav"
        sf.write(output_filename, reduced_noise, rate)

        st.success("✅ Success! Noise removed.")
        st.write("### 🔉 Cleaned Audio:")
        st.audio(output_filename, format="audio/wav")

        with open(output_filename, "rb") as file:
            st.download_button(
                label="⬇️ Download Clean Audio",
                data=file.read(),
                file_name="clean_audio.wav",
                mime="audio/wav"
            )
        
        # Cleanup
        os.remove(temp_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Try uploading a different audio file format")

