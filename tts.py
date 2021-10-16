# Google Text to Speech API
from gtts import gTTS
from random import random
# Import Speech Recognition
import speech_recognition as sr

# Library to play an mp3 using python
from playsound import playsound


def recordText():
    # ----- this section is inspired from this website -----
    # https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__main__.py
    # Setup recognizer and microphone
    r = sr.Recognizer()
    m = sr.Microphone()
    text = ""
    # Ajust Ambient Noise
    with m as source:
        r.adjust_for_ambient_noise(source)
    print('Speak!\n')

    # Listen to microphone
    with m as source:
        audio = r.listen(source)

    # Transform speech to text
    try:
        text = r.recognize_google(audio, language="Fr-CA")
        print("Text entered : {}".format(text))
    except:
        print('Sorry. Try again')
    # ----------
    return text.capitalize()


def playText(text):
    # Passing the text and language to the engine
    # to transform it back into voice
    compteur = random()
    myobj = gTTS(text=text, lang="fr", slow=False)

    # Saving the converted audio in a mp3 file
    myobj.save("speech"+str(compteur)+".mp3")

    # Playing the converted file
    playsound("speech"+str(compteur)+".mp3", True)
