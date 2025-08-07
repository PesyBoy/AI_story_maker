# pipeline/story_generator.py
from pipeline.mistral_utils import query_mistral


def generate_story_idea(story_requested):
    prompt = (
        f"Write a single, imaginative, and concise story about {story_requested}. "
        "Do not include a title, headings, or any introductory phrases. "
        "Make it short like maybe 2-3 minutes read"
        "Return the story as clean, natural text with standard punctuation only. Avoid symbols, special characters, or formatting."
    )
    return query_mistral(prompt)

def generate_titles(story_idea):
    prompt = (
        f"Based on this idea, generate 1 engaging story title:\n\nIdea: {story_idea}"
        "Avoid giving more than 1 title. Do not include any unnecessary instructions, symbols, or metadata—just the title in words."
    )
    return query_mistral(prompt)
