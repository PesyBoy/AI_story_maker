from dotenv import load_dotenv
from pipeline.story_generator import generate_story_idea, generate_titles
from pipeline.scene_generator import generate_scenes
from pipeline.prompt_generator import generate_image_prompt
from pipeline.image_generator import generate_image
from pipeline.video_generator import generate_video
from pipeline.video_consolidator_utils import video_consolidator, merge_audio_to_video
from pipeline.tts_speech_generator import generate_narration
from PIL import Image
import json, os


load_dotenv()
# def fake_stable_diffusion(prompt):
#     return Image.new('RGB', (512, 512), color = 'white')

# Run full pipeline
def run_pipeline(story_id="story_004"):
    
    #Define directory
    output_dir = f"/Users/pesy/Projects/professional/AI_story_maker/{story_id}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/videos", exist_ok=True)
    os.makedirs(f"{output_dir}/audios", exist_ok=True)
    os.makedirs(f"{output_dir}/final", exist_ok=True)
    os.makedirs(f"{output_dir}/consolidated", exist_ok=True)
    os.makedirs(f"{output_dir}/data", exist_ok=True)
    
  

    # Generate the story, title, scenes and prompts to generate images for the scenes
    story_rquested = "write an exiting story about a protagonist who is good at stealing"
    story_idea = generate_story_idea(story_rquested)
    story_title = generate_titles(story_idea)
    full_story = f"{story_title} \n {story_idea}"
    scenes = generate_scenes(story_idea)
    image_prompts = generate_image_prompt(scenes)

    results = {
        "idea": story_idea,
        "title": story_title,
        "scenes": scenes,
        "image_prompts": image_prompts
    }
    

    # Generate images from scene prompts
    image_paths = []
    for i, img_prompt in enumerate(image_prompts):
        save_path = f"{output_dir}/images/scene_{i}.png"
        img_prompt = image_prompts[i]
        img_path = generate_image(img_prompt, save_path)
        image_paths.append(img_path)

    results["image_paths"] = image_paths
       
    # Generate videos from the images 

    video_paths = []
    for i, img_path in enumerate(image_paths):
        save_path = f"{output_dir}/videos/video_{i}.mp4"
        video_path = generate_video(img_path, save_path)
        video_paths.append(video_path)
    
    results["video_paths"] = video_paths
    
    audio_path = generate_narration(full_story, f"{output_dir}/audios")
    results["audio_path"] = audio_path
    
    consolidated_video_path = video_consolidator(f"{output_dir}/videos", audio_path,  f"{output_dir}/consolidated")
    results["consolidated_video"] = consolidated_video_path
    
    
    final_video_path = merge_audio_to_video(consolidated_video_path, audio_path, f"{output_dir}/final")
    results["final_video"] = final_video_path

    
    # Save results as json
    with open(f"{output_dir}/data/story.json", "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    run_pipeline()
