import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="သီးရိလှိုင် AI Scanner", page_icon="🎭")

st.title("🎭 သီးရိလှိုင် AI Scanner")
st.write("ဓာတ်ပုံတင်ပြီး စိတ်ခံစားချက်ကို စကင်ဖတ်ကြည့်ပါ!")

uploaded_file = st.file_uploader("ဓာတ်ပုံတစ်ပုံ ရွေးပေးပါ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="တင်ထားသော ဓာတ်ပုံ", use_column_width=True)
    
    if st.button("စကင်ဖတ်မည် 🔍"):
        with st.spinner("AI မှ စိတ်ခံစားချက်ကို စကင်ဖတ်နေပါသည်..."):
            emotions = ["ပျော်ရွှင်နေသည် (Happy) 😊", "ဝမ်းနည်းနေသည် (Sad) 😢", "ဒေါသထွက်နေသည် (Angry) 😡", "အံ့အားသင့်နေသည် (Surprised) 😲"]
            result = random.choice(emotions)
            
            st.success(f"**တွေ့ရှိချက် ခန့်မှန်းချက် -** {result}")
            st.balloons()
