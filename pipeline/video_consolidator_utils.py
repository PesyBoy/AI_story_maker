import os
import re
import tempfile
from moviepy import VideoFileClip, concatenate_videoclips, AudioFileClip, ImageClip, vfx, audio


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1

# --- CONFIG ---
def video_consolidator(supabase_client, videos_folder, audio_path, consolidated_folder):
    CROSSFADE_DURATION = 1  # seconds
    OUTPUT_FILENAME = "final_video.mp4"

    # Download audio to temp file
    audio_resp = supabase_client.storage.from_("stories").download(audio_path)
    

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_temp:
        audio_temp.write(audio_resp)
        audio_temp_path = audio_temp.name

    audio_clip = AudioFileClip(audio_temp_path)
    audio_duration = audio_clip.duration

    # List videos in Supabase folder
    video_files_resp = supabase_client.storage.from_("stories").list(videos_folder)

    video_filenames = sorted(
        [f['name'] for f in video_files_resp if f['name'].lower().endswith(('.mp4', '.mov', '.avi', '.webm'))],
        key=lambda x: extract_number(os.path.basename(x))
    )

    temp_video_files = []
    clips = []
    # Download videos as temp files & open VideoFileClip
    for vid_name in video_filenames:
        vid_resp = supabase_client.storage.from_("stories").download(f"{videos_folder}/{vid_name}")

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as vid_temp:
            vid_temp.write(vid_resp)
            vid_temp_path = vid_temp.name
            temp_video_files.append(vid_temp_path)

        clips.append(VideoFileClip(vid_temp_path))

    num_clips = len(clips)
    avg_target_duration = audio_duration / num_clips
    adjusted_clips = []

    for clip in clips:
        if clip.duration < avg_target_duration:
            n_repeats = int(avg_target_duration // clip.duration) + 1
            adjusted_clip = concatenate_videoclips([clip] * n_repeats).subclipped(0, avg_target_duration)
        elif clip.duration > avg_target_duration:
            adjusted_clip = clip.subclipped(0, avg_target_duration)
        else:
            adjusted_clip = clip
        adjusted_clips.append(adjusted_clip)

    for i in range(1, len(adjusted_clips)):
        adjusted_clips[i] = adjusted_clips[i].with_start(adjusted_clips[i - 1].end - CROSSFADE_DURATION)

    final_consolidated = concatenate_videoclips(adjusted_clips, method="compose", padding=-CROSSFADE_DURATION)
    final_video = merge_audio_to_video(final_consolidated, audio_clip)
    # final_video = final_video.set_audio(audio_clip)


    # Clean up temp downloaded video files and audio
    for temp_vid in temp_video_files:
        os.remove(temp_vid)
    os.remove(audio_temp_path)

    # Upload consolidated video back to Supabase
    
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_vid:
        temp_video_path = temp_vid.name
    final_video.write_videofile(temp_video_path, codec="libx264", audio_codec="aac")
    
    consolidated_supabase_path = f"{consolidated_folder}/{OUTPUT_FILENAME}"
    upload_resp = supabase_client.storage.from_("stories").upload(
        consolidated_supabase_path, 
        temp_video_path,
        file_options={"content-type": "video/mp4"}
        )

    

    # Close all clips
    for clip in clips + adjusted_clips:
        clip.close()
    audio_clip.close()
    final_consolidated.close()
    final_video.close()



    return consolidated_supabase_path


def merge_audio_to_video(video, audio):

    video_duration = video.duration
    audio_duration = audio.duration

    if audio_duration > video_duration:
        freeze_duration = audio_duration - video_duration
        last_frame = video.get_frame(video_duration - 0.04)
        freeze_clip = ImageClip(last_frame).with_duration(freeze_duration).with_fps(video.fps).with_audio(None)
        extended_video = concatenate_videoclips([video, freeze_clip])
        print(f"Extending video by {freeze_duration:.2f} seconds to match audio.")
    else:
        extended_video = video.subclipped(0, audio_duration)
        print(f"Trimming video to {audio_duration:.2f} seconds to match audio.")

    final_video = extended_video.with_audio(audio.with_duration(extended_video.duration))

    extended_video.close()

    return final_video