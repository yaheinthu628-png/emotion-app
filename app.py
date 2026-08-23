import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from gtts import gTTS
import os
import base64

st.set_page_config(page_title=" AI Scanner", layout="centered")

# အသံထွက်ပေးရန် Function (gTTS)
def play_audio(text):
    try:
        tts = gTTS(text=text, lang='my')
        tts.save("speech.mp3")
        
        with open("speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.write("အသံမထွက်နိုင်ပါ: ", e)

# ၁။ AI စက်ရုပ်ပုံနှင့် မိတ်ဆက်စာသား
st.title("🤖 သီးရိလှိုင် AI Emotion Scanner")

intro_speech = (
    "မင်္ဂလာပါ လူကြီးမင်း၊ ကျွန်တော်ကို ကြိုက်သလို ခေါ်နိုင်ပါတယ်။ "
    "ဖန်တီးတဲ့သူကတော့ ကျွန်တော်ကို သီးရိလှိုင်လို့ နာမည်ပေးထားပါတယ်။ "
    "လူကြီးမင်းရဲ့ မျက်နှာကို Scan ဖတ်ပြီး စိတ်ခံစားချက်တွေကို ပြောပြပေးပါမယ်။"
)
st.info(intro_speech)

# ၂။ ဓာတ်ပုံ ရယူခြင်း
img_file_buffer = st.camera_input("Scan ဖတ်ရန် ဓာတ်ပုံရိုက်ပါ")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # ၃။ ခံစားချက်ကို Analyse လုပ်ခြင်း
    with st.spinner('သီးရိလှိုင်မှ Scan ဖတ်နေပါသည်။ ခဏစောင့်ပါ...'):
        try:
            results = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False, detector_backend='skip')
            emotion = results[0]['dominant_emotion']

            emotion_mm = {
                'happy': 'ပျော်ရွှင်နေပါတယ်',
                'sad': 'ဝမ်းနည်းနေပါတယ်',
                'angry': 'ဒေါသထွက်နေပါတယ်',
                'surprise': 'အံ့ဩနေပါတယ်',
                'neutral': 'ပုံမှန်အေးအေးဆေးဆေး ဖြစ်နေပါတယ်'
            }
            detected_mood = emotion_mm.get(emotion, 'စိတ်ခံစားချက် တစ်ခုခု ဖြစ်နေပါတယ်')

            # ၄။ ရလဒ် စာတန်းနှင့် နောက်ဆုံး စကားပြော
            final_speech = (
                f"လူကြီးမင်းရဲ့ စိတ်ခံစားချက်ကတော့ {detected_mood} ဖြစ်ပါတယ်။ "
                "နောက်ဆုံးမှာတော့ လူကြီးမင်းရဲ့ ကောင်လေးကို အနမ်းပေးဖို့ လိုနေပါပြီ။ "
                "အမြန်လေး သွားပြီး အနမ်းပေးလိုက်ပါနော်။"
            )

            st.success(final_speech)
            play_audio(final_speech)

        except Exception as e:
            st.error(f"Error ဖြစ်နေပါသည်: {e}") 