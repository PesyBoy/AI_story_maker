import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from io import BytesIO

from pipeline.story_generator import generate_story_idea, generate_titles
from pipeline.scene_generator import generate_scenes
from pipeline.prompt_generator import generate_image_prompt
from pipeline.image_generator import generate_image
from pipeline.video_generator import generate_video
from pipeline.video_consolidator_utils import video_consolidator, merge_audio_to_video
from pipeline.tts_speech_generator import generate_narration


def run_pipeline(story_request: str, user_story_title: str = "", is_custom_story: bool=False, story_id: str = "story_000", progress_callback=None) -> dict:
    try:
        
        load_dotenv()
        # Your Supabase settings
        api_key = os.environ["MISTRAL_API_KEY"]
        SUPABASE_URL = os.environ["SUPABASE_URL"]  # replace this
        SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_API_KEY"]   # keep this secret
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

        # Generate the story and supporting elements
        
        # Generate Story or use story provided
        if not is_custom_story:
            if progress_callback:
                progress_callback("Step 1: Generating story idea...")
            story_idea = generate_story_idea(story_request)
        else:
            if progress_callback:
                progress_callback("Step 1: Story provided...")
            story_idea = story_request
        
        # Generate Title or use title provided
        if not user_story_title:
            if progress_callback:
                progress_callback("Step 2: Generating title...")
            story_title = generate_titles(story_idea)
        else:
            if progress_callback:
                progress_callback("Step 2: Title provided...")
            story_title = user_story_title
        
        # Concatenate title and story for narration
        full_story = f"{story_title}\n{story_idea}"

        story_text_bytes = full_story.encode('utf-8')
        # story_text_file = BytesIO(story_text_bytes)
        story_text_filename = f"{story_id}/full_story/story.txt"
        upload_response = supabase.storage.from_("stories").upload(story_text_filename, story_text_bytes)
        
        
        # Generate scenes that will be used for images
        if progress_callback:
            progress_callback("Step 3: Generating scenes...")
        scenes = generate_scenes(story_idea)
        for i, scene in enumerate(scenes):
            scene_text_bytes = scene.encode('utf-8')
            # scene_text_file = BytesIO(scene_text_bytes)
            scene_text_filename = f"{story_id}/scenes/scene_{i}.txt"
            upload_response = supabase.storage.from_("stories").upload(scene_text_filename, scene_text_bytes)

        
        # Generate prompt for image generation
        if progress_callback:
            progress_callback("Step 4: Generating image prompts...")
        image_prompts = generate_image_prompt(scenes)

        # Generate images from the prompts
        image_paths = []
        for i, prompt in enumerate(image_prompts):
            if progress_callback:
                progress_callback(f"Step 5.{i+1}/{len(image_prompts)}: Generating image for scene {i+1}...")
            image_bytes = generate_image(prompt)
            image_filename = f"{story_id}/images/scene_{i}.png"
            upload_response = supabase.storage.from_("stories").upload(image_filename, image_bytes)
            image_paths.append(image_filename)

        video_paths = []
    
        for i, image_path in enumerate(image_paths):
            if progress_callback:
                progress_callback(f"Step 5.{i+1}/{len(image_paths)}: Generating video for scene {i+1}...")

            # Download image from Supabase
            file_response = supabase.storage.from_("stories").download(image_path)

            # Convert to PIL Image
            image_bytes = file_response

            # Generate video from image object
            video_filename = f"{story_id}/videos/video_{i}.mp4"
            video_bytes = generate_video(image_bytes)

            # Upload video to Supabase
            upload_response = supabase.storage.from_("stories").upload(
                video_filename,
                video_bytes,
                {"content-type": "video/mp4"}  # optional but recommended
            )
            video_paths.append(video_filename)

        
        # Generate audio
        if progress_callback:
            progress_callback("Step 6: Generating audio...")
        audio_bytes = generate_narration(full_story)
        audio_filename = f"{story_id}/audios/narration.mp3"  # or .wav depending on your format

        upload_response = supabase.storage.from_("stories").upload(audio_filename, audio_bytes)

        
        
        # Consolidate video
        if progress_callback:
            progress_callback("Step 7: Finalizing...")
        final_video_path = video_consolidator(
            supabase,
            videos_folder=f"{story_id}/videos",        # e.g., "123/videos"
            audio_path=f"{story_id}/audios/narration.mp3",
            consolidated_folder=f"{story_id}/final"
        )


        video_public_url = supabase.storage.from_("stories").get_public_url(final_video_path)
        results = {
            "title": story_title,
            "final_video_ui": video_public_url,
        }
       

        return results
    except Exception as e:
        print(f"[Pipeline ERROR] {e}")
        raise
