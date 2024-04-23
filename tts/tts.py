import pyttsx3

ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Irina"

def speak(what):
    engine = pyttsx3.init()
    
    engine.setProperty('voice', ru_voice_id)
    engine.say(what)

    engine.runAndWait()


def list_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print("Voice:")
        print(" - ID: %s" % voice.id)
        print(" - Name: %s" % voice.name)
        print(" - Languages: %s" % voice.languages)
        print(" - Gender: %s" % voice.gender)
        print(" - Age: %s" % voice.age)

if __name__ == "__main__":
    list_voice()
    speak("Привет, я голосовой ассистент пятница")
