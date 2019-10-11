#
# Note: This was the original offline tester but one day it stopped working.
#       I Cntl C/V into another file and it works fine..?
#       Another mystery for another day.
#
from app.controllers.db_mgmt import DatabaseManager
from app.controllers.g_manager import Main
from app.models.textDAO import textDAO
from time import gmtime, strftime
from app.models.charDAO import CharDAO

#
# All output in tester identical to Tweepy output.
#
# south
# thisthatotherth
# 2019-08-02 19:46:59
# 1155645641793687552
#

class notMain:
#,2^1L3,2^2M2
    def __init__(self):
        self.db_mgmt = DatabaseManager()
        self.g_manager = Main()
        inptFake = "south"
        userNameFake = "fakeAccount"
        createDateFake = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        statIDFake ="1155645641793687552"
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



if __name__ == '__main__':
    notMain()





