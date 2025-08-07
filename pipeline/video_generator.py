from pipeline.stable_diffusion_utils import query_video_diffusion

def generate_video(image_bytes: bytes) -> bytes:
    response = query_video_diffusion(image_bytes)

    return response.content
