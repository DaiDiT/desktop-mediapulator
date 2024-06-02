from pydub import AudioSegment

import os

def configure_pydub():
    AudioSegment.converter = os.path.join(os.path.dirname(__file__)[:-9], 'bin', 'ffmpeg.exe')
    AudioSegment.ffprobe = os.path.join(os.path.dirname(__file__)[:-9], 'bin', 'ffprobe.exe')