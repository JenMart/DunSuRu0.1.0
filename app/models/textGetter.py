class textDAO:
    def __init__(self,x):
        self.__x = x
        #
        # VARIABLES FOR THE VARIABLE GOD.
        #
    def get_encounters(self, x, y):
        # y = 4
        if y > 4:
            y = 4
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
        trapDict = {
            "x": "You have bested the trap.|wlk",
            0: " a defeated trap.|itr",
            1: " a defeated trap..|itr",
            2: " a sprung trap|itr",
            3: " a disarmed trap.|itr",
            4: " a trap about to sprint.|itr"
        }
        puzzleDict= {
            "x": "You have solved the puzzle|wlk",
            0: " a solved puzzle|wlk",
            1: " a puzzle with one X's.|PZL",
            2: " a puzzle with two X's.|PZL",
            3: " a puzzle with three X's.|PZL",
            4: " a puzzle with four X's.|PZL"
        }
        lootDict = {
            "x": "You have solved the chest.|wlk"
            , 0: "You find a smashed chest.|wlk"
            , 1: "You come across an opened chest.|itr"
            , 2: " You see a chest.|itr"
            , 3: " You see a chest.|itr"
            , 4: " You see a chest.|itr"
        }
        encDict= {
            "P": puzzleDict[y]
            , "R": ratDict[y]
            , "M": monsterDic[y]
            , "L": lootDict[y]
            , "T": trapDict[y]
            , "B": banditDic[y]
            , "N": " An angry bandit brandishing a weapon.|cmb"
            , "Z": " The Basilisk of Carrows Way appears before you.|tlk"
            , "E": subDict["NP"]
        }
        return encDict[x]

    def get_puzzle(self, x):
        #
        # a | 
        #
        puzzleDict = {
            "x":"Choose the {Top}, {Bottom} or {Middle} disk | Then choose to rotate {Right} or {Left}"
        }
        return puzzleDict[x]

    def get_special(self, x, y):
        banditDict = {
            "xx": "|",
            "PSF": " |{Attack}|{Free Shot}|{Item}|{Talk}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        ratDict = {
            "xx": "|",
            "PSF": " |{Attack}|{Free Shot}|{Item}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        monsterDict = {
            "xx": "|",
            "PSF": " |{Attack}|{Free Shot}|{Items}",
            "ESF": " |{Attack}|{Item}",
            "BP": " |{Attack}|{Item}"
        }
        trapDict = {
            "xx":"|{evade}|{disarm}"
        }
        specialDict= {
            "T": trapDict[y],
            "R": ratDict[y],
            "B": banditDict[y],
            "M": monsterDict[y]

        }
        return specialDict[x]
    def get_damage(self, x, job):
        print(job)
        dmgDictBandit = {
            "free Shot": "You strike the unaware opponent and deal $$ damage.|1"
            , "item": "You throw a vile of alchemist fire and deal $$ damage.|1"
            , "attack": "You deal $$ damage as you clash with your opponent.|1"
        }
        dmgDict = {
            "bandit":dmgDictBandit[x]
        }
        return dmgDict[job]

    def get_Dungeon(self, x):
        #
        # B = bandits, mel
        # R = rats, cmb
        # M = monsters, cmb
        # L
        # T
        # P = puzzle, PZL
        #
        dunDict = {
            "1^1": "p,2^1,x,x,BRMLT"
            , "2^1": "1^1,x,2^2,x,LLLLLLLLLLLL"
            , "2^2": "x,3^2,x,2^1,LLL"
            , "3^2": "2^2,4^2,x,x,RRR"
            , "4^2": "3^2,x,4^3,x,BRMLT"
            , "4^3": "x,5^3,x,4^2,BRMLT"
            , "5^3": "4^3,6^3,x,x,BRMLT"
            , "6^2": "x,7^2,6^3,x,BRMLT"
            , "6^3": "5^3,x,6^4,6^2,BRMLT"
            , "6^4": "x,7^4,x,6^3,BRMLT"
            , "7^2": "6^2,8^2,x,x,BRMLT"
            , "7^4": "6^4,8^4,x,x,BRMLT"
            , "8^2": "7^2,x,8^3,x,BRMLT"
            , "8^3": "x,x,8^4,8^2,BRMLT"
            , "8^4": "7^4,9^4,8^5,8^3,BRMLT"
            , "8^5": "x,x,x,8^4,BRMLT"
            , "9^4": "8^4,x,x,x,BRMLT"
        }
        try:
            return dunDict[x]
        except KeyError:
            return "You narrowly escape a void."

    def get_interact(self, x, y):
        #
        # Interact works not unlike talk.
        #
        treasureDict = {
            "start":" The chest appears locked.| {Open} the lid.| examine the {lock}.| examine the {sides}.|itr"
            , "open": "The lock holds steady.| attempt to {force} the lid open.| examine the {lock}.| examine the {sides}.|itr"
            , "lock": "It's a simple lock, you may be able to pick it| attempt to {pick} the lock.| try to {force} the lid.| examine the {sides}.|itr"
            , "sides": "You walk clockwise around the chest. When you reach the back a second time, you see a lever| {Pull} the lever.|itr"
            , "pull":"The lever slides down and finishes with a satisfying click.| {Check} inside.|itr"
            , "pickFAIL":"Your pick breaks, sealing the lock. | attempt to {force} the lid open.| examine the {lock}.| examine the {sides}."
            , "pickSUCCESS":"The pick strikes true and the lock clatters to the floor| {Check} inside.|itr"
            , "forceFAIL":"In your attempt to break the lock you smash the contents of the chest. All you find is torn parchment.| {Move} on.|wlk"
            , "forceSUCCESS": "With unerring precision you break the lock off while leaving the chest unmolested.| {Check} inside.|itr"
            , "check": "Inside you discover scrolls of a forgotten age. Without thought you place them within your bag.|wlk"
        }
        if x == "L":
            return treasureDict[y]
        else:
            return False


    def get_talk(self, x, y):
        talkDict = {
            "00": "This is not a valid option.|tlk"
            , "start": " You meet the Basilisk of Carrows Way. 'Speak adventurer.'"
                     " It hisses from a miasmic cloud. |{OK}|I wish you {peace}|{Hail} and well met|tlk"
            , "ok": "It eyes you dispassionately with a weight of infinite patients."
                  " 'Tell me what you seek.' | A {purpose}.| An {answer}.| enough {Wealth} to live |{Fame}|tlk"
            , "peace": "“How fortuitous.” it chortles mirthlessly. 'These halls lay empty for sometime. What do seek?' | A {purpose}|An {answer}|{Wealth}|{Fame}|tlk"
            , "hail": "its eye reveal a hint of surprise. “Such politeness to a beast such as myself. Do you speak so out of fear or a sense of obligation?”  |{Fear}|{Obligation}|tlk"
            , "fame": "Many live to have their names written in the scrolls of history but few scrolls have survived The End.|{exit}|tlk"
            , "wealth": "Gold and jewels are said to be overrated but few can argue against the comfort they bring. Would you be satisfied with facing The End of luxury?|{exit}|tlk"
            , "answer": "I am sorry to say but you shall not find an answer here.|{exit}|tlk"
            , "fear": "I will not eat my first visitor in eons. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk"
            , "obligation": "Good to see the old ways are not dead. Tell me what you wish. |A {purpose}|An {answer}|{Wealth}|{Fame}|tlk"
            , "purpose": "In this I cannot help.|{exit}|tlk"
            , "exit": "Luck upon your travels.|wlk"
        }
        if x == "Z":
            return talkDict[y]
        else:
            return False

    def get_traps(self, x, y):
        trapDict = {
            1: " A blade appears from the ceiling and heads straight for you. Jump {Right} or {Left} to avoid|swingR"
            , 2: " From the ceiling a blade appears and heads straight for you. Jump {Right} or {Left} to avoid|swingL"
        }
        return trapDict[x]


    def get_melee(self, x):
        movesDict = {
            "slash": "feint|parry"
            , "lunge": "slash|feint"
            , "push": "lunge|slash"
            , "pierce": "push|lunge"
            , "riposte": "pierce|push"
            , "parry": "riposte|pierce"
            , "feint": "parry|riposte"
        }
        try:
            return movesDict[x]
        except KeyError:
            return "Your strike connects with nothing."
