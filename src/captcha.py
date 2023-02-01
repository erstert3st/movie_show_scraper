import speech_recognition  as sr
from pydub import AudioSegment
import urllib.request

class captcha(object):
    def captchaSolver(self, url):
        urllib.request.urlretrieve(url, "audio.mp3")  # Ask why
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("song.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("song.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio)