from vosk import Model, KaldiRecognizer
import json
import pyaudio
from datetime import datetime
from config.phase import recognize_command, VA_ANSWER_LIST
from tts.tts import speak
import random
from utils.sound import hand_volume
from pydub import AudioSegment
import config.config as cfg
import sounddevice as sd
import subprocess
# model = Model('model_small')
model = Model('model_small')
p = pyaudio.PyAudio()
rec = KaldiRecognizer(model, 16000)

def normalize_volume(data):
    audio = AudioSegment(data, sample_width=2, frame_rate=16000, channels=1)
    normalized_audio = audio.apply_gain(-audio.max_dBFS + 3)
    return normalized_audio.raw_data

def va_listen(time):
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1200)
    print("Listening ...")
    start_time = datetime.now()
    data = b''
    sd.play(cfg.WakeUp, cfg.fs)
    sd.wait()
    while (datetime.now() - start_time).total_seconds() < time:
        chunk = stream.read(1200, exception_on_overflow=False)
        if(chunk):
            data = b''
            data += chunk
            normalized_data = normalize_volume(data)
            if (rec.AcceptWaveform(chunk)):
                answer = json.loads(rec.Result())
                if answer["text"]:
                    data = recognize_command(answer["text"])
                    if data:
                        answer = VA_ANSWER_LIST[data]
                        if answer.get("cmd"):
                            command_str = answer.get("cmd")
                            command_list = command_str[0].split()  # Assuming command_str is a list with one string element
                            print(command_list)
                            subprocess.Popen(command_list)
                        if answer.get("command"):
                            speak(random.choice(answer["command"]))
                    yield data
                    rec.Reset()
    print("Stop Listening ...")

if __name__ == "__main__":
    for text in va_listen(9600):
        print(text)