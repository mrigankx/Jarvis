import os
import random
import re as regex
import smtplib
import time
from datetime import datetime
from tkinter import *
from typing import List
from urllib.request import urlopen
import sys
import mysql.connector
import pyowm
import pyttsx3
import requests as rq
import speech_recognition as sr
import vlc
import wikipedia
import youtube_dl
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from selenium.webdriver import Firefox
from Authentication import *
import ctypes


class ProcessRequests:
    auth = Authentication()
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
    cmd7 = ['what is your color', 'what is your colour',
            'your color', 'your color?']
    colrep = ['right now its rainbow',
              'right now its transparent', 'right now its non chromatic']
    cmd8 = ['what is you favourite colour', 'what is your favourite color']
    cmd9 = ['thank you']
    rep9 = ["you're welcome", 'glad i could help you']
    webSearch: List[str] = ['firefox', 'internet', 'browser']
    sound = ['volume', 'sound']
    txtEdit = ['notepad']
    says = ['tell', 'say']
    newsText = ['news', 'headlines']
    posAnswers = ['yes', 'ok', 'yop']
    negAnswers = ['no', 'never', 'nope']
    mailCmd = ['mail', 'email']
    mypc = ['pc', 'laptop', 'system', 'computer']
    logoutCmd = ['log', 'sign', 'logout', 'signout']

    def validateCommand(self, query, givenList):
        for word in query:
            for gword in givenList:
                if (word == gword):
                    return True
        return False

    def processRequests(self, query):
        queryx = query.split()
        queryx = [word for word in queryx if not word in set(
            stopwords.words('english'))]
        if (self.validateCommand(queryx, self.webSearch) and (self.auth.permissions["internet_access"] == 1 or self.auth.permissions["master_access"] == 1)):
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
        elif ('change your password' == query):
            self.auth.setPassword()
        elif (self.validateCommand(queryx, self.says) and (r'something' in query) and (self.auth.permissions["internet_access"] == 1 or self.auth.permissions["master_access"] == 1)):
            self.tellInfoFromWiki(query)
        elif self.validateCommand(queryx, self.var3):
            self.getTime()
        elif self.validateCommand(queryx, self.mailCmd) and self.validateCommand(queryx, ['send']):
            self.sendEmail()
        elif query in self.question:
            self.auth.speak('I am fine')

        elif query in self.cmd9:
            self.auth.speak(random.choice(self.rep9))

        elif query in self.cmd7:
            self.auth.speak('It keeps changing every second')

        elif query in self.cmd8:
            self.auth.speak(random.choice(self.colrep))
            self.auth.speak('It keeps changing every second')
        elif self.validateCommand(queryx, self.cmd5):
            self.getWeatherInfo()
        elif self.validateCommand(queryx, self.cmd2):
            self.playMusic()

        elif (r'open' in query):
            # open [foldername] inside [name of drive] drive in file explorer
            if (r'file explorer' in query):
                self.openFileExplorer(query)
            else:
                openApp = self.openAnyApplication(query)
                if (openApp == 'notepad'):
                    self.openNotepad()
                else:
                    self.auth.speak('app not found')

        elif (self.validateCommand(queryx, self.newsText) and (self.auth.permissions["internet_access"] == 1 or self.auth.permissions["master_access"] == 1)):
            self.auth.speak("fetching headlines from IndiaToday")
            url = 'https://www.indiatoday.in/top-stories'
            self.getHeadines(url)
        elif self.validateCommand(queryx, self.cmdjokes):
            self.auth.speak(random.choice(self.jokes))
        elif (query == 'who are you' or query == 'what is your name'):
            self.auth.speak('I am covia, your personal assistant')
        elif ('who is your developer' in query) or (r'who made you' in query):
            self.auth.speak('Mriganka Goswami developed me.')
        elif (r'shutdown' in query) and self.validateCommand(queryx, self.mypc):
            os.system("shutdown /s /t 1")

        elif (r'restart' in query) and self.validateCommand(queryx, self.mypc) and self.auth.permissions["master_access"] == 1:
            os.system("shutdown /r /t 1")
        elif (r'lock' in query) and self.validateCommand(queryx, self.mypc):
            ctypes.windll.user32.LockWorkStation()

        elif (self.validateCommand(queryx, self.logoutCmd) or (r'out' in query)) and self.validateCommand(queryx,
                                                                                                          self.mypc) and self.auth.permissions["master_access"] == 1:
            os.system("shutdown -l")
        elif (query in self.exitCmd):
            self.auth.speak('Good bye!')
            sys.exit()
        else:
            self.auth.speak("sorry....invalid voice command...say again")

        def openAnyApplication(self, query):
            app = regex.compile(r'(open)\s*([\w\s]*)')
            match = regex.search(app, query)
            try:
                openApp = match.group(2)
            except:
                self.auth.speak('unable to open the application')
                self.auth.sp.logger.exception("Error in opening application")
                openApp = ''
            return openApp

    def openFileExplorer(self, query):
        comp = regex.compile(r'(open)\s*([\w\s]*)\s*inside\s*([\w])\s')
        match = regex.search(comp, query)
        try:
            drivePath = match.group(3)
            folderPath = match.group(2)
        except:
            self.auth.speak("Drive name is missing.....try again")
            self.auth.sp.logger.exception("Drive name missing in 'open drive'")
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
            self.auth.speak('unable to process your request now')
            self.auth.sp.logger.exception("Exception in 'say something'")

    def playMusic(self):
        path = 'X://Covia//'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.auth.sp.logger.exception("Unable to find directory")
                self.auth.speak('unable to find music directory')
        self.auth.speak('Which song shall I play?')
        mysong = self.listenAudio()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + \
                mysong.replace(' ', '+')
            response = urlopen(url)
            html = response.read()
            soup1 = BeautifulSoup(html, "lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
            if flag == 1:
                url = url_list[0]
                ydl_opts = {}
                os.chdir(path)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                for the_file in os.listdir(folder):
                    path = os.path.join(folder, the_file)
                player = vlc.MediaPlayer(path)
                player.play()
                duration = player.get_length() / 1000
                duration = time.time() + duration
                while True:
                    exitQuery = self.listenAudio()
                    if exitQuery != None:
                        exitQuery = exitQuery.split()
                        if self.validateCommand(exitQuery, self.exitCmd):
                            player.stop()
                            break
                    continue
        if flag == 0:
            self.auth.speak('I have not found anything in Youtube ')

    def getWeatherInfo(self):
        owm = pyowm.OWM('57a134899fde0edebadf307061e9fd23')
        observation = owm.weather_at_place('Barpeta, IN')
        w = observation.get_weather()
        self.auth.speak(w.get_wind())
        self.auth.speak('humidity')
        self.auth.speak(w.get_humidity())
        self.auth.speak('temperature')
        self.auth.speak(w.get_temperature('celsius'))

    def openNotepad(self):
        path = 'C:\\Windows\\notepad.exe'
        os.startfile(path)

    def getHeadines(self, url):
        response = rq.get(url)
        status_code = response.status_code
        if (status_code == 200):
            self.topNewsHeadlines(response)
        else:
            self.auth.speak("Error in fetching data from internet")
            self.auth.sp.logger.error("error in fetching data")

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
            self.auth.speak(news)

    def getDataFromWiki(self, match):
        squery = match.group(2)
        gotText = wikipedia.summary(squery)
        gotText = regex.sub('(\/[\w]+\/)', '', gotText)
        gotText = regex.sub('(\[[\d]+\])', '', gotText)
        gotText = regex.sub('[^A-Za-z0-9\s\(\)\-\,\.]+', '', gotText)
        gotText = gotText.replace('\n', '')
        self.auth.speak(gotText)
        time.sleep(2)
        self.auth.speak('Do you want to save this information?')
        answer = self.listenAudio()
        answer = answer.split()
        if self.validateCommand(answer, self.posAnswers):
            raNum = squery + str(random.randint(1, 1000))
            drive = 'X:\\Docs\\' + raNum + ".txt"
            file = open(drive, 'w+')
            file.write(gotText)
            file.close()
            self.auth.speak('information saved in docs folder with ' +
                            raNum + ' name.')
        elif self.validateCommand(answer, self.negAnswers):
            self.auth.speak('As your wish!')

    def openFirefox(self, url):
        browser = self.initializeBrowser(url)
        xquery = 'running'
        while (xquery != 'close browser'):
            xquery = self.listenAudio()
            if (xquery == 'close browser'):
                browser.close()

    def sendEmail(self):
        self.auth.speak('Who is the recipient?')
        recipient = self.listenAudio()
        recipient = recipient.replace(' ', '')

        if (recipient != None and (self.auth.permissions["master_access"] == 1 or self.auth.permissions["email_access"] == 1)):
            SqlQueryRecipient = 'SELECT email_id FROM email_list WHERE shortname = "' + recipient + '"'
            EmailIdList = self.getDatafromDb(SqlQueryRecipient)
            if (len(EmailIdList)):
                emailId = EmailIdList[0][0]
                self.auth.speak('What should I say to him?')
                content = self.listenAudioLong()
                if(content == None):
                    content = "Hii there"
                self.auth.speak('can i send the message?')
                resp = self.listenAudio()
                if (resp == None):
                    resp = "yes"
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
                    self.auth.speak('Email has been sent successfully')
                else:
                    self.auth.speak('Email sending cancelled')
            else:
                self.auth.speak('no recipients found')

    def initializeBrowser(self, url):
        browser = Firefox()
        browser.get(url)
        return browser

    def getTime(self):
        now = datetime.now()
        self.speak(now.strftime("The time is %H:%M"))

    def quit(self):
        sys.exit()
