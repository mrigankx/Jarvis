'''
Name: 'Covia'
Date: 03/05/2020
Developer: Mriganka Goswami
'''
from LoggingFile import *
from Authentication import *
from ProcessCommand import *
from ManageDb import *

auth = Authentication()
pc = ProcessCommand()
db = ManageDb()
try:
    auth.sp.speak("Agent started")
    auth.sp.logger.info("Agent started")
    auth.sp.speak("please verify your identity!")
    auth.getCreds()
    pc.processCommand()
except Exception as e:
    auth.sp.logger.exception(
        "Exception in main function(before authentication). message: " + str(e))
finally:
    logging.shutdown()
    db.close()
