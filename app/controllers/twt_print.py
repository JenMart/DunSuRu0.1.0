import tweepy

#
# Note: This is deprecated.
#


ckey= 'rlee33vXmHIlmR5tQljIX0ucD'
csecret= 'cUiIFESIXSSin9YJHYwLnVwnHpS64Ytj7csY9yFqshvAlkcaPg'
atoken= '2836017980-DxYDsgHqGMyRIq1yH3Uf3Ar63eYCFhqawJAWGOw'
asecret= 'SruNXYjh0BpY4GQhiflXaxbB2XUhrCMslBrmrH2ViULnu'

class printTwt:

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
        api.update_status(message)