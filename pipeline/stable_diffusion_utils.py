import requests
import os
import io
from dotenv import load_dotenv
import base64
import time
from PIL import Image
from io import BytesIO

load_dotenv()


def query_stable_diffusion(prompt: str, max_retries=3) -> requests.Response:

    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise ValueError("STABILITY_API_KEY not found in .env file")

    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "authorization": f"Bearer {api_key}",
        "accept": "image/*"
    }

    data = {
        "prompt": prompt,
        "output_format": "png",
    }
    
    files = {"none": ''}

    for attempt in range(max_retries):
        response = requests.post(url=url, headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            return response
        
        elif response.status_code == 504:
            wait_time = 2 ** attempt  # exponential backoff: 1, 2, 4 seconds
            print(f"Timeout error (504) on attempt {attempt + 1}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Error generating image: {response.status_code} - {response.text}")

    raise Exception("Max retries reached with timeout error (504).")




def query_video_diffusion(image_bytes: bytes):
    
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise ValueError("STABILITY_API_KEY not found in environment")

    url_post = "https://api.stability.ai/v2beta/image-to-video"
    
    img_file = io.BytesIO(image_bytes)
    response = requests.post(
        url_post,
        headers={"authorization": f"Bearer {api_key}"},
        files={"image": img_file},
        data={
            "seed": 0,
            "cfg_scale": 5.0,
            "motion_bucket_id": 100  # Controls motion intensity (0–255)
        }
    )

    if response.status_code != 200:
        raise Exception(f"Error during submission: {response.status_code} - {response.text}")
    
    generation_id = response.json().get("id")
    print(f"[✓] Video generation started. ID: {generation_id}")

    # Step 2: Poll until video is ready
    url_get = f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}"
    
    while True:
        result_response = requests.request("GET",
            url_get,
            headers={
                "accept": "video/*",
                "authorization": f"Bearer {api_key}" 
            },
            timeout = 60
        )

        if result_response.status_code == 202:
            print("[-] Generation in progress. Waiting 10 seconds...")
            time.sleep(10)
        elif result_response.status_code == 200:
            print(f"[✓] Video Generated")
            return result_response
        else:
            raise Exception(f"Error during polling: {result_response.status_code} - {result_response.text}")
