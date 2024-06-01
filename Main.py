import streamlit as st
import asyncio
import nest_asyncio
from utils import generate_prompt
from agent import run_agent, get_groq_api_key
import os
import json

nest_asyncio.apply()

RAM_OPTIONS = ['2 GB', '4 GB', '6 GB', '8 GB', '12 GB', '16 GB']
STORAGE_OPTIONS = ['16 GB', '32 GB', '64 GB', '128 GB', '256 GB', '512 GB', '1 TB']
CAMERA_OPTIONS = ['8 MP', '12 MP', '16 MP', '24 MP', '48 MP', '64 MP', '108 MP']
BATTERY_OPTIONS = ['3000 mAh', '4000 mAh', '5000 mAh', '6000 mAh', '7000 mAh']
PROCESSOR_OPTIONS = ['Quad-Core', 'Octa-Core', 'Snapdragon 665', 'Snapdragon 865', 'Exynos 990', 'A14 Bionic']
PHONE_COMPANIES = ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi", "Huawei", "Sony", "LG", "Motorola", "Nokia", "Oppo", "Vivo", "Realme", "Asus", "Lenovo"]
DISPLAY_SIZE_OPTIONS = ['5.0"', '5.5"', '6.0"', '6.5"', '6.7"', '6.9"']
PRICE_RANGE = (10000, 300000)

st.title("Phone Buddy")
st.caption('''This application takes user requirements as input and provides recommendations for the two best smartphones that meet their criteria.
Let's find the ideal smartphone for you.''')
st.code('''
def PhoneBuddy(product):
    if product == "Best":
        return "We got it for you!"
    else:
        return "Find Next! Repeat!"
''')

selected_ram = st.multiselect('Select RAM options:', RAM_OPTIONS)
selected_company = st.multiselect('Select Company options:', PHONE_COMPANIES)
selected_storage = st.multiselect('Select Storage options:', STORAGE_OPTIONS)
selected_battery = st.multiselect('Select Battery options:', BATTERY_OPTIONS)
selected_camera = st.multiselect('Select Camera options:', CAMERA_OPTIONS)
selected_processor = st.multiselect('Select Processor options:', PROCESSOR_OPTIONS)
selected_display_size = st.multiselect('Select Display Size options:', DISPLAY_SIZE_OPTIONS)
selected_price = st.slider('Select Price Range (₹):', PRICE_RANGE[0], PRICE_RANGE[1], (PRICE_RANGE[0], PRICE_RANGE[1]), step=500)
prompt = st.text_area('Or Write your requirements in text:')

if st.button('Suggest'):
    sample_prompt = generate_prompt(selected_ram, selected_storage, selected_camera, selected_processor, selected_display_size, selected_price, selected_company, selected_battery, prompt)
    # st.write(sample_prompt)
    asyncio.run(run_agent(sample_prompt, get_groq_api_key()))
    if 'groq_response' in st.session_state:
        st.write('### Top 2 Suggestions:')
        try:
            response_json = json.loads(st.session_state['groq_response'])
            for phone, specs in response_json.items():
                st.subheader(phone)
                for spec_key, spec_value in specs.items():
                    st.write(f"**{spec_key.capitalize()}:** {spec_value}")
                st.markdown("---")
        except json.JSONDecodeError:
            st.write(st.session_state['groq_response'])

url = "https://github.com/Akashkunwar/phone-buddy"
st.write("Check out phone buddy [github repository](%s)" % url)
