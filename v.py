import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import io

st.title("Découpeur de vidéo simple")

uploaded_file = st.file_uploader("Uploader une vidéo", type=["mp4", "mov", "avi"])

if uploaded_file:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    clip = VideoFileClip(tmp_file_path)
    duration = clip.duration

    st.write("### Sélectionner la plage à découper (en secondes)")
    start = st.number_input("Début", min_value=0.0, max_value=duration, value=0.0)
    end = st.number_input("Fin", min_value=0.0, max_value=duration, value=duration)

    if st.button("Rogner la vidéo"):
        subclip = clip.subclip(start, end)
        buffer = io.BytesIO()
        subclip.write_videofile("output.mp4", codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
        with open("output.mp4", "rb") as f:
            st.success("Vidéo rognée avec succès")
            st.download_button("Télécharger le clip", f.read(), file_name="video_clip.mp4", mime="video/mp4")
