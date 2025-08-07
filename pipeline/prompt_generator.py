# pipeline/prompt_generator.py
from pipeline.mistral_utils import query_mistral

def generate_image_prompt(scene_descriptions):
    prompts = []
    for scene in scene_descriptions:
        
        prompt = (
            f"Write a highly detailed and visually rich prompt (300 words or less) for Stable Diffusion XL, based on the following scene:\n"
            f"scene = \"{scene}\"\n\n"
            f"The prompt should include specific objects, characters, setting details, lighting, atmosphere, and style. "
            f"Use an art style suitable for the story. Ensure the description is clear, concise, and directly translatable into a single coherent image. "
            f"Avoid repeating the scene text. Do not include any unnecessary instructions or metadata—just the visual description for the image generation model. "
            f"include characters, animals, and object in the image when they are in the scenes. "
            f"Keep the object and characters simple to avoid overloading the image. "
            f"Make sure the prompt and scene description match. "
        )
        result = query_mistral(prompt)

        
        while len(result) > 1500:
            prompt = (
                "shorten this sable diffusion prompt while ensuring the most important details are still in \n"
                f"prompt = {result}\n"
                "Avoid repeating the scene text. Do not include any unnecessary instructions or metadata—just the new prompt. "
            )
            result = query_mistral(prompt)
            
        prompts.append(result)
    
    return prompts
