import sqlite3
from time import gmtime, strftime
import random
import re
from datetime import datetime

text = "1U1"
name = "thisthatotherth"
# date example: "2019-08-02 20:46:59"
date = strftime("%Y-%m-%d %H:%M:%S", gmtime())


conn = sqlite3.connect('SkyTweetRun.sqlite')


a = conn.cursor()
a.execute("""SELECT NAME FROM CHARACTERS""")
# a.execute("""SELECT * FROM CHARACTERS JOIN PLAYERTRACKER ON
#                     CHARACTERS.ID = PLAYERTRACKER.CHAR WHERE USER =
#                     (SELECT ID FROM USERS WHERE USERNAME = ?)""", ("fakeAccount",))
# a.execute("""SELECT CHARACTERS.USER, CHARACTERS.NAME, CHARACTERS.JOB, CHARACTERS.HEALTH, CHARACTERS.GOLD, CHARACTERS.ITEMS,
#                     CHARACTERS.STATE, PLAYERTRACKER.REGION, PLAYERTRACKER.TYPE, PLAYERTRACKER.POS, PLAYERTRACKER.TRACKER
#                      FROM CHARACTERS JOIN PLAYERTRACKER ON
#                     CHARACTERS.ID = PLAYERTRACKER.CHAR WHERE USER =
#                     (SELECT ID FROM USERS WHERE USERNAME = ?)""",("KlydeAdVanced",))
print(a.fetchall())

conn.commit()
conn.close()

vvv = " You see a swarm of rats.|cmb"
vvz = vvv.split("|")[0]
print(vvz)

#
# "Pay no attention to that man behind the curtain."
# Translation: Useless code I made to add to DB because I was getting sick of the code not working.
#
# tracker = "1^1|E|NP|1|edw"
# zz = tracker.split("|")[:-1]
# print(tracker[-3:])
#
#
# talkDict = {
#     "00":"This is not a valid option.",
#     "start":"The darkness drifts towards you and a set of eyes appears from its depth “Speak adventurer.” It hisses. |{OKL}|I wish you {peace}|{Hail} and well met|tlk",
#     "ok":"It eyes you dispassionately with a weight of infinite patients. “Tell me what you seek.” |A {purpose}|{An answer}|{Wealth}|{Fame}|tlk",
#     "peace":"“How fortuitous.” it chortles mirthlessly. “These halls lay empty for sometime. What do seek?” |A {purpose}|{An answer}|{Wealth}|{Fame}|tlk",
#     "hail":"its eye reveal a hint of surprise. “Such politeness to a beast such as myself. Do you speak so out of fear or a sense of obligation?”  |{Fear}|{Obligation}|tlk",
#     "fame":"Many live to have their names written in the scrolls of history but few scrolls have survived The End|tlk",
#     "wealth":" Gold and jewels are said to be overrated but few can argue against the comfort they bring. Would you be satisfied with facing The End of luxury?|tlk",
#     "answer":"I am sorry to say but you shall not find an answer here.|{exit}|tlk",
#     "fear":"I will not eat my first visitor in eons. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk",
#     "obligation":"Good to see the old ways are not dead. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk",
#     "purpose":"In this I cannot help.|{exit}|wlk"
# }
#
# s = 'The darkness drifts towards you and a set of eyes appears from its depth “Speak adventurer.” It hisses. |{ok}|a {hail} and well met|I wish you {peace}.'
# result = re.match('%(.*)%', talkDict["start"])
# x = talkDict["start"].split("|")
# while 0 != 1:
#     print(talkDict["start"])
#     inpt = input("Input: \n")
#     for i in x:
#         zz = re.search('{(.*)}', i)  # Searched for any word (options) surrounded by curly brackets.
#         if zz is None:
#             None # filters out fields without.
#         else:
#             try:
#                 y = zz.group(0)[1:-1].lower() # Removes curly brackets.
#                 # Looks for instances of options in input- allows user to write full sentences.
#                 if y in inpt.lower():
#                     x = talkDict[y].split("|")
#                     break
#             except KeyError:
#                 print("Error")


v1 = "wfw|wf|werf|1,2,3,4"
v2 = v1.split("|")[3].split(",")
print(int(v2[0]) + 1)



moves = ["slash","lunge","push","pierce"]
movesDict = {
    "slash":"feint|parry",
    "lunge":"slash|feint",
    "push":"lunge|slash",
    "pierce":"push|lunge",
    "riposte":"pierce|push",
    "parry":"riposte|pierce",
    "feint":"parry|riposte"
}


print(list(movesDict.keys())[0])
ran = random.randint(0, len(moves) - 1)
enemyMove = moves[0]
out = "The enemy tries a " + enemyMove
#
# This part finds the time by seconds.
# Changes what the enemy counters with based on if # is divis by 3.
#
timeThing = int(strftime("%S", gmtime()))
if (timeThing % 3) ==0:
    moveCounter = movesDict.get(enemyMove).split("|")[0]
else:
    moveCounter = movesDict.get(enemyMove).split("|")[1]

while True == True:

    inp = input(out+"\n").lower() # What the player typed, lower case.

    inp = inp.split(" ") # splits input into individual works
    zz = "incorrect"
    timeThing = int(strftime("%S", gmtime()))
    for i in inp:
        if moveCounter and not moveCounter in i and i in movesDict:
            print("naught")
            zz = "incorrect"
            enemyMove = moves[0]
            out = "The enemy tries a " + enemyMove
            moveCounter = movesDict.get(enemyMove)
            break
        elif moveCounter and moveCounter in i:
            zz = "correct"
            enemyMove = movesDict.get(i)
            out = "The enemy tries a " + enemyMove
            moveCounter = movesDict.get(enemyMove)

    print(zz)
