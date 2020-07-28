import mysql.connector
import sys
from LoggingFile import *


class ManageDb:
    mydb = None
    logger = LoggingFile().logVal()

    def connectToDb(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost", user="root", passwd="password", database="jarvis_data")
            return self.mydb
        except Exception as e:
            self.logger.exception("MySQL not connected.")
            sys.exit()

    def getDatafromDb(self, Sqlquery):
        mycursor = self.setDatatoDb(Sqlquery)
        myresult = mycursor.fetchall()
        return myresult

    def setDatatoDb(self, Sqlquery):
        mycursor = self.mydb.cursor()
        mycursor.execute(Sqlquery)
        return mycursor
    def close(self):
        if(self.mydb!=None):
            self.mydb.close()