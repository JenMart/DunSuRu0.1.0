class textDAO:
    def __init__(self,x):
        self.__x = x
        #
        # VARIABLES FOR THE VARIABLE GOD.
        #
    def get_encounters(self, x, y):

        subDict = {"NP": " You are alone.{Walk}|wlk"}
        ratDict = {
            "x": "The rats have been slain.|wlk",
            0: " You see the body of a dead rat.|wlk",
            1: " You see a single rat.|cmb",
            2: " You see two rats.|cmb",
            3: " You see a trio of rats.|cmb",
            4: " You see a swarm of rats.|cmb"
        }
        banditDic = {
            "x": " The bandit was defeated.|wlk",
            0: " You see the body of a dead bandit.|mel",
            1: " You see a bandit on the ground at the mercy of your blade.|mel",
            2: " You see an injured bandit.|mel",
            3: " You see a Bandit with eyes full of greed.|mel",
            4: " You see a Bandit with eyes full of greed.|mel"
        }
        monsterDic = {
            "x": "You have slain the monster.|wlk",
            0: " You see no monster.|wlk",
            1: " You see a single monsters.|cmb",
            2: " You see two monsters.|cmb",
            3: " You see a trio of monsters.|cmb",
            4: " You see a swarm of monsters.|cmb"
        }
        encDict= {
            "R": ratDict[y],
            "M": monsterDic[y],
            "L": " A pile of loot crosses your path.|itr",
            "T": " A trap springs nearby.|itr",
            "B": banditDic[y],
            "N": " An angry bandit brandishing a weapon.|cmb",
            "Z": " The Basilisk of Carrows Way appears before you.|tlk",
            "E": subDict["NP"]
        }
        return encDict[x]

    def get_special(self, x, y):
        banditDict = {
            "PSF": " |{Attack}|{Free Shot}|{Item}|{Talk}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        ratDict = {
            "PSF": " |{Attack}|{Free Shot}|{Item}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        monsterDict = {
            "PSF": " |{Attack}|{Free Shot}|{Items}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        specialDict= {
            "R": ratDict[y],
            "B": banditDict[y],
            "M": monsterDict[y]
        }
        return specialDict[x]
    def get_damage(self, x, job):
        print(job)
        dmgDictBandit = {
            "free Shot": "You strike the unaware opponent and deal $$ damage.|1",
            "item": "You throw a vile of alchemist fire and deal $$ damage.|1",
            "attack": "You deal $$ damage as you clash with your opponent.|1"
        }
        dmgDict = {
            "bandit":dmgDictBandit[x]
        }
        return dmgDict[job]

    def get_Dungeon(self,x):
        #
        # Main : North,South,East,West
        # p = exit/start
        # x = empty
        #
        dunDict = {
            "1^1": "p,2^1,x,x,BRMLT",
            "2^1": "1^1,x,2^2,x,ZZZZ", # All rats all the time.
            "2^2": "x,3^2,x,2^1,BBBB", # Dem' bandits.
            "3^2": "2^2,4^2,x,x,RRR", # Monsters but less.
            "4^2": "3^2,x,4^3,x,BRMLT",
            "4^3": "x,5^3,x,4^2,BRMLT",
            "5^3": "4^3,6^3,x,x,BRMLT",
            "6^2": "x,7^2,6^3,x,BRMLT",
            "6^3": "5^3,x,6^4,6^2,BRMLT",
            "6^4": "x,7^4,x,6^3,BRMLT",  # fixed
            "7^2": "6^2,8^2,x,x,BRMLT",
            "7^4": "6^4,8^4,x,x,BRMLT",
            "8^2": "7^2,x,8^3,x,BRMLT",
            "8^3": "x,x,8^4,8^2,BRMLT",
            "8^4": "7^4,9^4,8^5,8^3,BRMLT",
            "8^5": "x,x,x,8^4,BRMLT",
            "9^4": "8^4,x,x,x,BRMLT"  # fixed
        }
        try:
            return dunDict[x]
        except KeyError:
            return "You narrowly escape a void."

    def get_talk(self,x,y):
        talkDict = {
            "00": "This is not a valid option.|tlk",
            "start": " You meet the Basilisk of Carrows Way. 'Speak adventurer.'"
                     " It hisses from a miasmic cloud. |{OK}|I wish you {peace}|{Hail} and well met|tlk",
            "ok": "It eyes you dispassionately with a weight of infinite patients."
                  " 'Tell me what you seek.' |A {purpose}|{An answer}|{Wealth}|{Fame}|tlk",
            "peace": "“How fortuitous.” it chortles mirthlessly. 'These halls lay empty for sometime. What do seek?' |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk",
            "hail": "its eye reveal a hint of surprise. “Such politeness to a beast such as myself. Do you speak so out of fear or a sense of obligation?”  |{Fear}|{Obligation}|tlk",
            "fame": "Many live to have their names written in the scrolls of history but few scrolls have survived The End|{exit}|tlk",
            "wealth": "Gold and jewels are said to be overrated but few can argue against the comfort they bring. Would you be satisfied with facing The End of luxury?|{exit}|tlk",
            "answer": "I am sorry to say but you shall not find an answer here.|{exit}|tlk",
            "fear": "I will not eat my first visitor in eons. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk",
            "obligation": "Good to see the old ways are not dead. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk",
            "purpose": "In this I cannot help.|{exit}|tlk",
            "exit": "Luck upon your travels.|wlk"
        }
        #
        # try/catch used in chance if misspelling in options.
        # I should use an if statement but this covers both dict calls so... yeah.
        #
        try:
            charDict = {
                "Z": talkDict[y]
            }
            return charDict[x]
        except KeyError:
            return "The words are went unheard."

    def getMelee(self,x):
        moves = ["slash", "lunge", "push", "pierce","riposte","parry","feint"]
        movesDict = {
            "slash": "feint|parry",
            "lunge": "slash|feint",
            "push": "lunge|slash",
            "pierce": "push|lunge",
            "riposte": "pierce|push",
            "parry": "riposte|pierce",
            "feint": "parry|riposte"
        }
        try:
            return movesDict[x]
        except KeyError:
            return "Your strike connects with nothing."