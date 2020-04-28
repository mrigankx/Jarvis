"""
Created on Fri Apr  3 18:43:54 2020
@author: Mriganka Goswami
"""
import logging.config
import re as regex
import sys
import time
from typing import List
import pyowm
import wikipedia
import os
from datetime import datetime
import random
import pyttsx3
import requests as rq
import speech_recognition as sr
from bs4 import BeautifulSoup
from pygame import mixer
from selenium.webdriver import Firefox

logging.config.fileConfig('logger.config')
logger = logging.getLogger('Admin_Client')
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)
recog = sr.Recognizer()
mic = sr.Microphone()

greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']
question = ['how are you', 'how are you doing']
var3 = ['time']
cmdjokes = ['joke','funny']
cmd2 = ['music','songs', 'song']
jokes = ['can a kangaroo jump higher than a house? of course, a house doesn’t jump at all.', 'my dog used to chase people on a bike a lot. it got so bad, finally i had to take his bike away.', 'doctor: im sorry but you suffer from a terminal illness and have only 10 to live.patient: what do you mean, 10? 10 what? months? weeks?!"doctor: nine.']
cmd4 = ['open youtube', 'i want to watch a video']
cmd5 = ['weather']
exitCmd = ['exit', 'close', 'goodbye', 'nothing']
cmd7 = ['what is your color', 'what is your colour', 'your color', 'your color?']
colrep = ['right now its rainbow', 'right now its transparent', 'right now its non chromatic']
cmd8 = ['what is you favourite colour', 'what is your favourite color']
cmd9 = ['thank you']
rep9 = ['youre welcome', 'glad i could help you']
webSearch: List[str] = ['search', 'web', 'firefox']

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def listenAudio():
    required = -1
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "External" in name:
            required = index
    print('say now')
    with sr.Microphone(device_index=required) as source:
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source, phrase_time_limit=5)
    try:
        givenInput = recog.recognize_google(audio)
        return str(givenInput).lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        logger.error("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))

def validateCommand(query, givenList):
    flag = False
    query = query.split()
    for word in query:
        for gword in givenList:
            if(word == gword):
                flag = True
    return flag

def wishMe():
    hour = int(datetime.now().hour)
    if (hour >= 0 and hour < 12):
        return "Good morning!"
    elif (hour >= 12 and hour <= 16):
        return "Good afternoon!"
    else:
        return "Good evening!"

def setPassword():
    speak("please say the master password")
    tPass = listenAudio()
    print(tPass)
    mfile = open('master.txt','r')
    masterPass = mfile.readline()
    mfile.close()
    if(tPass == masterPass):
        speak("setting new passcode.... say the new passcode")
        npass = listenAudio()
        try:
            file = open('passcode.txt', "w")
            file.write(npass)
            file.close()
            logger.debug("passcode changed successfully.")
            speak('I Successfully set your passcode....restart the agent')
        except Exception as e:
            logger.error("Exception in passcode changing. message: " + str(e))
            speak('Unable to change passcode.')
    else:
        speak('invalid master password.....exiting')
        sys.exit()
        logger.debug("invalid master password")

def authUser(rpass, pcode):
    if (pcode == rpass):
        speak("Passcode matched.... ")
        logger.debug("in authUser().Passcode matched & agent activated.")
        greeting = random.choice(greetings)
        wish = greeting + wishMe()
        speak(wish)
        processRequests()
    else:
        speak("Invalid passcode.....Exiting.")
        logger.error("Invalid Passcode.Exiting.")
        sys.exit()

def processRequests():
    while (1):
        try:
            time.sleep(2)
            speak('Listening now')
            logger.debug('Listening......')
            query = listenAudio()
            if (query == None):
                query = ''
            logger.debug('query: ' + str(query))
            processCommands(query)
        except Exception as e:
            speak("sorry.....unable to process...say again")
            print(str(e))
            logger.exception(str(e))

def processCommands(query):
    if (validateCommand(query, webSearch)):
        comp = regex.compile(r'(firefox|web)\s*([\w\s]*)')
        match = regex.search(comp, query)
        try:
            squery = match.group(2)
        except AttributeError:
            squery = ''
        squery = squery.replace('about', '').replace(' ', '+')
        url = 'https://www.google.com/search?q=' + squery
        openFirefox(url)
    elif(query == 'change passcode'):
        setPassword()
    elif (((r'tell' in query) and (r'something' in query)) or ((r'say' in query) and (r'something' in query))):
        comp = regex.compile(r'(something\s*about)\s*([\w\s]+)')
        match = regex.search(comp, query)
        try:
            getDataFromWiki(match)
        except AttributeError:
            speak('unable to process your request now')
            logger.exception("Exception in 'say something'")
    elif validateCommand(query,var3):
        now = datetime.now()
        speak(now.strftime("The time is %H:%M"))

    elif (query == 'shutdown pc'):
        os.system("shutdown /s /t 1")

    elif (query == 'restart pc'):
        os.system("shutdown /r /t 1")

    elif query in question:
        speak('I am fine')

    elif query in cmd9:
        speak(random.choice(rep9))

    elif query in cmd7:
        speak('It keeps changing every second')

    elif query in cmd8:
        speak(random.choice(colrep))
        speak('It keeps changing every second')
    elif validateCommand(query, cmd5):
        owm = pyowm.OWM('57a134899fde0edebadf307061e9fd23')
        observation = owm.weather_at_place('Barpeta, IN')
        observation_list = owm.weather_around_coords(26.511885, 91.180901)
        w = observation.get_weather()
        w.get_wind()
        w.get_humidity()
        w.get_temperature('celsius')
        speak(w.get_wind())
        speak('humidity')
        speak(w.get_humidity())
        speak('temperature')
        speak(w.get_temperature('celsius'))
    elif validateCommand(query,cmd2):
        mixer.init()
        mixer.music.load("song.wav")
        mixer.music.play()

    elif ((r'open' in query) and (r'file explorer' in query)):  # open [fodername] inside [name of drive] drive in file explorer
        comp = regex.compile(r'(open)\s*([\w\s]*)\s*inside\s*([\w])\s')
        match = regex.search(comp, query)
        try:
            drivePath = match.group(3)
            folderPath = match.group(2)
        except:
            speak("Drive name is missing.....try again")
            logger.exception("Drive name missing in 'open drive'")
        path = drivePath + ":/" + folderPath + "/"
        path = os.path.realpath(path)
        os.startfile(path)
    elif ((r'news' in query) and (r'headlines' in query)):
        speak("fetching headlines from IndiaToday")
        url = 'https://www.indiatoday.in/top-stories'
        getHeadines(url)
    elif validateCommand(query, cmdjokes):
        speak(random.choice(jokes))

    elif (query in exitCmd):
        sys.exit()
    else:
        speak("sorry....invalid voice command...say again")


def getHeadines(url):
    response = rq.get(url)
    status_code = response.status_code
    if (status_code == 200):
        topNewsHeadlines(response)
    else:
        speak("Error in fetching data from internet")
        logger.error("error in fetching data")


def topNewsHeadlines(response):
    elems = []
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in range(1, 11):
        selector = '#content > div.view.view-category-wise-content-list.view-id-category_wise_content_list.view-display-id-section_wise_content_listing.view-dom-id-.custom > div.view-content > div:nth-child(' + str(
            i) + ') > div.detail > h2 > a'
        selected = soup.select(selector)
        if (len(selected) and selected[0].text != '\n'):
            selected = selected[0].text
            elems.append(selected)
    for i in range(len(elems)):
        news = str(i + 1) + '..........' + elems[i]
        speak(news)


def getDataFromWiki(match):
    squery = match.group(2)
    gotText = wikipedia.summary(squery)
    gotText = regex.sub('(\/[\w]+\/)', '', gotText)
    gotText = regex.sub('(\[[\d]+\])', '', gotText)
    gotText = regex.sub('[^A-Za-z0-9\s\(\)\-\,\.]+', '', gotText)
    gotText = gotText.replace('\n', '')
    speak(gotText)

def openFirefox(url):
    browser = Firefox()
    browser.get(url)
    xquery = 'running'
    while (xquery != 'close browser'):
        xquery = listenAudio()
        if (xquery == 'close browser'):
            browser.close()


try:
    speak("Agent started")
    logger.info("Agent started")
    file = open('passcode.txt', 'r')
    readFile = file.readline()
    file.close()
    if (len(readFile) == 0):
        setPassword()
    else:
        speak('Say the passcode')
        passcode = listenAudio()
        logger.debug(passcode)
        speak('Processing passcode')
        authUser(readFile, passcode)
except Exception as e:
    print(str(e))
    logger.exception("Exception in main function(before authentication). message: " + str(e))
finally:
    logging.shutdown()
