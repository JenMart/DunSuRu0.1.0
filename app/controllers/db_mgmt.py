import sqlite3
import os

from sqlite3worker import Sqlite3Worker



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
        # cur = sqlite3.connect('SkyTweetRun.sqlite')
        #
        # u = cur.cursor()
        # c = cur.cursor()
        # m = cur.cursor()
        # g = cur.cursor()
        # p = cur.cursor()

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")

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
                    WINCON VARCHAR(5) NOT NULL,
                    FOREIGN KEY(USER) REFERENCES USERS(ID)
                    ) """
        playerTracker = """CREATE TABLE PLAYERTRACKER (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        CHAR INTEGER NOT NULL,
                        REGION VARCHAR(255) NOT NULL,
                        TYPE VARCHAR(255) NOT NULL,
                        POS VARCHAR(255) NOT NULL,
                        TRACKER VARCHAR(255) NOT NULL,
                        FOREIGN KEY(CHAR) REFERENCES CHARACTERS(ID)
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
        sql_worker.execute(users)
        sql_worker.execute(characters)
        sql_worker.execute(graveyard)
        sql_worker.execute(playerTracker)
        sql_worker.close()

        # u.execute(users)
        # c.execute(characters)
        # g.execute(graveyard)
        # p.execute(playerTracker)
        #
        # cur.commit()
        # cur.close()

    def addUser(self, name, date, tweetID):
        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute("INSERT INTO USERS(USERNAME, TWEETID, DATESTAMP, LASTMESSAGE) VALUES (?, ?, ?, ?)", (name, tweetID, str(date), "null"))
        sql_worker.close()
        print("""Adding user data to Database""")
        # cursor = sqlite3.connect('SkyTweetRun.sqlite')
        # c = cursor.cursor()
        # c.execute("INSERT INTO USERS(USERNAME, TWEETID, DATESTAMP, LASTMESSAGE) VALUES (?, ?, ?, ?)", (name, tweetID, str(date), "null"))
        # cursor.commit()
        # cursor.close()
        return

    def addChar(self, userName, charName):
        charJob = "bandit"
        health = "10"
        gold = "1"
        curSec = "dun"
        region = "tester"
        state = "wlk"
        pos = "1^1"
        tracker = "1^1|E|NP|0|0|0"
        items = "holy water|1,alch fire|3,egg|5,lit candle|1"
        wincon = "false"
        CHARACTER = (
            """INSERT INTO CHARACTERS(USER, NAME, JOB, HEALTH, GOLD, ITEMS, STATE, REGIONTYPE, REGION, WINCON) VALUES((SELECT ID FROM USERS WHERE USERNAME = '{}'), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                .format(userName, charName, charJob, health, gold, items, state, curSec, region, wincon))
        PLAYERTRACKER = (
            """INSERT INTO PLAYERTRACKER(CHAR, REGION, TYPE, POS, TRACKER) VALUES((SELECT ID FROM CHARACTERS WHERE NAME ='{}'), '{}', '{}', '{}', '{}')""".format(
                charName, region, curSec, pos, tracker))

        # cur = sqlite3.connect('SkyTweetRun.sqlite')
        # c = cur.cursor()
        # p = cur.cursor()
        # c.execute(CHARACTER)
        # p.execute(PLAYERTRACKER)
        # cur.commit()
        # cur.close()

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(CHARACTER)
        sql_worker.execute(PLAYERTRACKER)
        sql_worker.close()

        return

    def delete_character(self, userName, charName):
        PLAYERTRACKER = (
            """DELETE FROM PLAYERTRACKER WHERE CHAR = (SELECT ID FROM CHARACTERS WHERE NAME ='{}')""".format(charName))

        CHARACTER = (
            """DELETE FROM CHARACTERS WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = '{}')""".format(userName))
        USER = ("""DELETE FROM USERS WHERE USERNAME = '{}'""".format(userName))

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(PLAYERTRACKER)
        sql_worker.execute(CHARACTER)
        sql_worker.execute(USER)
        sql_worker.close()
        print("character successfully deleted")
        return

    def delete_all_characters(self):
        PLAYERTRACKER = (
            """DELETE FROM PLAYERTRACKER""")

        CHARACTER = (
            """DELETE FROM CHARACTERS""")
        USER = (
            """DELETE FROM USERS""")

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(PLAYERTRACKER)
        sql_worker.execute(CHARACTER)
        sql_worker.execute(USER)
        sql_worker.close()
        print("The deed is done. All characters successfully deleted")
        return

    def character_death(self, username, char):
        CHARACTER = ("""DELETE FROM CHARACTERS WHERE VALUES((SELECT ID FROM USERS WHERE USERNAME = '{}')""".format(username))
        PLAYERTRACKER = (
            """DELETE FROM PLAYERTRACKER WHERE VALUES(SELECT ID FROM CHARACTERS WHERE NAME ='{}'""".format(char.name))
        the_longship = ("""INSERT INTO GRAVEYARD() VALUES((SELECT ID FROM USERS WHERE USERNAME = '{}'))""".format(username, char.name, char.job, char.gold))

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(CHARACTER)
        sql_worker.execute(PLAYERTRACKER)
        sql_worker.execute(the_longship)
        sql_worker.close()

        return

    def updateUser(self, name, tweetID, date, char):

        item_list = ""
        for i in char.items: # holy water|1,alch fire|3,egg|5,lit candle|1
            item_list += "{}|{},".format(i, char.items[i])
        item_list = item_list[:-1]



        # print(item_list)
        CHARACT = ("""UPDATE CHARACTERS SET STATE = '{}', ITEMS = '{}', WINCON = '{}' WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = '{}')""".format(char.state, item_list, char.WINCON, name))
        USER = ("""UPDATE USERS SET TWEETID = '{}', DATESTAMP = '{}', LASTMESSAGE = '{}' WHERE USERNAME = '{}'""".format(tweetID, str(date), "null", name))
        PLAYERTRACKER = ("""UPDATE PLAYERTRACKER SET POS = '{}', TRACKER = '{}' WHERE CHAR = (SELECT ID FROM CHARACTERS WHERE NAME ='{}')""".format(char.POS, char.tracker, name))

        # cursor = sqlite3.connect('SkyTweetRun.sqlite')
        # c = cursor.cursor()
        # u = cursor.cursor()
        # p = cursor.cursor()
        # print(char.tracker)
        # c.execute("""UPDATE USERS SET TWEETID = ?, DATESTAMP = ?, LASTMESSAGE = ? WHERE USERNAME = ?""", (tweetID, str(date), "null", name))
        # u.execute("""UPDATE CHARACTERS SET STATE = ?, ITEMS = ? WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = ?)""",(char.state, char.items, name))
        # p.execute("""UPDATE PLAYERTRACKER SET POS = ?, TRACKER = ? WHERE CHAR = (SELECT ID FROM CHARACTERS WHERE NAME =?)""", (char.POS, char.tracker, name))
        # cursor.commit()
        # cursor.close()

        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(CHARACT)
        sql_worker.execute(PLAYERTRACKER)
        sql_worker.execute(USER)
        sql_worker.close()

        return

    def for_this_moment_all_is_well(self, the_honored):

        yes_please = "true"
        CHARACT = ("""UPDATE CHARACTERS SET WINCON = {} WHERE USER = (SELECT ID FROM USERS WHERE USERNAME = '{}')""".format(yes_please, the_honored))
        sql_worker = Sqlite3Worker("SkyTweetRun.sqlite")
        sql_worker.execute(CHARACT)
        sql_worker.close()
        print("All is well.")
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
                    CHARACTERS.STATE, PLAYERTRACKER.REGION, PLAYERTRACKER.TYPE, PLAYERTRACKER.POS, PLAYERTRACKER.TRACKER,
                    CHARACTERS.WINCON
                     FROM CHARACTERS JOIN PLAYERTRACKER ON
                    CHARACTERS.ID = PLAYERTRACKER.CHAR WHERE USER =
                    (SELECT ID FROM USERS WHERE USERNAME = ?)""",(name,))
        getChar = c.fetchall()
        cursor.commit()
        cursor.close()
        charTuple = getChar[0]
        return charTuple


