import sqlite3
import os


class DatabaseManager:
    #
    #   Should call self.setup() if the DB isn't found in the same folder as g_manager.py.
    #   To rebuild the DB, delete the file and run g_manager.py again.
    #
    def __init__(self):
        if not os.path.isfile('SkyTweetRun.sqlite'):
            self.setup()
    #
    #   Deletes the database. Used for testing.
    #
    def delete(self):
        #delete the database to test new additions
        print('deleting database')
        if os.path.isfile('SkyTweetRun.sqlite'):
           os.remove('SkyTweetRun.sqlite')

    def setup(self):
        cur = sqlite3.connect('SkyTweetRun.sqlite')
        u = cur.cursor()
        c = cur.cursor()
        m = cur.cursor()
        g = cur.cursor()
        p = cur.cursor()
        print("Creating database")
        users = """ CREATE TABLE USERS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME VARCHAR(255) NOT NULL,
                TWEETID VARCHAR(255) NOT NULL,
                DATESTAMP VARCHAR(255) NOT NULL,
                LASTMESSAGE VARCHAR(255) NOT NULL
                )"""
        characters = """ CREATE TABLE CHARACTERS (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USER INTEGER NOT NULL,
                    NAME VARCHAR(255) NOT NULL,
                    JOB VARCHAR(255) NOT NULL,
                    HEALTH INT NOT NULL, 
                    GOLD INT NOT NULL, 
                    ITEMS VARCHAR(512) NOT NULL,
                    STATE VARCHAR(4) NOT NULL,                  
                    REGION VARCHAR(255) NOT NULL,
                    REGIONTYPE VARCHAR(255) NOT NULL,
                    FOREIGN KEY(USER) REFERENCES USERS(ID)
                    ) """
        playerTracker = """CREATE TABLE PLAYERTRACKER (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CHAR INTEGER NOT NULL,
                        REGION VARCHAR(255) NOT NULL,
                        TYPE VARCHAR(255) NOT NULL,
                        POS VARCHAR(255) NOT NULL,
                        TRACKER VARCHAR(255) NOT NULL,
                        FOREIGN KEY(CHAR) REFERENCES USERS(ID)
                    )"""
        graveyard = """CREATE TABLE GRAVEYARD (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USER INTEGER NOT NULL,
                    NAME VARCHAR(255) NOT NULL,
                    JOB VARCHAR(255) NOT NULL,
                    GOLD INT NOT NULL,
                    FOREIGN KEY(USER) REFERENCES USERS(ID)
                    )
                    """
        u.execute(users)
        c.execute(characters)
        g.execute(graveyard)
        p.execute(playerTracker)

        cur.commit()
        cur.close()

    def addUser(self, name, date, tweetID):
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        print("""Adding user data to Database""")
        c.execute("INSERT INTO USERS(USERNAME, TWEETID, DATESTAMP, LASTMESSAGE) VALUES (?, ?, ?, ?)", (name, tweetID, str(date), "null"))
        cursor.commit()
        cursor.close()
        return

    def addChar(self, userName, charName):
        cur = sqlite3.connect('SkyTweetRun.sqlite')
        c = cur.cursor()
        p = cur.cursor()
        charJob = "bandit"
        health = 1
        gold = 1
        curSec = "dun"
        region = "tester"
        state = "wlk"
        pos = "1^1"
        tracker = "1^1|E|NP|0"
        items = "Holy Water|1,Alch Fire|3,Egg|5"
        c.execute("""INSERT INTO CHARACTERS(USER, NAME, JOB, HEALTH, GOLD, ITEMS, STATE, REGIONTYPE, REGION) VALUES((SELECT ID FROM USERS WHERE USERNAME = ?),
         ?, ?, ?, ?, ?, ?, ?, ?)""", (userName, charName, charJob, health, gold, items, state, curSec, region))
        p.execute("""INSERT INTO PLAYERTRACKER(CHAR, REGION, TYPE, POS, TRACKER) VALUES((SELECT ID FROM CHARACTERS WHERE NAME =?), ?, ?, ?, ?)""",
                  (charName, region, curSec, pos, tracker))
        cur.commit()
        cur.close()
        return

    def updateUser(self, name, tweetID, date, char):
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        u = cursor.cursor()
        p = cursor.cursor()
        print(char.tracker)
        c.execute("""UPDATE USERS SET TWEETID = ?, DATESTAMP = ?, LASTMESSAGE = ? WHERE USERNAME = ?""", (tweetID, str(date), "null", name))
        u.execute("""UPDATE CHARACTERS SET STATE = ?, ITEMS = ? WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = ?)""",(char.state, char.items, name))
        p.execute("""UPDATE PLAYERTRACKER SET POS = ?, TRACKER = ? WHERE CHAR = (SELECT ID FROM CHARACTERS WHERE NAME =?)""", (char.POS, char.tracker, name))
        cursor.commit()
        cursor.close()
        return


    def checkUser(self, name):
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        c.execute("""SELECT * FROM USERS WHERE USERNAME = ? """, (name,))
        tweets = c.fetchall()
        cursor.commit()
        cursor.close()
        if len(tweets) == 0:
            return True
        else:
            return False

    def checkCharacter(self, name):
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        c.execute("""SELECT * FROM CHARACTERS WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = ?) """, (name,))
        tweets = c.fetchall()
        cursor.commit()
        cursor.close()
        if len(tweets) == 0:
            return True
        else:
            return False


    def pullLocation(self, name):
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        c.execute("""SELECT POS FROM CHARACTERS WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = ?)""", (name,))
        tweets = c.fetchall()
        cursor.commit()
        outTweet = ""
        for tweet in tweets:

            outTweet = tweet[0]
        cursor.close()
        return outTweet

    def pullCharacter(self, name):
        #
        # NOTE: Anything other than basic joins are not supported with SQLite.
        #
        cursor = sqlite3.connect('SkyTweetRun.sqlite')
        c = cursor.cursor()
        c.execute("""SELECT CHARACTERS.NAME, CHARACTERS.JOB, CHARACTERS.HEALTH, CHARACTERS.GOLD, CHARACTERS.ITEMS,
                    CHARACTERS.STATE, PLAYERTRACKER.REGION, PLAYERTRACKER.TYPE, PLAYERTRACKER.POS, PLAYERTRACKER.TRACKER
                     FROM CHARACTERS JOIN PLAYERTRACKER ON
                    CHARACTERS.ID = PLAYERTRACKER.CHAR WHERE USER =
                    (SELECT ID FROM USERS WHERE USERNAME = ?)""",(name,))
        getChar = c.fetchall()
        cursor.commit()
        cursor.close()
        charTuple = getChar[0]
        return charTuple