import pyaudio
import pvporcupine
from pvrecorder import PvRecorder
import sounddevice as sd
from tts.stt_vosk import va_listen
import config.config as cfg
import os
import platform
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Получение интерфейса для управления громкостью
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

p = pyaudio.PyAudio()

# Создание экземпляра Porcupine
porcupine = pvporcupine.create(
    access_key="",
    model_path="config/porcupine_params_ru.pv",
    keyword_paths=["config/ru_windows_v3_0_0.ppn"]
)

# Создание экземпляра записывающего устройства
recorder = PvRecorder(
    frame_length=porcupine.frame_length,
    device_index=0  # поменяйте, если нужно
)

recorder.start()

# Очистка экрана консоли
os.system('cls' if platform.system() == 'Windows' else 'clear')

def back_end():
    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            if result >= 0:
                print("Keyword detected")
                recorder.stop()

                # Получение диапазона громкости и установка уровня громкости
                vol_range = volume.GetVolumeRange()
                min_vol = vol_range[0]
                max_vol = vol_range[1]
                target_vol = cfg.VOLUME - 10
                volume.SetMasterVolumeLevel(max(min_vol, target_vol), None)

                # Получение и обработка голосовых команд
                for text in va_listen(cfg.time):
                    print(text)

                # Сброс уровня громкости и проигрывание звукового сигнала
                volume.SetMasterVolumeLevel(cfg.VOLUME, None)
                sd.play(cfg.Stop, cfg.fs)
                sd.wait()
                recorder.start()

    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        p.terminate()

if __name__ == "__main__":
    back_end()