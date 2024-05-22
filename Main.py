import streamlit as st

ram_options = ['2 GB', '4 GB', '6 GB', '8 GB', '12 GB', '16 GB']
storage_options = ['16 GB', '32 GB', '64 GB', '128 GB', '256 GB', '512 GB', '1 TB']
camera_options = ['8 MP', '12 MP', '16 MP', '24 MP', '48 MP', '64 MP', '108 MP']
processor_options = ['Quad-Core', 'Octa-Core', 'Snapdragon 665', 'Snapdragon 865', 'Exynos 990', 'A14 Bionic']
display_size_options = ['5.0"', '5.5"', '6.0"', '6.5"', '6.7"', '6.9"']
price_range = (10000, 200000)
rating_range = (1, 5)

st.title("Phone Buddy")
st.caption("Let's get the best phone suggestion for you")
st.code('''
def PhoneBuddy(product):
    if product == "Best":
        return "We got it for you!"
    else:
        return "Find Next! Repeat!"
''')

selected_ram = st.multiselect('Select RAM options:', ram_options)
selected_storage = st.multiselect('Select Storage options:', storage_options)
selected_camera = st.multiselect('Select Camera options:', camera_options)
selected_processor = st.multiselect('Select Processor options:', processor_options)
selected_display_size = st.multiselect('Select Display Size options:', display_size_options)
selected_price = st.slider('Select Price Range ($):', price_range[0], price_range[1], (price_range[0], price_range[1]))
selected_rating = st.slider('Select Minimum Rating:', *rating_range, step=1)
prompt = st.text_area('Or Write Prompt:')

st.write('You selected the following options:')
st.write('**RAM:**', selected_ram)
st.write('**Storage:**', selected_storage)
st.write('**Camera:**', selected_camera)
st.write('**Processor:**', selected_processor)
st.write('**Display Size:**', selected_display_size)
st.write('**Price Range: $**', selected_price)
st.write('**Minimum Rating:**', selected_rating)


def get_recommendations(ram, storage, camera, processor, display_size, price, rating):
    recommendations = [
        {
            'Name': 'Phone A',
            'RAM': '4 GB',
            'Storage': '64 GB',
            'Camera': '12 MP',
            'Processor': 'Snapdragon 665',
            'Display Size': '6.0"',
            'Price': 30000,
            'Rating': 4.5
        },
        {
            'Name': 'Phone B',
            'RAM': '6 GB',
            'Storage': '128 GB',
            'Camera': '48 MP',
            'Processor': 'Snapdragon 865',
            'Display Size': '6.5"',
            'Price': 70000,
            'Rating': 4.8
        },
    ]

    filtered_recommendations = [
        phone for phone in recommendations
        if (not ram or phone['RAM'] in ram) and
           (not storage or phone['Storage'] in storage) and
           (not camera or phone['Camera'] in camera) and
           (not processor or phone['Processor'] in processor) and
           (not display_size or phone['Display Size'] in display_size) and
           (price[0] <= phone['Price'] <= price[1]) and
           (phone['Rating'] >= rating)
    ]
    return filtered_recommendations

recommendations = get_recommendations(selected_ram, selected_storage, selected_camera, selected_processor, selected_display_size, selected_price, selected_rating)

st.write('### Recommended Smartphones:')
if recommendations:
    for phone in recommendations:
        st.write(f"**Name:** {phone['Name']}")
        st.write(f"**RAM:** {phone['RAM']}")
        st.write(f"**Storage:** {phone['Storage']}")
        st.write(f"**Camera:** {phone['Camera']}")
        st.write(f"**Processor:** {phone['Processor']}")
        st.write(f"**Display Size:** {phone['Display Size']}")
        st.write(f"**Price:** ${phone['Price']}")
        st.write(f"**Rating:** {phone['Rating']}")
        st.write('---')
else:
    st.write("No smartphones match your criteria.")
