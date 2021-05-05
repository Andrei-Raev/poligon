import os
import sys
import webbrowser
import speech_recognition as sr
import win32com.client as wincl


class MainCore(object):
    speak = wincl.Dispatch("SAPI.SpVoice")
    work = True

    def __init__(self):
        pass

    def talk(self, words):
        print(words)  # Дополнительно выводим на экран
        MainCore.speak.Speak(words)  # Проговариваем слова

    def command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Говорите")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            zadanie = r.recognize_google(audio, language="ru-RU").lower()
            print("Вы сказали: " + zadanie)
        except sr.UnknownValueError:
            self.talk("Я вас не поняла")
            zadanie = self.command()
        return zadanie
