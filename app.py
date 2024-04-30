import os
import streamlit as st
import google.generativeai as genai  # Assuming you renamed the library for brevity
from dotenv import load_dotenv
import io
from PIL import Image
import PIL.Image
import google.ai.generativelanguage as glm

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')
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
    user_response = st.text_input("What objects do you think the cloud looks like? ")
    if user_response:  # Check if the user has entered a response
        # When the user provides an answer, show a button to get results
        if st.button('Reveal the Riddle'):
            with st.spinner('Analyzing...'):
                try:
                    img_byte_arr = prepare_image(uploaded_image)
                    content = glm.Content(parts=[
                        glm.Part(text=f"You are a cloud researcher, you know a lot about the various cloud shapes in the sky and you have imagination. So What top 5 objects does this cloud resemble? and say the corresponding degree of similarity, for example, dog: 60%, bird: 30%."),
                        glm.Part(inline_data=glm.Blob(mime_type='image/png', data=img_byte_arr)),
                    ])
                    response = model.generate_content(content)
                    analysis_text = response.text
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