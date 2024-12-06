from googletrans import Translator
from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import DiffusionPipeline
from fastapi.responses import FileResponse

# Initialize the FastAPI app
app = FastAPI()

# Load the Stable Diffusion model
pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

# Initialize the translator
translator = Translator()

# Input schema
class Prompt(BaseModel):
    text: str

@app.post("/generate-image/")
def generate_image(prompt: Prompt):
    try:
        # Translate the prompt to English
        translated_prompt = translator.translate(prompt.text, dest="en").text
        
        # Generate the image
        image = pipe(translated_prompt).images[0]
        
        # Save the generated image
        output_path = "generated_image.png"
        image.save(output_path)
        
        return {"message": "Image generated successfully", "image_path": output_path}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download-image/")
def download_image():
    file_path = "generated_image.png"
    return FileResponse(file_path, media_type="image/png", filename="generated_image.png")
