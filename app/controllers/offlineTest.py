from app.controllers.db_mgmt import DatabaseManager
from app.controllers.g_manager import Main
from app.models.textDAO import textDAO
from time import gmtime, strftime
from app.models.charDAO import CharDAO
from datetime import datetime

#
# All output in tester identical to Tweepy output.
#
# south
# thisthatotherth
# 2019-08-02 19:46:59
# 1155645641793687552
#

class notMain:
    def __init__(self):
        self.db_mgmt = DatabaseManager()
        self.g_manager = Main()
        inptFake = "hail"
        userNameFake = "fakeAccount"
        createDateFake = gmtime()
        statIDFake ="1155645641793687552"
        ##########################################
        DT = datetime.now().strftime("%H:%M:%S.%f")
        print("Time Stamp: " + DT)
        ##########################################
        try:
            exFake = self.g_manager.handleChoice(inptFake, userNameFake, createDateFake, statIDFake)
            self.fakePrinter(userNameFake, exFake, statIDFake)
        except Exception as e:
            print("Error")
            print(e)

    def fakePrinter(self, user, text, statID):
        message = "@" + user + " " + text
        print("Creating fake tweet: \n" + message + "\n")
        print("character count: " + str(len(message)))
        if len(message) >= 263:
            print("*******")
            print("WARNING: message too large or at character limit")
            print("*******")
        ##########################################
        DT = datetime.now().strftime("%H:%M:%S.%f")
        print("Time Stamp: " + DT)
        #########################################



if __name__ == '__main__':
    notMain()




