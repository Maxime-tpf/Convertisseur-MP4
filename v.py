import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.title("Découpeur de vidéo simple")

uploaded_file = st.file_uploader("Uploader une vidéo", type=["mp4", "mov", "avi"])

if uploaded_file:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        clip = VideoFileClip(tmp_file_path)
        duration = clip.duration

        st.write("### Sélectionner la plage à découper (en secondes)")
        start = st.number_input("Début", min_value=0.0, max_value=duration, value=0.0)
        end = st.number_input("Fin", min_value=start, max_value=duration, value=duration)

        if st.button("Rogner la vidéo"):
            subclip = clip.subclip(start, end)

            # Créer un fichier temporaire de sortie
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as out_file:
                output_path = out_file.name

            # Exporter la vidéo
            subclip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                verbose=False,
                logger=None
            )

            with open(output_path, "rb") as f:
                video_bytes = f.read()

            st.success("Vidéo rognée avec succès")
            st.download_button("Télécharger le clip", video_bytes, file_name="video_clip.mp4", mime="video/mp4")

    except Exception as e:
        st.error(f"Erreur : {e}")
    finally:
        try:
            clip.close()
        except:
            pass
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists("temp-audio.m4a"):
            os.remove("temp-audio.m4a")
