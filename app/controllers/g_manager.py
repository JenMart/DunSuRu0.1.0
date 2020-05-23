from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
from app.models.textGetter import textDAO
from app.models.userData import userData
from app.controllers.combat_manager import combatManager
from app.controllers.new_character import newCharacter
from app.controllers.interact_manager import interactManager
from app.controllers.talk_manager import talkManager
from app.controllers.item_manager import itemManager
from app.controllers.puzzle_manager import puzzleManager
from app.models.parsers import parsers
import random
import re
from time import gmtime, strftime




class Main:
    def __init__(self):
        self.db_mgmt = DatabaseManager()
        self.twt_print = printTwt()
        self.CharDAO = CharDAO
        self.textDAO = textDAO
        self.userData = userData
        self.combatManager = combatManager
        self.newCharacter = newCharacter
        self.interact = interactManager
        self.talk = talkManager
        self.items = itemManager
        self.puzzles = puzzleManager
        self.parser = parsers


    def handleChoice(self, input, userName, createDate, tweetID):

        #
        # checks to see if user info already exists. If it does not, adds to DB.
        #
        self.user = userData(userName, createDate, input, tweetID)
        checkUser = self.db_mgmt.checkUser(userName)
        if (checkUser):  # If not, add to DB
            self.db_mgmt.addUser(userName, createDate, tweetID)
        input = input.lower()
        #
        # Figure out how to store function calls in a dict without it calling them all!
        #
        checkChar = self.db_mgmt.checkCharacter(userName)
        if (checkChar):
            if "new" in input or "start" in input:
                new_char = newCharacter()
                self.db_mgmt.addChar(userName, userName)
                charTuple = self.db_mgmt.pullCharacter(userName)
                self.char = CharDAO(charTuple[0], charTuple[1], int(charTuple[2]), charTuple[3], charTuple[4], charTuple[5],
                                    charTuple[6],
                                    charTuple[7], charTuple[8], charTuple[9], charTuple[10])
                output = new_char.newCharacter(userName)
                output += self.lookAround()
            else:
                output = "You do not possess a character. Type {Start} or {New} to begin playing."
        else:
            # try:
            charTuple = self.db_mgmt.pullCharacter(userName)
            self.char = CharDAO(charTuple[0], charTuple[1], charTuple[2], charTuple[3], charTuple[4], charTuple[5],
                                charTuple[6],
                                charTuple[7], charTuple[8], charTuple[9], charTuple[10])

            if self.char.POS == "p":
                None
            else:

                # elif "summon the basilisk of carrows way." in input:
                #     converse = talkManager()
                #     output = converse.converse(input)
                if self.char.state == "wlk":
                    output = self.moveto(input)
                    output += self.lookAround()
                    output += self.encounter(userName)
                elif self.char.state == "cmb":
                    combat_manager = combatManager()
                    output = combat_manager.groupCombat(input, self.char)
                    # output += self.lookAround()
                    # output += self.encounter()
                elif self.char.state == "mel": #Two sep combat types. May combine later.
                    combat_manager = combatManager()
                    output = combat_manager.meleeCombat(input, self.char)
                    # output += self.lookAround()
                    # output += self.encounter()
                elif self.char.state == "itr":
                    interact = interactManager()
                    output = interact.interact(input, self.char)
                    # output += self.lookAround()
                    # output += self.encounter()
                elif self.char.state == "tlk":
                    talk_manager = talkManager()
                    output = talk_manager.converse(input)
                elif self.char.state == "PZL":
                    puz = puzzleManager()
                    output = puz.puzzles(input, self.char)

                    # output += self.lookAround()
                    # output += self.encounter()
                elif "items" in input or "item" in input and self.char.state != "cmb":
                    item_manager = itemManager()
                    output = item_manager.useItem(input, self.char)
                elif "look" in input:
                    output = self.lookAround()
                    output += self.encounter(userName)
                else:
                    output = "This is not a valid option."



                self.db_mgmt.updateUser(userName, tweetID, createDate, self.char)
                # except Exception as e:
                #     print('Error: ' + str(e))
                #     pass

            if self.char.health < 0: # This is intentional.
                output = "{} has fallen on this day. Their legacy will be remembered as people remember the clouds that bring rain."

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
            output = "You go north. "
            self.char.POS = nor
        elif "south" in imp and sou != "x":
            output = "You go south. "
            self.char.POS = sou
        elif "east" in imp and eas != "x":
            output = "You go east. "
            self.char.POS = eas
        elif "west" in imp and wes != "x":
            output = "You go west. "
            self.char.POS = wes
        else:
            output = "This is not a valid choice."
        #
        # If player attempts to leave, system currently places them back at starting square.
        #
        if self.char.POS == "p":
            if self.char.WINCON == "Permitted.":
                output = "You step in the sun. For the moment there is respite. Do you brave the depths of Carrows Way again?| {Yes} or {No}."
            else:
                self.char.POS = "1^1"
                output = "The exit is closed off."
        return output

    def lookAround(self):
        output = " You see"
        text = textDAO("pojihudew")
        dungeon = text.get_Dungeon(self.char.POS)
        nor = dungeon.split(",")[0]
        sou = dungeon.split(",")[1]
        eas = dungeon.split(",")[2]
        wes = dungeon.split(",")[3]
        des = dungeon.split(",")[5]

        output = des
        # if nor != "x":
        #     if nor == "p":
        #        output += " the exit to the north,"
        #     else:
        #        output += " a passage north,"
        # if sou != "x":
        #     if sou == "p":
        #        output += " the exit to the south,"
        #     else:
        #        output += " a passage south,"
        # if eas != "x":
        #     if eas == "p":
        #        output += " the exit to the east,"
        #     else:
        #        output += " a passage east,"
        # if wes != "x":
        #     if wes == "p":
        #        output += " The exit to the west,"
        #     else:
        #        output += " a passage west,"
        #
        # Replaces last character with a period.
        #
        output = output[:-1] + "."
        return output

    def encounter(self, user):
        phs = "xx"
        enc = ""
        num = 4
        third = "4"
        forth = "4"
        fifth = "4"
        #
        # looks to see if player has visited square.
        # Research Numpy for possible better design.
        #
        text = textDAO("ytjwvcewrv")

        #########################################################
        # If encounter exists.
        #########################################################
        print("Position is...")
        print(self.char.POS)
        if self.char.POS in self.char.tracker: #If encounter exists in this square
            x = self.char.tracker.split(",")
            for i in x: # Looks for space
                if self.char.POS in i: # If finds space, slices into chunks.
                    enc = i.split("|")[1] # encounter
                    phs = i.split("|")[2] # Encounter phase
                    num = int(i.split("|")[3]) # number of things in encounter
                    moveTracker = i.split("|")[3]
                    # print(num)
                    break
            if num > 0:
                output = text.get_encounters(enc, num).split("|")[0]
                if self.char.state == "cmb" or self.char.state == "wlk":
                    output = text.get_special(enc, phs) + "|"
                if self.char.state == "itr": # 8^4|E|xx|4|4|4
                    output = text.get_interact(enc, phs).split("^")[0]

                #     output += " The enemy tries a " + phs
                #     moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
                #     for x in moves:
                #         if x not in moveTracker:
                #             output += "|{" + x + "}"

            else:
                output = text.get_encounters(enc, num).split("|")[0]

        #########################################################
        # If new encounter is made, setup here.
        #########################################################
        else:
            encSquare = text.get_Dungeon(self.char.POS).split(",")[4]
            randy = random.randint(0, len(encSquare) - 1)
            enc = encSquare[randy]
            if enc in "LZ" or "|L|" in self.char.tracker or "|Z|" in self.char.tracker: # Added so the loot and the Basilisk are non-repeatable.
                enc = "E"

            ######################################################### Testers
            if self.user.username == "fakeWalker" or self.user.username == "fakeSolve" and self.user.statusID == "000000000000":
                enc = "E"
            elif self.user.username == "fakeMelee" and self.user.statusID == "000000000000":
                enc = "B"
            elif self.user.username == "fakeInteract" and self.user.statusID == "000000000000":
                enc = "L"
            elif self.user.username == "fakeTalker" and self.user.statusID == "000000000000":
                enc = "T"
            elif self.user.username == "fakePuzzle" and self.user.statusID == "000000000000":
                enc = "P"
            elif self.user.username == "fakeRats" and self.user.statusID == "000000000000":
                enc = "R"
            ######################################################### Testers

            output = text.get_encounters(enc, num).split("|")  # All encounters set to max
            self.char.state = output[1]
            output = output[0]

            if self.char.state == "cmb": # Go here if state == combat
                if num != "0":
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
            elif self.char.state == "mel":
                moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
                phs = moves[0]  # slash by default until further notice.
                output += " They come at you with a " + phs  # Using phase to track what move enemy used.
                for i in moves:
                    output += "|{" + i + "}"
            elif self.char.state == "tlk":
                cutter = text.get_talk(enc, "start").split("|")
                output += cutter[0]
                phs = "start"
            elif self.char.state == "itr":
                if enc == "T":
                    cutter = text.get_traps(enc, 1).split("|")
                    output += cutter[0]
                    phs = cutter[1]
                elif enc == "L":
                    cutter = text.get_interact(enc, "start").split("|")
                    output += cutter[0]
                    phs = "start"
            elif self.char.state == "PZL":
                output += text.get_puzzle("x")
                third = "2"
                forth = "000"
                fifth = "x"
                phs = "fixed" # In the future, this will be used to determine the type of puzzle.


            #
            # Temp changed to make sure every passage has an encounter & all encounters set to max.
            #
            self.char.tracker += "," + self.char.POS + "|" + enc + "|" + phs + "|" + third + "|" + forth + "|" + fifth



        #
        # If 0 encounters in square, system acts like it's empty.
        #
        return output

############################### No Mans Land **********************************************