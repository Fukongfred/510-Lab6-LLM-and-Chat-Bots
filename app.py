import os
import streamlit as st
import openai
from dotenv import load_dotenv
import io
from PIL import Image
import PIL.Image

load_dotenv()

# Configure OpenAI GPT-4 API
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4"  # Using GPT-4 model
extracted_results = []  

def prepare_image(uploaded_file):
    image = Image.open(uploaded_file)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # Adjust format as needed
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def process_analysis_text(text):
    # Implement the logic to process the analysis text and extract top 5 items and similarities
    pass

def upload_image():
    uploaded_file = st.file_uploader("Upload Your Cloud Photo", type=["jpg", "jpeg", "png"], key="image_uploader")
    if uploaded_file is not None:
        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Cloud Photo', width=200)
    return uploaded_file

uploaded_image = upload_image()

if uploaded_image is not None:
    user_response = st.text_input("What objects do you think the cloud looks like?")
    if user_response:  # Check if the user has entered a response
        # When the user provides an answer, show a button to get results
        if st.button('Reveal the Riddle'):
            with st.spinner('Analyzing...'):
                try:
                    img_byte_arr = prepare_image(uploaded_image)
                    prompt = f"What top 5 objects does this cloud resemble? Include the corresponding degree of similarity, for example, dog: 60%, bird: 30%."
                    response = openai.Image.create(
                        model=model,
                        images=[img_byte_arr],
                        prompt=prompt,
                        n=1
                    )
                    analysis_text = response.choices[0].text
                    st.write(analysis_text)  # Remove this line if you don't want to display the raw API response
                    
                    extracted_results = process_analysis_text(analysis_text)
                    if extracted_results:
                        st.subheader("Top 5 Similarities:")
                        for item, similarity in extracted_results:
                            st.write(f"- {item}: {similarity}%")
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if extracted_results:
    st.subheader("Top 5 Similarities:")
    for item, similarity in extracted_results:
        st.write(f"- {item}: {similarity}%")