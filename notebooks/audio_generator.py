import io
import numpy as np
import soundfile as sf
from gtts import gTTS
import ffmpeg

def text_to_audio(text: str, sr: int = 16000):
    """
    Convert text to audio (returns NumPy array + sample rate, not saved).
    
    Args:
        text (str): Input text
        sr (int): Sample rate (default 16kHz)
    
    Returns:
        tuple: (audio numpy array, sample rate)
    """
    # Generate MP3 in memory
    tts = gTTS(text, lang="en")
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Decode MP3 -> WAV PCM using ffmpeg
    out, _ = (
        ffmpeg
        .input("pipe:0")
        .output("pipe:1", format="wav", ar=sr, ac=1)
        .run(input=mp3_fp.read(), capture_stdout=True, capture_stderr=True)
    )

    # Convert to numpy array
    audio_bytes = io.BytesIO(out)
    audio, sr = sf.read(audio_bytes, dtype="float32")

    return audio, sr