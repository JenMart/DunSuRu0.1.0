import threading
import time
import tweepy
from tweepy.streaming import StreamListener, json
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
from app.controllers.db_mgmt import DatabaseManager
from app.controllers.g_manager import Main
from  app.models.userData import userData
import time



#
# Rate limit: 2400 tweets a day- 300 an hour- 15 every 15 minutes (How does this make sense??)
# 1000 DM a day.
# Cycles through array full of keys. If system throws error,
#

################################
access_0 = ['jmPAnJTFJzL9xg2M6LxwAXHTO','wQ4EcSOGyqHcFKwZvGVa5eIjtZ3G5CJKJlMfeldQSzFZa7hoQe','2836017980-WsUL4uUBLVKGD2VCrkyhijZs6g8pq8CwztiELJ9','wi5wNXdpPOje76oB0EqpZGOVzq78Pb3ml44wYRl2AiI2o']
access_1 = ['3z5SpXPsvo6a79Rk2kqZEtH1M','fB0cQdxlylNt9xgH1mBhAtObWkVzwrbzAOsVcbceHNsRi9bLBj','1158742691435487232-BFz6z1tN9EwnHAGyc2O9oipHbX8jOg','1ZXSHbAFcrc8PDeDoUR0IIBZXntRFMLmXRI4C3ZPTwMR1']
access_2 = ["ebEE8WNuzCW0HE49fUihAWihb","dGa6QIHjGy6Np9FVUeRtCe71Y3MxXqQHobJSDfHp9ngQqTPNxc","2614702302-IPhBfVOPMjm5Nth7OI8UocccXgI7ZL6hcdycpWG","bD3FR7MOt9rhy7OFRzD1MEfoHfXjHZ26CHcFQjdpQzg16"]
access_3 = ["UmgeWxJ5fh50M7iMgtGJkWsNn","zjWlYimaCQrdKuDmAR6EYqBoUzRPAcgTVwkymyzKBS2TE4KXid","1282074139235418112-NjSbQvAYIE0tiHSRJy2Knp6AbLxGuR","moXf7WtUIR1WnvyTBkZ6U4OLuBLJaRXdBq03TAYN1Kc4D"]
access_array = [access_0, access_1, access_2, access_3]
################################

class twtrManager(StreamListener):

    #
    # A listener handles tweets that are received from the stream.
    # This is a basic listener that just prints received tweets to stdout.
    #

    def __init__(self, api=None):
        super().__init__(api=None)
        self.db_mgmt = DatabaseManager()
        self.g_manager = Main()
        self.userData = userData


    def on_status(self, status):
        #
        # Status object holds all twitter user info objects
        # Here we parse down data
        #
        screenName = status.author.screen_name
        time = time.time() # formely status.created_at
        statID = status.id
        txt = status.text
        txt = txt.replace("@DunSuRu","")
        print(txt)
        ##########################################
        DT = datetime.now().strftime("%H:%M:%S.%f")
        print("Time Stamp: "+DT)
        ##########################################
        try:
            ex = self.g_manager.handleChoice(txt, screenName, time, statID)
            self.printTweet(screenName, ex, statID)
        except Exception as e:
            print("Error")
            print(e)

    def printTweet(self, user, text, statID):
        #
        # Remember: You have exactly 263 characters to tell a story.
        #
        for i in access_array:
            try: # This cycles through keys when rate limit error occurs.
                if text != "OVER_TIME_ERROR":
                    ckey = i[0]
                    csecret = i[0]
                    atoken = i[0]
                    asecret = i[0]
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
                                break # Break points added to stop process entirely to avoid using more of the rate limits
                    # time.sleep(random.randint(1,3))
                    print(message)
                    ##########################################
                    DT = datetime.now().strftime("%H:%M:%S.%f")
                    print("Time Stamp: "+DT)
                    ##########################################
                    api.update_status(message, statID)
                else:
                    print("over time error")
            except Exception as e:
                print(e)
                print("Switching keys")

    def on_error(self, status):
        print(status)




if __name__ == '__main__':
    TWT = twtrManager()
    #
    # Starts twitter scrape
    #
    for i in access_array:
        try: # This cycles through keys when rate limit error occurs.
            ckey = i[0]
            csecret = i[0]
            atoken = i[0]
            asecret = i[0]

            auth = OAuthHandler(ckey, csecret)
            auth.set_access_token(atoken, asecret)
            stream = Stream(auth, TWT)

            #
            # Filters results to only display @DunSuRu
            #
            try:
                th = threading.Thread(stream.filter(track=['@DunSuRu']))
                th.start()
                print("ddddd")
            except Exception as e:
                print(str(e))
                print("process failed at: " + time.ctime())
                break # Break points added to stop process entirely to avoid using more of the rate limits
        except Exception as e:
            print(e)
            print("Switching keys")
