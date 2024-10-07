from pydub import AudioSegment

# Load your stereo audio file
stereo_audio = AudioSegment.from_wav("test_audio.wav")  # Change this to your audio file path

# Convert to mono
mono_audio = stereo_audio.set_channels(1)

# Export the mono audio file
mono_audio.export("test_audio_mono.wav", format="wav")
print("Converted to mono and saved as 'test_audio_mono.wav'.")