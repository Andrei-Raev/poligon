from core import MainCore
from lib import lib
import speech_recognition as sr
import os
import sys
import webbrowser
import win32com.client as wincl

# MainCore.talk('Загрузка завершена...')
mc = MainCore()
l = lib()

while True:
    a = mc.command()
    print(a)
    l.main(a)
