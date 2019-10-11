import random
import time
import tweepy



ckey= 'rlee33vXmHIlmR5tQljIX0ucD'
csecret= 'cUiIFESIXSSin9YJHYwLnVwnHpS64Ytj7csY9yFqshvAlkcaPg'
atoken= '2836017980-DxYDsgHqGMyRIq1yH3Uf3Ar63eYCFhqawJAWGOw'
asecret= 'SruNXYjh0BpY4GQhiflXaxbB2XUhrCMslBrmrH2ViULnu'


def printTweet():
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    api = tweepy.API(auth)
    message = "Hello world."
    print("pip")
    for status in tweepy.Cursor(api.user_timeline).items():
        if status.text in message:
            try:
                api.destroy_status(status.id)
            except:
                pass
    time.sleep(random.randint(1, 3))
    print(message)
    time.sleep(10)
    api.update_status(status=message)


printTweet()