import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.set_page_config(page_title="Découpeur Vidéo", layout="centered")
st.title("🎬 Découpeur de vidéo simple")

uploaded_file = st.file_uploader("Uploader une vidéo", type=["mp4", "mov", "avi"])

if uploaded_file:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        clip = VideoFileClip(tmp_file_path)
        duration = clip.duration

        # Limite de sécurité pour Streamlit Cloud (30 sec max)
        max_clip = min(duration, 30.0)

        st.write("### Sélectionner la plage à découper (max 30 sec)")
        start = st.number_input("Début", min_value=0.0, max_value=max_clip, value=0.0)
        end = st.number_input("Fin", min_value=start, max_value=max_clip, value=max_clip)

        if st.button("✂️ Rogner la vidéo"):
            with st.spinner("Traitement..."):
                subclip = clip.subclip(start, end)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as out_file:
                    output_path = out_file.name

                subclip.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    temp_audiofile="temp-audio.m4a",
                    remove_temp=True,
                    verbose=False,
                    logger=None,
                )

                with open(output_path, "rb") as f:
                    video_bytes = f.read()

                st.success("✅ Vidéo rognée avec succès")
                st.download_button(
                    label="📥 Télécharger le clip",
                    data=video_bytes,
                    file_name="video_clip.mp4",
                    mime="video/mp4"
                )

    except Exception as e:
        st.error(f"Erreur : {e}")
        st.exception(e)
    finally:
        try:
            clip.close()
        except:
            pass
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists("temp-audio.m4a"):
            os.remove("temp-audio.m4a")
