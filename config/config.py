import soundfile as sf
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Получение интерфейса для управления громкостью
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Загрузка звуковых файлов
WakeUp, fs = sf.read('Sound/WakeUp.wav')  # Звук включения
Stop, fs = sf.read('Sound/Stop.wav')      # Звук выключения

# Время в секундах для прослушивания
time = 5

# Глобальные переменные для уровня громкости
global MIN_VOL
global MAX_VOL
global VOLUME
VOLUME = volume.GetMasterVolumeLevel()
MIN_VOL = volume.GetVolumeRange()[0]
MAX_VOL = volume.GetVolumeRange()[1]