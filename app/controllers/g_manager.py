from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
from app.models.textDAO import textDAO
import random
import re
from time import gmtime, strftime




class Main:
    def __init__(self):
        self.db_mgmt = DatabaseManager()
        self.twt_print = printTwt()
        self.CharDAO = CharDAO
        self.textDAO = textDAO

    def handleChoice(self, input, userName, createDate, tweetID):
        #
        # checks to see if user info already exists. If it does not, adds to DB.
        #
        checkUser = self.db_mgmt.checkUser(userName)
        if (checkUser):  # If not, add to DB
            self.db_mgmt.addUser(userName, createDate, tweetID)
        choice = input.lower()
        #
        # Figure out how to store function calls in a dict without it calling them all!
        #
        checkChar = self.db_mgmt.checkCharacter(userName)
        if (checkChar):
            if "new" in choice or "start" in choice:
                self.db_mgmt.addChar(userName, "The"+userName)
                charTuple = self.db_mgmt.pullCharacter(userName)
                self.char = CharDAO(charTuple[0], charTuple[1], charTuple[2], charTuple[3], charTuple[4], charTuple[5],
                                    charTuple[6],
                                    charTuple[7], charTuple[8], charTuple[9])
                output = self.newCharacter(userName)
            else:
                output = "You do not possess a character. Type {Start} or {New} to begin playing."
        else:
            # try:
            charTuple = self.db_mgmt.pullCharacter(userName)
            self.char = CharDAO(charTuple[0], charTuple[1], charTuple[2], charTuple[3], charTuple[4], charTuple[5],
                                charTuple[6],
                                charTuple[7], charTuple[8], charTuple[9])
            if "items" in choice or "item" in choice:
                output = self.useItem(choice)
            elif "look" in choice:
                output = self.lookAround()
            elif "summon the basilisk of carrows way." in choice:
                output = self.converse(choice)
            elif self.char.state == "wlk":
                output = self.moveto(choice)
            elif self.char.state == "cmb":
                output = self.combat(choice)
            elif self.char.state == "mel": #Two sep combat types. May combine later.
                output = self.meleeCombat(choice)
            elif self.char.state == "itr":
                output = self.interact(choice)
            elif self.char.state == "tlk":
                output = self.converse(choice)
            else:
                output = "This is not a valid option."
            self.db_mgmt.updateUser(userName, tweetID, createDate, self.char)
            # except Exception as e:
            #     print('Error: ' + str(e))
            #     pass
        return output


    def useItem(self, input):
        itemsCut = self.char.items.lower().split(",")
        output = ""
        if "show" in input:
            output = "You hold in your possession: "
            for i in itemsCut:
                output += i.replace("|"," x") + ", "
            output = output[:-1]
        elif "use" in input:
            for i in itemsCut:
                i = i.split("|")[0]
                print(i)
                if i in output:
                    output = "You use " + i
                    break
                else:
                    output = "You do not possess this item."
        else:
            output = "You have selected an invalid option."

        return output

    def newCharacter(self,userName):
        #
        # Full character creator will be added in later.
        #
        look = self.lookAround()
        # encounter = self.encounter()
        output = userName + " has been created." + look
        return output

    def moveto(self, input):
        imp = input
        #
        # For sake of sanity, all dungeons start at 1:1 until stated otherwise.
        #
        dungeon = textDAO("pojihudew")
        nor = dungeon.get_Dungeon(self.char.POS).split(",")[0]
        sou = dungeon.get_Dungeon(self.char.POS).split(",")[1]
        eas = dungeon.get_Dungeon(self.char.POS).split(",")[2]
        wes = dungeon.get_Dungeon(self.char.POS).split(",")[3]
        if "north" in imp and nor != "x":
            output = "You go north."
            self.char.POS = nor
        elif "south" in imp and sou != "x":
            output = "You go south."
            self.char.POS = sou
        elif "east" in imp and eas != "x":
            output = "You go east."
            self.char.POS = eas
        elif "west" in imp and wes != "x":
            output = "You go west."
            self.char.POS = wes
        else:
            output = "This is not a valid choice."


        if self.char.POS == "p":
            self.char.POS = "1^1"
            output = "The exit is closed off."

        output += self.lookAround()
        output += self.encounter()
        return output

    def interact(self, input):
        x = self.char.tracker.split(",")
        for i in x:
            if self.char.POS in i:
                enc = i.split("|")[1]  # encounter
                phs = i.split("|")[2]  # Encounter phase
                num = i.split("|")[3]  # number of things in encounter
                break
        # print(enc)
        if "evade" in input and enc == "T":
            output = "You deftly avoid the swinging blades."
            self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
            self.char.state = "wlk"
        elif "disarm" in input and enc == "T":
            output = "With nimble fingers, you safely disable the arrow trap."
            self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
            self.char.state = "wlk"
        elif "inspect" in input and enc == "L":
            output = "The treasure looks safe."
        elif "take" in input and enc == "L":
            output = "With a quick swipe you push the loot into your bag."
            self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
            self.char.state = "wlk"
        else:
            output = "This is not a valid choice."
        output += self.lookAround()
        output += self.encounter()
        return output



    def converse(self, input):
        #
        # Under construction.
        #
        output = ""
        text = textDAO("nfeqwhgwtwg")
        x = self.char.tracker.split(",")
        for i in x:
            if self.char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter (name of thing you're talking to)
        phs = counter.split("|")[2]  # Encounter phase (Where in conversation)
        place = counter.split("|")[3]  # friendliness meter. (add feature later)
        conversation = text.get_talk(enc, phs).split("|")
        for i in conversation:
            convParsed = re.search('{(.*)}', i)
            if convParsed is None:
                None
            else:
                response = convParsed.group(0)[1:-1].lower()
                if response in input:
                    out = text.get_talk(enc, response)
                    if not out:
                        # Note: If you're here, someone fucked up.
                        output = "Your response is invalid."
                    else:
                        output = out[:-4]
                        updateCell = self.char.POS + "|" + enc + "|" + response + "|" + "0"
                        self.char.tracker = self.char.tracker.replace(counter, updateCell)
                        self.char.state = out[-3:]
                    break
                else:
                    output = "This is not a valid option"
        if self.char.state == "wlk":
            output += "You are now alone. " + self.lookAround()
        return output

    def meleeCombat(self, input):
        text = textDAO("lkjge9423r")
        tracker = self.char.tracker.split(",")
        for i in tracker:
            if self.char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter
        phase = counter.split("|")[2]  # Encounter phase
        enemyHealth = int(counter.split("|")[3])  # number of things in encounter
        playerHealth = int(counter.split("|")[4])
        moveTracker = counter.split("|")[5]
        #
        # Moves array is inefficient. Find better solution later.
        #
        moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
        #
        # This part finds the time by seconds.
        # Changes what the enemy counters with based on if # is divis by 3.
        #
        secTracker = int(strftime("%S", gmtime()))
        inputSplit = input.split(" ")
        moveCounter = text.getMelee(phase)
        for i in inputSplit:
            # If incorrect
            if phase == "win":
                if "spare" in input:
                    output = "You have spared the enemies life."
                    enemyHealth = 0
                    break
                elif "slay" in input:
                    output = "You have slain the enemy"
                    enemyHealth = 0
                    break
                else:
                    output = "The world unfocuses for a moment."
                    enemyHealth = 0
            elif phase == "lose":
                if "surrender" in input:
                    output = "You successfully barter for your life."
                    playerHealth = 0
                    break
                elif "last ditch" in input:
                    if (secTracker % 4) == 0: # gives players 1/4 chance of success
                        output = "Your attack surprises the enemy."
                        enemyHealth = 0
                    else:
                        output = "Your last ditch effort failed."
                        playerHealth = 0
                    break
                else:
                    output = "The world inverses but soon returns to normal."

            else:
                if i not in moveCounter and i in moves or i in moveTracker or i == "fail":
                    if secTracker < len(moves) and phase != moves[secTracker]:
                        phase = moves[secTracker]
                    else:
                        rand = random.randint(1,len(moves))-1
                        if phase != moves[rand]:
                            phase = moves[rand]
                        else:
                            phase = text.getMelee(i).split("|")[0]
                    playerHealth -= 1
                    output = "You failed to counter. P: " + str(playerHealth) + " E: " + str(enemyHealth)
                    break
                # If correct
                elif i in moveCounter and i != "|":
                    if (secTracker % 3) == 0:
                        # print("One "+ text.getMelee(i).split("|")[1])
                        phase = text.getMelee(i).split("|")[0]
                    else:
                        # print("Two "+ text.getMelee(i).split("|")[0])
                        phase = text.getMelee(i).split("|")[1]
                    enemyHealth -= 1
                    output = "You countered the attack. P: " + str(playerHealth) + " E: " + str(enemyHealth)
                    moveTracker += i
                else:
                    output = "That is not a valid option."

        if enemyHealth > 1 and playerHealth > 1: # If battle is normal
            updateCell = self.char.POS + "|" + enc + "|" + phase + "|" + str(enemyHealth) + "|" + str(playerHealth) + "|" + moveTracker
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            self.char.state = updateEncounter[1]
            output += updateEncounter[0] + " The enemy tries a " + phase
            for x in moves:
                if x not in moveTracker:
                    output += "|{" + x + "}"
        elif enemyHealth == 1 and playerHealth > 0: # If enemy is brought to 1 HP
            updateCell = self.char.POS + "|" + enc + "|" + "win" + "|" + str(enemyHealth) + "|" + str(playerHealth) + "|" + moveTracker
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            self.char.state = updateEncounter[1]
            output = updateEncounter[0] + "|{Spare}|{Slay}"
        elif playerHealth == 1 and enemyHealth > 0: # If player is brought to 1 HP
            updateCell = self.char.POS + "|" + enc + "|" + "lose" + "|" + str(enemyHealth) + "|" + str(playerHealth) + "|" + moveTracker
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            self.char.state = updateEncounter[1]
            output = updateEncounter[0] + " You are at the mercy of its sword|{Last Ditch}|{Surrender}"
        elif enemyHealth <= 0: # If enemy is defeated
            updateCell = self.char.POS + "|" + enc + "|" + "EP" + "|" + str(0) + "|" + str(playerHealth) + "|" + moveTracker
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, "x").split("|")
            self.char.state = updateEncounter[1]
            output += updateEncounter[0] + " The passage is now empty."
        else: # If player is defeated. NOTE: Will default to enemy wining ATM.
            updateCell = self.char.POS + "|" + enc + "|" + "EP" + "|" + str(0) + "|" + str(playerHealth) + "|" + moveTracker
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, "x").split("|")
            self.char.state = updateEncounter[1]
            output += " Your failure goes unrecorded." + " The passage is now empty."
        print(updateCell)
        return output

    def combat(self, input):
        text = textDAO("ntergo;ybw")
        damage = 0
        tracker = self.char.tracker.split(",")
        for i in tracker:
            if self.char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter
        phase = counter.split("|")[2]  # Encounter phase
        num = int(counter.split("|")[3])  # number of things in encounter
        ablities = text.get_special(enc, phase).split("|")
        #####################
        for i in ablities:
            ablitiesParsed = re.search('{(.*)}', i)  # Searched for any word (options) surrounded by curly brackets.
            if ablitiesParsed is None:
                None
            else:
                action = ablitiesParsed.group(0)[1:-1].lower()  # Removes curly brackets.
                # Looks for instances of options in input- allows user to write full sentences.
                if action in input:
                    damage = text.get_damage(action,"bandit").split("|")
                    num -= int(damage[1])
                    break
                else:
                    damage = ["that is not a valid option you do $$ damage.",0]
        #####################
        if num > 0:
            updateCell = self.char.POS + "|" + enc + "|" + "BP" + "|" + str(num)
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncount = text.get_encounters(enc, num).split("|")
            output = damage[0].replace("$$",str(damage[1])) +  updateEncount[0] + text.get_special(enc,phase)
            self.char.state = updateEncount[1]
        else:
            updateCell = self.char.POS + "|" + enc + "|" + "EP" + "|" + str(0)
            self.char.tracker = self.char.tracker.replace(counter, updateCell)
            updateEncount = text.get_encounters(enc, "x").split("|")
            output = updateEncount[0] + " The passage is now empty."
            self.char.state = updateEncount[1]
        return output

    def lookAround(self):
        output = " You see"
        text = textDAO("pojihudew")
        nor = text.get_Dungeon(self.char.POS).split(",")[0]
        sou = text.get_Dungeon(self.char.POS).split(",")[1]
        eas = text.get_Dungeon(self.char.POS).split(",")[2]
        wes = text.get_Dungeon(self.char.POS).split(",")[3]
        if nor != "x":
            if nor == "p":
               output += " the exit to the north,"
            else:
               output += " a passage north,"
        if sou != "x":
            if sou == "p":
               output += " the exit to the south,"
            else:
               output += " a passage south,"
        if eas != "x":
            if eas == "p":
               output += " the exit to the east,"
            else:
               output += " a passage east,"
        if wes != "x":
            if wes == "p":
               output += " The exit to the west,"
            else:
               output += " a passage west,"
        #
        # Replaces last character with a period.
        #
        output = output[:-1] + "."
        # output += self.encounter()
        return output

    def encounter(self):
        phs = "xx"
        # e = dunDict[self.char.POS].split(",")[4]
        enc = ""
        num = 4
        #
        # looks to see if player has visited square.
        # There is an easier way called "numpy" but... pfft.
        #
        text = textDAO("ytjwvcewrv")
        # print(self.char.POS)
        e = text.get_Dungeon(self.char.POS).split(",")[4]
        randy = random.randint(0, len(e)-1)
        if self.char.POS in self.char.tracker: #If encounter exists in this square
            x = self.char.tracker.split(",")
            for i in x: # Looks for space
                if self.char.POS in i: # If finds space, slices into chunks.
                    enc = i.split("|")[1] # encounter
                    phs = i.split("|")[2] # Encounter phase
                    num = int(i.split("|")[3]) # number of things in encounter
                    # print(num)
                    break
            if num > 0:
                output = text.get_encounters(enc, num).split("|")[0] + text.get_special(enc, phs) + "|"
            else:
                output = text.get_encounters(enc, num).split("|")[0]

        else: #If new encount is made, setup here.
            enc = e[randy] #z
            output = text.get_encounters(enc, num).split("|")  # All encounters set to max
            self.char.state = output[1]
            output = output[0]

            if self.char.state == "cmb": # Go here if state = combat
                # if randy > 2: # Reminder to change phase system.
                #     phs = "PSF"
                # else:
                #     phs = "ESF"
                if num != "0":
                    if enc == "B":
                        moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
                        secTracker = int(strftime("%S", gmtime())) # May use later.
                        phs = moves[0]  # slash by default until futher notice.
                        output += " They come at you with a " + phs  # Using phase to track what move enemy used.
                        for i in moves:
                            output += "|{" + i + "}"
                    else:
                        if num > 1:  # changes pronoun based on number of enemies in encounter.
                            output += " They"
                        else:
                            output += " It"
                        # if phs == "PSF":
                        if randy > 2:
                            phs = "PSF"
                            output += " does not spot the player." + text.get_special(enc, phs) + "|"
                        # elif phs == "ESF":
                        else:
                            phs = "ESF"
                            output += " spots the player." + text.get_special(enc, phs) + " |"
                else:
                    output = " The passage is empty."
                    self.char.state = "wlk"
            if self.char.state == "tlk":
                output = text.get_talk(enc, "start").split("|")[0]
                phs = "start"

            self.char.tracker += "," + self.char.POS + "|" + enc + "|" + phs + "|" + "5" + "|" + "5" + "|"#trying a new battle system.
            # self.char.tracker += "," + self.char.POS + "|" + enc + "|" + phs + "|" + str(num)   # All encounters set to max
            # Temp changed to make sure every passage has an encounter.


        #
        # If 0 encounters in square, system acts like it's empty.
        #
        return output

    ##
    ## Deprecated. Kept because The Lady demands it.
    ##

    # def combatDeprecated(self, input):
    #     x = self.char.tracker.split(",")
    #     for i in x:
    #         if self.char.POS in i:
    #             enc = i.split("|")[1]  # encounter
    #             phs = i.split("|")[2]  # Encounter phase
    #             num = i.split("|")[3]  # number of things in encounter
    #             break
    #     if "fight" in input:
    #         output = "You quickly dispatch the enemy. DunSuRu grows safer."
    #         self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
    #         self.char.state = "wlk"
    #         output += self.lookAround()
    #     elif "distract" in input and enc == "R":
    #         output = "You throw a morsel of food, the hungry beast scampers off. The way is clear but your " \
    #                  "provisions grow scarce."
    #         self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
    #         self.char.state = "wlk"
    #         output += self.lookAround()
    #     elif "sneak" in input and enc == "M":
    #         output = "You time your weary steps in sync with the pacing of the monster. You watch from the shadows as" \
    #                  "it stalks off."
    #         self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
    #         self.char.state = "wlk"
    #         output += self.lookAround()
    #     elif "calm" in input and enc == "N":
    #         output = "The bandit weapon lowers. They eye you suspiciously."
    #         self.char.tracker = self.char.tracker.replace(enc+str(num), "B" +str(num))
    #         self.char.state = "tlk"
    #     else:
    #         output = "This isn't a valid choice."
    #     output += self.encounter()
    #     return output
    #
    # def talk(self, input):
    #     x = self.char.tracker.split(",")
    #     for i in x:
    #         if self.char.POS in i:
    #             enc = i[-2:-1]  # encounter
    #             num = i[-1:]  # number of things in encounter
    #             break
    #     if "bribe" in input and enc == "B":
    #         output = "You hand over your gold. The bandit leaves with a tip of his imaginary hat."
    #         self.char.tracker = self.char.tracker.replace(enc+str(num), enc+str(0))
    #         self.char.state = "wlk"
    #         output += self.lookAround(self.char.POS)
    #     if "talk" in input and enc == "B":
    #         output = "The bandit grows angry with your banter and draws a vicious saber."
    #         self.char.tracker = self.char.tracker.replace(enc + str(num), "N" + str(num))
    #         self.char.state = "cmb"
    #     return output