import threading
import time
import random
import tweepy
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
# from app.models.userDAO import UserDAO
from app.controllers.db_mgmt import DatabaseManager
from app.controllers.g_manager import Main

####
ckey= '*****'
csecret= '*****'
atoken= '*****'
asecret= '*****'

class twtrManager(StreamListener):

    #
    # A listener handles tweets that are received from the stream.
    # This is a basic listener that just prints received tweets to stdout.
    #

    def __init__(self, api=None):
        super().__init__(api=None)
        self.db_mgmt = DatabaseManager()
        self.g_manager = Main()


    def on_status(self, status):
        #
        # Status object holds all twitter user info objects
        #
        screenName = status.author.screen_name
        createDate = str(status.created_at)
        statID = status.id
        txt = status.text
        txt = txt.replace("@DunSuRu","")
        print(txt)
        ##########################################
        DT = datetime.now().strftime("%H:%M:%S.%f")
        print("Time Stamp: "+DT)
        ##########################################
        try:
            #
            #Originally started a new thread. Removed because pointless.
            #
            ex = self.g_manager.handleChoice(txt, screenName, createDate, statID)
            self.printTweet(screenName, ex, statID)

        except Exception as e:
            print("Error")
            print(e)

    def printTweet(self, user, text, statID):
        #
        # Remember: You have exactly 263 characters to tell a story.
        #
        auth = tweepy.OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        api = tweepy.API(auth)
        message = "@" + user + " " + text
        for status in tweepy.Cursor(api.user_timeline).items():
            if status.text in message:
                try:
                    api.destroy_status(status.id)
                except:
                    pass
        # time.sleep(random.randint(1,3))
        print(message)
        ##########################################
        DT = datetime.now().strftime("%H:%M:%S.%f")
        print("Time Stamp: "+DT)
        ##########################################
        api.update_status(message, statID)

    def on_error(self, status):
        print(status)




if __name__ == '__main__':
    TWT = twtrManager()
    #
    # Starts twitter scrape
    #
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    stream = Stream(auth, TWT)

    #
    # Filters results to only display @DunSuRu
    #
    try:
        th = threading.Thread(stream.filter(track=['@DunSuRu']))
        th.start()
    except Exception as e:
        print(str(e))
        print("process failed at: " + time.ctime())
        # time.sleep(5)
        th = threading.Thread(stream.filter(track=['things']))
        th.start()