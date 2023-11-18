# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# import pandas as pd


import pyaudio
import wave
file_path = 'C:\Users\HP\Documents\NoMorals'

audio = pyaudio.PyAudio()

stream = audio.open (format = pyaudio.paInt16, channels=1, rate=44100, input= True,frames_per_buffer=1024)

frames = []

try:
    while True:
        data = stream.read (1024)
        frames.append (data)
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open ('Your recording.wave', 'wb')
sound_file.setnchannels (1)
sound_file.setsampwidth (audio.get_sample_size (pyaudio.paInt16))
sound_file.setframerate (44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()


    




