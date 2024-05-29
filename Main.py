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
st.caption("Let's get the best phone suggestion for you")
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


# import streamlit as st
# import asyncio
# import nest_asyncio
# from uagents import Agent, Context, Model
# from groq import Groq
# import os
# import json

# nest_asyncio.apply()

# RAM_OPTIONS = ['2 GB', '4 GB', '6 GB', '8 GB', '12 GB', '16 GB']
# STORAGE_OPTIONS = ['16 GB', '32 GB', '64 GB', '128 GB', '256 GB', '512 GB', '1 TB']
# CAMERA_OPTIONS = ['8 MP', '12 MP', '16 MP', '24 MP', '48 MP', '64 MP', '108 MP']
# BATTERY_OPTIONS = ['3000 mAh', '4000 mAh', '5000 mAh', '6000 mAh', '7000 mAh']
# PROCESSOR_OPTIONS = ['Quad-Core', 'Octa-Core', 'Snapdragon 665', 'Snapdragon 865', 'Exynos 990', 'A14 Bionic']
# PHONE_COMPANIES = ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi", "Huawei", "Sony", "LG", "Motorola", "Nokia", "Oppo", "Vivo", "Realme", "Asus", "Lenovo"]
# DISPLAY_SIZE_OPTIONS = ['5.0"', '5.5"', '6.0"', '6.5"', '6.7"', '6.9"']
# PRICE_RANGE = (10000, 300000)

# st.title("Phone Buddy")
# st.caption("Let's get the best phone suggestion for you")
# st.code('''
# def PhoneBuddy(product):
#     if product == "Best":
#         return "We got it for you!"
#     else:
#         return "Find Next! Repeat!"
# ''')

# selected_ram = st.multiselect('Select RAM options:', RAM_OPTIONS)
# selected_company = st.multiselect('Select Company options:', PHONE_COMPANIES)
# selected_storage = st.multiselect('Select Storage options:', STORAGE_OPTIONS)
# selected_battery = st.multiselect('Select Battery options:', BATTERY_OPTIONS)
# selected_camera = st.multiselect('Select Camera options:', CAMERA_OPTIONS)
# selected_processor = st.multiselect('Select Processor options:', PROCESSOR_OPTIONS)
# selected_display_size = st.multiselect('Select Display Size options:', DISPLAY_SIZE_OPTIONS)
# selected_price = st.slider('Select Price Range (₹):', PRICE_RANGE[0], PRICE_RANGE[1], (PRICE_RANGE[0], PRICE_RANGE[1]), step=500)
# prompt = st.text_area('Or Write your requirenments in text:')

# def generate_prompt(ram, storage, camera, processor, display_size, price, company, battery):
#     parts = ["List of 2 best phones with following minimum specs:"]
#     if ram:
#         parts.append(f"ram - {', '.join(ram)}")
#     if storage:
#         parts.append(f"rom - {', '.join(storage)}")
#     if battery:
#         parts.append(f"rom - {', '.join(battery)}")
#     if camera:
#         parts.append(f"front camera - {camera[0] if camera else ''}, back camera - {camera[-1] if camera else ''}")
#     if display_size:
#         parts.append(f"screen size - {', '.join(display_size)}")
#     if processor:
#         parts.append(f"processor - {', '.join(processor)}")
#     if company:
#         parts.append(f"company - {', '.join(company)}")
#     if price:
#         parts.append(f"under price {price[1]} INR")
#     prompt_text = ", ".join(parts)
#     prompt_text += f" {prompt}. Output results in json with phone name being primary key and specs being nested key: value pair. Make sure to include price in INR"
#     return prompt_text

# async def run_agent(prompt):
#     groq_api_key = os.getenv('groq_api_key')

#     class QueryRequest(Model):
#         query: str
#     class QueryResponse(Model):
#         response: str

#     client = Groq(api_key=groq_api_key)
#     agent = Agent(name="fetch_groq_agent")

#     @agent.on_message(model=QueryRequest)
#     async def handle_query(ctx: Context, query_request: QueryRequest):
#         completion = client.chat.completions.create(
#             model="gemma-7b-it",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": query_request.query
#                 }
#             ],
#             temperature=1,
#             max_tokens=1024,
#             top_p=1,
#             stream=True,
#             stop=None,
#         )
#         response_data = ""
#         for chunk in completion:
#             response_data += chunk.choices[0].delta.content or ""
#         st.session_state['groq_response'] = response_data
#     query_request = QueryRequest(query=prompt)
#     await handle_query(None, query_request)

# if st.button('Suggest'):
#     sample_prompt = generate_prompt(selected_ram, selected_storage, selected_camera, selected_processor, selected_display_size, selected_price, selected_company, selected_battery)
#     st.write(sample_prompt)
#     asyncio.run(run_agent(sample_prompt))
#     if 'groq_response' in st.session_state:
#         st.write('### Top 2 Suggestions:')
#         try:
#             response_json = json.loads(st.session_state['groq_response'])
#             for phone, specs in response_json.items():
#                 st.subheader(phone)
#                 for spec_key, spec_value in specs.items():
#                     st.write(f"**{spec_key.capitalize()}:** {spec_value}")
#                 st.markdown("---")
#         except json.JSONDecodeError:
#             st.write(st.session_state['groq_response'])