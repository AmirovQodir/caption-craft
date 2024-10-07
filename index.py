import speech_recognition as sr
from moviepy.editor import VideoFileClip
import pysrt

# Step 1: Extract audio from video
video = VideoFileClip("video1.mp4")
video.audio.write_audiofile("test_audio.wav")

# Get the duration of the audio in seconds
audio_duration = video.audio.duration

# Step 2: Perform speech recognition
recognizer = sr.Recognizer()
with sr.AudioFile("test_audio.wav") as source:
    audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)

# Step 3: Function to split text into smaller parts
def split_text_into_segments(text, max_words_per_segment=10):
    words = text.split()
    segments = [' '.join(words[i:i+max_words_per_segment]) for i in range(0, len(words), max_words_per_segment)]
    return segments

# Step 4: Create SRT format subtitles with dynamic timestamp logic
def create_srt_file(transcribed_text, audio_duration, output_file="output_subtitles.srt"):
    segments = split_text_into_segments(transcribed_text)
    subs = pysrt.SubRipFile()

    segment_duration = audio_duration / len(segments)  # Calculate duration per segment
    start_time = 0  # Start time in seconds

    for i, segment in enumerate(segments, start=1):
        # Ensure the last subtitle ends at the audio duration
        if i == len(segments):
            end_time = audio_duration
        else:
            end_time = start_time + segment_duration

        # Create subtitle timestamps
        start_srt = pysrt.SubRipTime(seconds=start_time)
        end_srt = pysrt.SubRipTime(seconds=end_time)

        # Add subtitle to SRT
        sub = pysrt.SubRipItem(i, start=start_srt, end=end_srt, text=segment)
        subs.append(sub)

        start_time = end_time  # Update start time for the next segment

    # Save the SRT file
    subs.save(output_file, encoding='utf-8')
    print(f"SRT file '{output_file}' created successfully.")

# Step 5: Generate and save the SRT file
create_srt_file(text, audio_duration)
