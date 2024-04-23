import pyaudio

def list_mics(p_audio: pyaudio.PyAudio):
    """Print information about all microphones."""
    print('Microphones:')
    for i in range(p_audio.get_device_count()):
        info = p_audio.get_device_info_by_index(i)
        print(f'{i}: {info["name"]}')
