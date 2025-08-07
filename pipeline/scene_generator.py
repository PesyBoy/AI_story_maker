# pipeline/scene_generator.py
from pipeline.mistral_utils import query_mistral
import time
from mistralai.models import sdkerror


def generate_scenes(story_idea, max_retries = 5):
    prompt = (
                f"Based on the following story idea:\n\n"
                f"\"{story_idea}\"\n\n"
                f"Break this story into about 10 short scenes. For each scene, describe what happens in 3-5 sentences. "
                f"Make sure the scenes are related to the story. "
                f"Use rich, vivid visual language to describe the setting and events, ensuring the scenes can be directly illustrated. "
                f"Make sure the descriptions are related to the story. "
                f"and will visually match the narration the viewer will hear. "
                f"Make sure each scene description starts with a dash (-) so they can be easily separated later. "
            )
    for attempt in range(max_retries):
        try:
            scene_text = query_mistral(prompt)
            break
        except sdkerror.SDKError as e:
            if "429" in str(e):
                wait_time = 2 ** attempt  # exponential backoff
                print(f"[!] Rate limit hit. Waiting {wait_time}s before retrying...")
                time.sleep(wait_time)
            else:
                raise
    else:
        raise RuntimeError("Max retries exceeded due to rate limiting.")
    
    # Parse scenes that start with '- '
    scenes = [line[2:].strip() for line in scene_text.split("\n") if line.strip().startswith("- ")]
    return scenes
