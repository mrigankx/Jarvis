import pyttsx3
import speech_recognition as sr
from LoggingFile import *


class SpeechProcess:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
    recog = sr.Recognizer()
    mic = sr.Microphone()
    logg = LoggingFile()
    logger = logg.logVal()

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def listenAudio(self):
        required = -1
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "External" in name:
                required = index
        if (required == -1):
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if "Internal" in name:  # (without earphone mic)
                    required = index
        print('say now')
        with sr.Microphone(device_index=required) as source:
            self.recog.adjust_for_ambient_noise(source)
            audio = self.recog.listen(source, phrase_time_limit=5)
        try:
            givenInput = self.recog.recognize_google(audio)
            return str(givenInput).lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.logger.error(
                "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.logger.error(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

    def listenAudioLong(self):
        required = -1
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "External" in name:
                required = index
        if (required == -1):
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if "Internal" in name:  # (without earphone mic)
                    required = index
        print('say now')
        with sr.Microphone(device_index=required) as source:
            self.recog.adjust_for_ambient_noise(source)
            audio = self.recog.listen(source, phrase_time_limit=10)
        try:
            givenInput = self.recog.recognize_google(audio)
            return str(givenInput).lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.logger.error(
                "Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.logger.error(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
