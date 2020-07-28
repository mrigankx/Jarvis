from SpeechProcess import *
from ManageDb import *
import sys
import random
from datetime import datetime


class Authentication:
    sp = SpeechProcess()
    manageDb = ManageDb()
    usr = None
    permissions = {"email_access": 0, "internet_access": 0, "master_access": 0}
    greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!', 'hey']

    def wishMe(self):
        hour = int(datetime.now().hour)
        if (hour >= 0 and hour < 12):
            return " Good morning!"
        elif (hour >= 12 and hour <= 16):
            return " Good afternoon!"
        else:
            return " Good evening!"

    def getCreds(self):
        username = str(input("Enter username: "))
        self.sp.logger.info('USERNAME: ' + username)
        mydb = self.manageDb.connectToDb()
        Sqlquery = 'select username,password from credentials where username="' + username + '"'
        userData = self.manageDb.getDatafromDb(Sqlquery)
        if (len(userData)):
            self.sp.speak('Enter the password')
            passcode = str(input("Enter password: "))
            self.sp.logger.debug(passcode)
            self.sp.speak('Processing passcode')
            self.authUser(userData, passcode)
        else:
            self.logger.error("user not found")
            self.sp.speak('user not found!')

    def authUser(self, rpass, pcode):
        if (pcode == rpass[0][1]):
            self.sp.speak("Passcode matched.... ")
            self.sp.logger.debug(
                "in authUser().Passcode matched & agent activated.")
            greeting = random.choice(self.greetings)
            wish = greeting + " " + rpass[0][0] + self.wishMe()
            self.sp.speak(wish)
            self.usr = rpass[0][0]
            Sqlquery = 'SELECT email_access, internet_access, master_access FROM `permissions` WHERE `user`=(SELECT cred_id FROM `credentials` WHERE username="' + self.usr + '")'
            userAccess = self.manageDb.getDatafromDb(Sqlquery)
            self.permissions["master_access"] = int(userAccess[0][2])
            self.permissions["internet_access"] = int(userAccess[0][1])
            self.permissions["email_access"] = int(userAccess[0][0])
        else:
            self.sp.speak("Invalid passcode.....Exiting.")
            self.sp.logger.error("Invalid Passcode.Exiting.")
            sys.exit()

    def setPassword(self):
        if(self.permissions["master_access"] == 1):
            self.sp.speak("setting new passcode.... enter the new password")
            npass = str(input())
            try:
                updateQuery = "update credentials set password ='" + \
                    npass + "' where username='" + self.usr + "'"
                self.manageDb.setDatatoDb(updateQuery)
                self.sp.logger.debug("passcode changed successfully.")
                self.sp.speak(
                    'I Successfully changed your passcode....')
            except Exception as e:
                self.sp.logger.error(
                    "Exception in password changing. message: " + str(e))
                self.sp.speak('Unable to change password.')
        else:
            self.sp.speak("Insufficient permissions to change password")
            self.sp.logger.error("Insufficient permissions to change password")
