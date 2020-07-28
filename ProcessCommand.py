from Authentication import *
from SpeechProcess import *
import time
from ProcessRequests import *


class ProcessCommand:
    sp = SpeechProcess()
    pr = ProcessRequests()

    def processCommand(self):
        while (1):
            try:
                time.sleep(1)
                self.sp.speak('Listening now')
                self.sp.logger.debug('Listening......')
                query = self.sp.listenAudio()
                if (query == None):
                    query = ''
                self.sp.logger.debug('query: ' + str(query))
                self.pr.processRequests(query)
            except Exception as e:
                self.sp.speak("sorry.....unable to process...say again")
                print(str(e))
                self.sp.logger.exception(str(e))
