import ctypes
import logging.config
import os
import random
import re as regex
import smtplib
import time
from datetime import datetime
from tkinter import *
from typing import List

import mysql.connector
import pyowm
import pyttsx3
import requests as rq
import speech_recognition as sr
import wikipedia
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pygame import mixer
from selenium.webdriver import Firefox


class AgentJarvis:
    greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']
    question = ['how are you', 'how are you doing']
    var3 = ['time']
    cmdjokes = ['joke', 'funny']
    cmd2 = ['music', 'songs', 'song']
    jokes = ["can a kangaroo jump higher than a house? of course, a house doesn’t jump at all.",
             'my dog used to chase people on a bike a lot. it got so bad, finally i had to take his bike away.',
             'doctor: im sorry but you suffer from a terminal illness and have only 10 to live.patient: what do you mean, 10? 10 what? months? weeks?!"doctor: nine.']
    cmd4 = ['open youtube', 'i want to watch a video']
    cmd5 = ['weather']
    exitCmd = ['exit', 'close', 'goodbye', 'nothing']
    cmd7 = ['what is your color', 'what is your colour', 'your color', 'your color?']
    colrep = ['right now its rainbow', 'right now its transparent', 'right now its non chromatic']
    cmd8 = ['what is you favourite colour', 'what is your favourite color']
    cmd9 = ['thank you']
    rep9 = ['youre welcome', 'glad i could help you']
    webSearch: List[str] = ['firefox', 'internet', 'browser']
    sound = ['volume', 'sound']
    txtEdit = ['notepad']
    says = ['tell', 'say']
    newsText = ['news', 'headlines']
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
    recog = sr.Recognizer()
    mic = sr.Microphone()
    logging.config.fileConfig('logger.config')
    logger = logging.getLogger('Admin_Client')
    posAnswers = ['yes', 'ok', 'yop']
    negAnswers = ['no', 'never', 'nope']
    mailCmd = ['e-mail', 'mail', 'email']
    mypc = ['pc', 'laptop', 'system', 'computer']
    logoutCmd = ['log', 'sign', 'logout', 'signout']
    mydb = None
    usr = None

    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="jarvis_data")
        except Exception as e:
            self.speak("MySQL not connected")
            self.logger.exception("MySQL not connected.")

    def getDatafromDb(self, Sqlquery):
        mycursor = self.mydb.cursor()
        mycursor.execute(Sqlquery)
        myresult = mycursor.fetchall()
        return myresult

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def listenAudio(self):
        required = -1
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "External" in name:
                required = index
            # if "Internal" in name:#(without earphone mic)
            #     required = index
        print('say now')
        with sr.Microphone(device_index=required) as source:
            self.recog.adjust_for_ambient_noise(source)
            audio = self.recog.listen(source, phrase_time_limit=5)
        try:
            givenInput = self.recog.recognize_google(audio)
            return str(givenInput).lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.logger.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))

    def listenAudioLong(self):
        required = -1
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            if "External" in name:
                required = index
        # if "Internal" in name:#(without earphone mic)
        #     required = index
        print('say now')
        with sr.Microphone(device_index=required) as source:
            self.recog.adjust_for_ambient_noise(source)
            audio = self.recog.listen(source, phrase_time_limit=10)
        try:
            givenInput = self.recog.recognize_google(audio)
            return str(givenInput).lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.logger.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            self.logger.error("Could not request results from Google Speech Recognition service; {0}".format(e))

    def validateCommand(self, query, givenList):
        for word in query:
            for gword in givenList:
                if (word == gword):
                    return True
        return False

    def wishMe(self):
        hour = int(datetime.now().hour)
        if (hour >= 0 and hour < 12):
            return " Good morning!"
        elif (hour >= 12 and hour <= 16):
            return " Good afternoon!"
        else:
            return " Good evening!"

    def setPassword(self):
        self.speak("please say the master password")
        tPass = self.self.listenAudio()
        print(tPass)
        mfile = open('master.txt', 'r')
        masterPass = mfile.readline()
        mfile.close()
        if (tPass == masterPass):
            self.speak("setting new passcode.... say the new passcode")
            npass = self.listenAudio()
            try:
                file = open('passcode.txt', "w")
                file.write(npass)
                file.close()
                self.logger.debug("passcode changed successfully.")
                self.speak('I Successfully set your passcode....restart the agent')
            except Exception as e:
                self.logger.error("Exception in passcode changing. message: " + str(e))
                self.speak('Unable to change passcode.')
        else:
            self.speak('invalid master password.....exiting')
            sys.exit()
            self.logger.debug("invalid master password")

    def authUser(self, rpass, pcode):
        if (pcode == rpass[0][1]):
            self.speak("Passcode matched.... ")
            self.logger.debug("in authUser().Passcode matched & agent activated.")
            greeting = random.choice(self.greetings)
            wish = greeting + " " + rpass[0][0] + self.wishMe()
            self.speak(wish)
            self.usr = rpass[0][0]
            self.processRequests()
        else:
            self.speak("Invalid passcode.....Exiting.")
            self.logger.error("Invalid Passcode.Exiting.")
            sys.exit()

    def processRequests(self):
        while (1):
            try:
                time.sleep(2)
                self.speak('Listening now')
                self.logger.debug('Listening......')
                query = self.listenAudio()
                if (query == None):
                    query = ''
                self.logger.debug('query: ' + str(query))
                self.processCommands(query)
            except Exception as e:
                self.speak("sorry.....unable to process...say again")
                print(str(e))
                self.logger.exception(str(e))

    def processCommands(self, query):
        queryx = query.split()
        queryx = [word for word in queryx if not word in set(stopwords.words('english'))]
        if (self.validateCommand(queryx, self.webSearch)):
            if (r'search' in query):
                self.getInfoWebSearch(query)
            elif (r'go to'):
                comp = regex.compile(r'(go\s*to)\s*([\w\s\.]*)')
                match = regex.search(comp, query)
                try:
                    squery = match.group(2)
                except AttributeError:
                    squery = ''
                url = 'https://' + squery
                self.openFirefox(url)
        elif (query == 'change password'):
            self.setPassword()
        elif (self.validateCommand(queryx, self.says) and (r'something' in query)):
            self.tellInfoFromWiki(query)
        elif self.validateCommand(queryx, self.var3):
            now = datetime.now()
            self.speak(now.strftime("The time is %H:%M"))
        elif self.validateCommand(queryx, self.mailCmd) and self.validateCommand(queryx, ['send']):
            self.sendEmail()
        elif query in self.question:
            self.speak('I am fine')

        elif query in self.cmd9:
            self.speak(random.choice(self.rep9))

        elif query in self.cmd7:
            self.speak('It keeps changing every second')

        elif query in self.cmd8:
            self.speak(random.choice(self.colrep))
            self.speak('It keeps changing every second')
        elif self.validateCommand(queryx, self.cmd5):
            self.getWeatherInfo()
        elif self.validateCommand(queryx, self.cmd2):
            self.playMusic()

        elif (r'open' in query):
            if (r'file explorer' in query):  # open [foldername] inside [name of drive] drive in file explorer
                self.openFileExplorer(query)
            else:
                openApp = self.openAnyApplication(query)
                if (openApp == 'notepad'):
                    self.openNotepad()
                else:
                    self.speak('app not found')

        elif (self.validateCommand(queryx, self.newsText)):
            self.speak("fetching headlines from IndiaToday")
            url = 'https://www.indiatoday.in/top-stories'
            self.getHeadines(url)
        elif self.validateCommand(queryx, self.cmdjokes):
            self.speak(random.choice(self.jokes))

        elif (r'shutdown' in query) and self.validateCommand(queryx, self.mypc):
            os.system("shutdown /s /t 1")

        elif (r'restart' in query) and self.validateCommand(queryx, self.mypc):
            os.system("shutdown /r /t 1")
        elif (r'lock' in query) and self.validateCommand(queryx, self.mypc):
            ctypes.windll.user32.LockWorkStation()

        elif (self.validateCommand(queryx, self.logoutCmd) or (r'out' in query)) and self.validateCommand(queryx,
                                                                                                          self.mypc):
            os.system("shutdown -l")
        elif (query in self.exitCmd):
            sys.exit()
        else:
            self.speak("sorry....invalid voice command...say again")

    def openAnyApplication(self, query):
        app = regex.compile(r'(open)\s*([\w\s]*)')
        match = regex.search(app, query)
        try:
            openApp = match.group(2)
        except:
            self.speak('unable to open the application')
            self.logger.exception("Error in opening application")
            openApp = ''
        return openApp

    def openFileExplorer(self, query):
        comp = regex.compile(r'(open)\s*([\w\s]*)\s*inside\s*([\w])\s')
        match = regex.search(comp, query)
        try:
            drivePath = match.group(3)
            folderPath = match.group(2)
        except:
            self.speak("Drive name is missing.....try again")
            self.logger.exception("Drive name missing in 'open drive'")
        path = drivePath + ":/" + folderPath + "/"
        path = os.path.realpath(path)
        os.startfile(path)

    def getInfoWebSearch(self, query):
        comp = regex.compile(r'(search)\s*([\w\s]*)')
        match = regex.search(comp, query)
        try:
            squery = match.group(2)
        except AttributeError:
            squery = ''
        squery = squery.replace('about', '').replace(' ', '+')
        url = 'https://www.google.com/search?q=' + squery
        self.openFirefox(url)

    def tellInfoFromWiki(self, query):
        comp = regex.compile(r'(something\s*about)\s*([\w\s]+)')
        match = regex.search(comp, query)
        try:
            self.getDataFromWiki(match)
        except AttributeError:
            self.speak('unable to process your request now')
            self.logger.exception("Exception in 'say something'")

    def playMusic(self):
        mixer.init()
        mixer.music.load("song.wav")
        mixer.music.play()

    def getWeatherInfo(self):
        owm = pyowm.OWM('57a134899fde0edebadf307061e9fd23')
        observation = owm.weather_at_place('Barpeta, IN')
        observation_list = owm.weather_around_coords(26.511885, 91.180901)
        w = observation.get_weather()
        w.get_wind()
        w.get_humidity()
        w.get_temperature('celsius')
        self.speak(w.get_wind())
        self.speak('humidity')
        self.speak(w.get_humidity())
        self.speak('temperature')
        self.speak(w.get_temperature('celsius'))

    def openNotepad(self):
        path = 'C:\\Windows\\notepad.exe'
        os.startfile(path)

    def getHeadines(self, url):
        response = rq.get(url)
        status_code = response.status_code
        if (status_code == 200):
            self.topNewsHeadlines(response)
        else:
            self.speak("Error in fetching data from internet")
            self.logger.error("error in fetching data")

    def topNewsHeadlines(self, response):
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
            self.speak(news)

    def getDataFromWiki(self, match):
        squery = match.group(2)
        gotText = wikipedia.summary(squery)
        gotText = regex.sub('(\/[\w]+\/)', '', gotText)
        gotText = regex.sub('(\[[\d]+\])', '', gotText)
        gotText = regex.sub('[^A-Za-z0-9\s\(\)\-\,\.]+', '', gotText)
        gotText = gotText.replace('\n', '')
        self.speak(gotText)
        time.sleep(2)
        self.speak('Do you want to save this information?')
        answer = self.listenAudio()
        answer = answer.split()
        if self.validateCommand(answer, self.posAnswers):
            raNum = squery + str(random.randint(1, 1000))
            drive = 'X:\\Docs\\' + raNum + ".txt"
            file = open(drive, 'w+')
            file.write(gotText)
            file.close()
            self.speak('information saved in docs folder with ' + raNum + ' name.')
        elif self.validateCommand(answer, self.negAnswers):
            self.speak('As your wish!')

    def openFirefox(self, url):
        browser = self.initializeBrowser(url)
        xquery = 'running'
        while (xquery != 'close browser'):
            xquery = self.listenAudio()
            if (xquery == 'close browser'):
                browser.close()

    def sendEmail(self):
        self.speak('Who is the recipient?')
        recipient = self.listenAudio()
        if (recipient != None):
            SqlQueryRecipient = 'SELECT email_id FROM email_list WHERE shortname = "' + recipient + '"'
            EmailIdList = self.getDatafromDb(SqlQueryRecipient)
            if (len(EmailIdList)):
                emailId = EmailIdList[0][0]
                self.speak('What should I say to him?')
                content = self.listenAudioLong()
                self.speak('can i send the message?')
                resp = self.listenAudio()
                if (resp == 'yes'):
                    userSql = 'SELECT email, epass FROM email_auth WHERE cred_id=(SELECT cred_id FROM credentials WHERE username= "' + self.usr + '")'
                    userEmailCred = self.getDatafromDb(userSql)
                    username = userEmailCred[0][0]
                    password = userEmailCred[0][1]
                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(username, password)
                    mail.sendmail(username, emailId, content)
                    mail.close()
                    self.speak('Email has been sent successfully')
                else:
                    self.speak('Email sending cancelled')
            else:
                self.speak('no recipients found')

    def initializeBrowser(self, url):
        browser = Firefox()
        browser.get(url)
        return browser

    def driverFunc(self):
        try:
            self.speak("Agent started")
            self.logger.info("Agent started")
            self.speak("please verify your identity!")
            username = self.listenAudio()
            username = username.replace(' ', '')
            Sqlquery = 'select username,password from credentials where username="' + username + '"'
            userData = self.getDatafromDb(Sqlquery)
            if (len(userData)):
                self.speak('Say the password')
                passcode = self.listenAudio()
                self.logger.debug(passcode)
                self.speak('Processing passcode')
                self.authUser(userData, passcode)
            else:
                self.logger.error("user not found")
                self.speak('user not found!')
        except Exception as e:
            print(str(e))
            self.logger.exception("Exception in main function(before authentication). message: " + str(e))
        finally:
            logging.shutdown()
            self.mydb.close()

    def quit(self):
        sys.exit()


root = Tk()
obj = AgentJarvis()
root.geometry('800x500')
root.minsize(400, 300)
photo = PhotoImage(file='spcir.png')
label = Label(image=photo)
label.pack()
startButton = Button(root, text='Start', bg='green', command=obj.driverFunc)
startButton.pack()
StopButton = Button(root, text='Stop', bg='red', command=obj.quit)
StopButton.pack()
root.mainloop()
