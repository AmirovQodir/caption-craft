import io
import os
from google.cloud import speech
from moviepy.editor import VideoFileClip
import pysrt

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "verdant-medley-437819-b0-3b7c8d56f83d.json"

# Step 1: Extract audio from video
# video = VideoFileClip("simonbek.mp4")
# video.audio.write_audiofile("test_audio.wav")

# Step 2: Perform speech recognition with timestamps
print('Place wait ...')
def transcribe_audio_with_timestamps(audio_file):
    client = speech.SpeechClient()

    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,  # Enable word timestamps
    )

    response = client.recognize(config=config, audio=audio)

    # Extract words and their timestamps
    words = []
    for result in response.results:
        for word in result.alternatives[0].words:
            words.append((word.word, word.start_time.total_seconds(), word.end_time.total_seconds()))
    
    return words

# Step 3: Create SRT format subtitles
def create_srt_file_with_timestamps(words, output_file="output_subtitles.srt"):
    subs = pysrt.SubRipFile()

    for i, (word, start, end) in enumerate(words, start=1):
        # Create subtitle timestamps
        start_srt = pysrt.SubRipTime(seconds=start)
        end_srt = pysrt.SubRipTime(seconds=end)

        # Add subtitle to SRT
        sub = pysrt.SubRipItem(i, start=start_srt, end=end_srt, text=word)
        subs.append(sub)

    # Save the SRT file
    subs.save(output_file, encoding='utf-8')
    print(f"SRT file '{output_file}' created successfully.")

# Step 4: Transcribe and generate SRT file
words_with_timestamps = transcribe_audio_with_timestamps("test_audio_mono.wav")
create_srt_file_with_timestamps(words_with_timestamps)