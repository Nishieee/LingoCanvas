import streamlit as st
import requests
from googletrans import Translator
from PIL import Image
import io

# Backend URL
backend_url = "http://127.0.0.1:8000"

# App Title and Description
st.title("LingoCanvas 🎨🌍")
st.markdown(
    """
    Generate stunning AI-generated images from text prompts in **any language**! 🌍
    
    1. Type your prompt in your preferred language.
    2. We'll translate it for you and generate the image.
    3. Enjoy your masterpiece! 🎨
    """
)

# Initialize the Translator
translator = Translator()

# Input Section
st.header("✨ Enter Your Prompt")
prompt = st.text_input(
    "Type a prompt (e.g., 'a sunset over a mountain' or 'सूर्यास्त का दृश्य पर्वत पर')",
    placeholder="Write your creative idea here..."
)

# Generate Button
if st.button("Generate Image 🚀"):
    if prompt:
        with st.spinner("Translating your prompt and generating the image... ⏳"):
            try:
                # Translate the prompt to English
                translated_prompt = translator.translate(prompt, dest="en").text
                
                # Show the translated prompt
                st.markdown(f"**Translated Prompt (to English):** `{translated_prompt}`")

                # Send the translated prompt to the backend
                response = requests.post(f"{backend_url}/generate-image/", json={"text": translated_prompt})
                
                if response.status_code == 200:
                    st.success("🎉 Image generated successfully!")
                    
                    # Retrieve and display the image
                    image_response = requests.get(f"{backend_url}/download-image/")
                    if image_response.status_code == 200:
                        img = Image.open(io.BytesIO(image_response.content))
                        st.image(img, caption="Your AI-Generated Image", use_container_width=True)
                    else:
                        st.error("❌ Failed to download the image.")
                else:
                    error_message = response.json().get('error', 'Unknown error occurred.')
                    st.error(f"❌ Error: {error_message}")
            except Exception as e:
                st.error(f"❌ Translation or image generation failed: {str(e)}")
    else:
        st.warning("⚠️ Please enter a prompt to generate the image.")

# Footer
st.markdown(
    """
    ---
    **Powered by** [Stable Diffusion](https://github.com/CompVis/stable-diffusion) | **Translations by** [Google Translator](https://pypi.org/project/googletrans/)
    """
)
