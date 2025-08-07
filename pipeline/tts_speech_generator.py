from TTS.api import TTS
from pathlib import Path
from pydub import AudioSegment
import os
import re
import numpy as np
from io import BytesIO

# Load the TTS model (you can change to another pre-trained model)
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False, gpu=False)


def split_text(text, max_chars=300):
    """Split text into chunks of roughly max_chars, preserving sentence boundaries."""
    sentences = re.split(r'(?<=[.!?]) +', text)  # Split on sentence endings
    chunks = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        
        if not sentence:
            continue
        
        elif len(current) + len(sentence) <= max_chars:
            current += " " + sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            current = sentence
    if current:
        chunks.append(current.strip())
    return chunks


def numpy_to_audiosegment(audio_np, sample_rate):
    
    if isinstance(audio_np, list):
        audio_np = np.array(audio_np)
    # Normalize to 16-bit PCM values
    audio_int16 = (audio_np * 32767).astype(np.int16)
    # Create AudioSegment from raw audio data
    return AudioSegment(
        audio_int16.tobytes(), 
        frame_rate=sample_rate, 
        sample_width=2,  # 2 bytes for int16
        channels=1
    )
    
def generate_narration(story_text) -> bytes:
    chunks = split_text(story_text, max_chars=300)
    narration = AudioSegment.empty()

    sample_rate = 22050  # common for LJSpeech VITS model
    narration = AudioSegment.empty()
    for i, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk or len(chunk) < 10:
            print(f"Skipping short chunk: {chunk}")
            continue
        
        # Generate numpy audio from TTS
        audio_np = tts.tts(text=chunk, speaker=tts.speakers[0] if tts.speakers else None, return_type="numpy")

        # Convert numpy audio to pydub AudioSegment
        audio_seg = numpy_to_audiosegment(audio_np, sample_rate)
        
        # Concatenate chunk audio to narration
        narration += audio_seg
        

        # narration += AudioSegment.from_wav(audio_np)

    # Export final narration to bytes buffer
    buffer = BytesIO()
    narration.export(buffer, format="wav")
    buffer.seek(0)

    return buffer.read()

