# pipeline/image_generator.py
from PIL import Image
from io import BytesIO
from pipeline.stable_diffusion_utils import query_stable_diffusion

def generate_image(prompt) -> bytes:
    
    response = query_stable_diffusion(prompt)
    
    img = Image.open(BytesIO(response.content))
    img = img.resize((768, 768))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()  # return image bytes




