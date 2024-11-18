from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import sys
import json

model = Model(r'C:\Users\vahl_\Projects\STT\model')
recognizer = KaldiRecognizer(model, 16000)

#recognize the microphone
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        print(recognizer.Result)