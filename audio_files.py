from elevenlabslib import *
from api_config import ELEVENLABS_API
import pydub
import pydub.playback
import io

def play(bytesData):
    sound = pydub.AudioSegment.from_file_using_temporary_files(io.BytesIO(bytesData))
    pydub.playback.play(sound)
    return

# Use your own API key through config.py
user = ElevenLabsUser(ELEVENLABS_API)
if ELEVENLABS_API == None:
    raise ValueError("Make sure to enter your own ElevenLabs API key as a string in config.py")

# Fill in the name of the voice you want to use. ex: "Adam" or "Rachel"
voice = user.get_voices_by_name("Adam")[0]

# Test: play(voice.generate_audio_bytes("Hello world, this is test audio"))
