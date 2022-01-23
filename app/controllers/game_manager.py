from app.controllers.database_manager import DatabaseManager
from app.controllers.twt_print import printTwt
from app.controllers.choice_manager import ChoiceManager, username_checker

from app.models.charDAO import CharDAO
from app.models.textGetter import textDAO
from app.models.UserData import UserData

from app.controllers.combat_manager import combatManager
from app.controllers.new_character import newCharacter
from app.controllers.interact_manager import interactManager
from app.controllers.talk_manager import TalkManager
from app.controllers.item_manager import itemManager
from app.controllers.puzzle_manager import puzzleManager
from app.controllers.whisper import Whispers

from app.models.parsers import parsers

import random
import time




class GameManager:
    def __init__(self):
        self.db_mgmt = DatabaseManager()
        self.twt_print = printTwt()
        self.choice = ChoiceManager()
        self.CharDAO = CharDAO
        self.textDAO = textDAO
        self.userData = UserData
        self.combatManager = combatManager
        self.newCharacter = newCharacter
        self.interact = interactManager
        self.talk = TalkManager
        self.items = itemManager
        self.puzzles = puzzleManager
        self.parser = parsers
        self.whisper = Whispers

    def handle_choice(self, input, userName, created_time, tweetID):
        xx = self.db_mgmt.setup()
        #
        # checks to see if user info already exists. If it does not, adds to DB.
        #
        self.user = UserData(userName, created_time, input, tweetID)
        current_time = time.time()
        output = "This is not a valid option"
        input = input.lower()

        username_checker(userName, created_time, tweetID)

        ###############################################################################################################
        #
        # Figure out how to store function calls in a dict without it calling them all!
        #
        ###############################################################################################################
        character_exists = self.db_mgmt.check_character(userName)
        if not character_exists:
            if "new" in input or "start" in input:
                new_char = newCharacter()
                add_character(userName, userName)
                character_info = self.db_mgmt.pull_character(userName)
                self.character = CharDAO(character_info[0], character_info[1], int(character_info[2]), character_info[3], character_info[4],
                                         character_info[5],
                                         character_info[6],
                                         character_info[7], character_info[8], character_info[9], character_info[10])
                output = new_char.newCharacter(userName)
                output += self.look_around()
                return output
            else:
                output = "You do not possess a character. Type {Start} or {New} to begin playing."
        elif current_time <= int(self.user.created_time) + 60:
            # try:
            character_info = self.db_mgmt.pull_character(userName)
            self.character = CharDAO(character_info[0], character_info[1], character_info[2], character_info[3], character_info[4], character_info[5],
                                     character_info[6],
                                     character_info[7], character_info[8], character_info[9], character_info[10])

        ###############################################################################################################

            output = "This is not a valid option."
            # elif "summon the basilisk of carrows way." in input:
            #     converse = talkManager()
            #     output = converse.converse(input)
            if self.character.health < 0:
                output = self.get_up(input)
            elif "items" in input or "item" in input:
                item_manager = itemManager()
                output = item_manager.useItem(input, self.character)
            elif "look" in input:
                output = self.look_around()
                output += self.encounter(userName)
            elif self.character.state == "wlk":
                output = self.move_character(input)
                if self.character.POS != "p":
                    output += self.look_around()
                    output += self.encounter(userName)
            elif self.character.state == "cmb":
                combat_manager = combatManager()
                output = combat_manager.groupCombat(input, self.character)
                # output += self.lookAround()
                # output += self.encounter()
            elif self.character.state == "mel":  # Two sep combat types. May combine later.
                combat_manager = combatManager()
                output = combat_manager.meleeCombat(input, self.character)
                # output += self.lookAround()
                # output += self.encounter()
            elif self.character.state == "itr":
                interact = interactManager()
                output = interact.interact(input, self.character)
                # output += self.lookAround()
                # output += self.encounter()
            elif self.character.state == "tlk":
                talk_manager = TalkManager()
                output = talk_manager.converse(input, self.character)
            elif self.character.state == "PZL":
                puz = puzzleManager()
                output = puz.puzzles(input, self.character)
                # output += self.lookAround()
                # output += self.encounter()
            elif self.character.state == "out":
                output = self.the_outside(input)
            elif self.character.state == "end":
                self.character.state = "stop"
                update_user(userName, tweetID, created_time, self.character)
                # self.the_end(input)
                text = textDAO("pojihudew")
                output = text.parchment_pieces(int(self.character.items["parchment piece"]))
                whisper = Whispers()
                whisper.the_note(userName, output, tweetID)
            elif self.character.state == "stop":
                output = "Your journey has faced The End."

            if self.character.health < 0:  # This is intentional.
                output = self.character.name + " has fallen. Their legacy will be remembered as people remember the clouds that bring rain. Do you wish to try again? {Yes} {No}."

        time.sleep(60)
        # current_time = time.time()
        ###############################################################################################################
        if int(self.user.created_time) + 60 < current_time:
            print("user time")
            print(self.user.created_time)
            print("current time")
            print(current_time)
            update_user(userName, tweetID, created_time, self.character)
            return output
        else:
            print("over time")
            time_out(userName, tweetID, created_time)
            return "OVER_TIME_ERROR"

    def move_character(self, input):
        imp = input
        #
        # For sake of sanity, all dungeons start at 1:1 until stated otherwise.
        #
        dungeon = textDAO("pojihudew")
        dun = dungeon.get_Dungeon(self.character.POS).split("|")[0]
        nor = dun.split("/")[0]
        sou = dun.split("/")[1]
        eas = dun.split("/")[2]
        wes = dun.split("/")[3]
        if "north" in imp and nor != "x":
            output = "You go north. "
            self.character.POS = nor
        elif "south" in imp and sou != "x":
            output = "You go south. "
            self.character.POS = sou
        elif "east" in imp and eas != "x":
            output = "You go east. "
            self.character.POS = eas
        elif "west" in imp and wes != "x":
            output = "You go west. "
            self.character.POS = wes
        else:
            output = "This is not a valid choice. "
        #
        # If player attempts to leave, system currently places them back at starting square.
        #
        if self.character.POS == "p":
            if self.character.WINCON == "Permitted.":
                output = "You step in the sun. For the moment there is respite. Do you brave the depths of Carrows Way again?| {Yes} {No}."
                self.character.state = "out"
            else:
                self.character.POS = "1^1"
                output = "You cannot leave. Not until you've found what you are looking for."
        return output

    def look_around(self):
        output = " You see"
        text = textDAO("pojihudew")
        dungeon = text.get_Dungeon(self.character.POS)
        nor = dungeon.split("/")[0]
        sou = dungeon.split("/")[1]
        eas = dungeon.split("/")[2]
        wes = dungeon.split("/")[3]
        des = dungeon.split("|")[2]

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
        # print("Position is...")
        # print(self.char.POS)
        if self.character.POS in self.character.tracker:  # If encounter exists in this square
            x = self.character.tracker.split(",")
            for i in x:  # Looks for space
                if self.character.POS in i:  # If finds space, slices into chunks.
                    enc = i.split("|")[1]  # encounter
                    phs = i.split("|")[2]  # Encounter phase
                    num = int(i.split("|")[3])  # number of things in encounter
                    moveTracker = i.split("|")[3]
                    # print(num)
                    break
            if num > 0:
                output = text.get_encounters(enc, num).split("/\\")[0]
                if self.character.state == "cmb" or self.character.state == "wlk":
                    output = text.get_special(enc, phs) + "|"
                if self.character.state == "itr":  # 8^4|E|xx|4|4|4
                    output = text.get_interact(enc, phs).split("|")[0]

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
            encSquare = text.get_Dungeon(self.character.POS).split("|")[1]
            randy = random.randint(0, len(encSquare) - 1)
            enc = encSquare[randy]
            if enc in "LZ" or "|L|" in self.character.tracker or "|Z|" in self.character.tracker:  # Added so the loot and the Basilisk are non-repeatable.
                enc = "E"

            ######################################################### Testers
            if self.user.username == "fakeWalker" or self.user.username == "fakeSolve" and self.user.statusID == "000000000000":
                enc = "E"
            elif self.user.username == "fakeMelee" and self.user.statusID == "000000000000":
                enc = "B"
            elif self.user.username == "fakeInteract" and self.user.statusID == "000000000000":
                enc = "L"
            elif self.user.username == "fakeTalker" and self.user.statusID == "000000000000":
                enc = "Z"
            elif self.user.username == "fakePuzzle" and self.user.statusID == "000000000000":
                enc = "P"
            elif self.user.username == "fakeRats" and self.user.statusID == "000000000000":
                enc = "R"
            ######################################################### Testers

            output = text.get_encounters(enc, num).split("|")  # All encounters set to max
            self.character.state = output[1]
            output = output[0]

            if self.character.state == "cmb":  # Go here if state == combat
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
                    self.character.state = "wlk"
            elif self.character.state == "mel":
                moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
                phs = moves[0]  # slash by default until further notice.
                output += " They come at you with a " + phs  # Using phase to track what move enemy used.
                for i in moves:
                    output += "|{" + i + "}"
            elif self.character.state == "tlk":
                cutter = text.get_talk(enc, "start").split("|")
                output += cutter[0]
                phs = "start"
            elif self.character.state == "itr":
                if enc == "T":
                    cutter = text.get_traps(enc, 1).split("|")
                    output += cutter[0]
                    phs = cutter[1]
                elif enc == "L":
                    cutter = text.get_interact(enc, "start").split("|")
                    output += cutter[0]
                    phs = "start"
            elif self.character.state == "PZL":
                output += text.get_puzzle("x")
                third = "2"
                forth = "000"
                fifth = "x"
                phs = "fixed"  # In the future, this will be used to determine the type of puzzle.

            #
            # Temp changed to make sure every passage has an encounter & all encounters set to max.
            #
            self.character.tracker += "," + self.character.POS + "|" + enc + "|" + phs + "|" + third + "|" + forth + "|" + fifth

        #
        # If 0 encounters in square, system acts like it's empty.
        #
        return output

    def get_up(self, input):
        if " yes " in input:
            output = "That is the right answer."
            self.character.WINCON = "false"
            self.character.state = "wlk"
            self.character.POS = "1^1"
            self.character.tracker = "1^1|E|NP|0|0|0"
            self.character.items.update({"lit candle": "1"})
        elif " no " in input:
            output = "Until you are ready."
        else:
            output = "Until you are ready."

        return output

    def the_outside(self, input):

        if "yes" in input.split(" "):
            if int(self.character.items["parchment piece"]) < 3:
                output = "Your candle is lit once more. Go forth."
                self.character.WINCON = "false"
                self.character.state = "wlk"
                self.character.POS = "1^1"
                self.character.items.update({"lit candle": "1"})
                self.character.tracker = "1^1|E|NP|0|0|0"
            else:
                output = "Your candle has fought hard. Now it is time to step {forward}."
        elif "no" in input.split(" "):
            # output = "Until you are ready."
            self.character.state = "tlk"
            text = textDAO("456ghy54yglllf")
            enc = "S"
            cutter = text.get_talk(enc, "start").split("|")
            output = cutter[0]
            phs = "start"
            self.character.tracker += "," + self.character.POS + "|" + enc + "|" + phs + "|4|4|4"
        else:
            output = "Do you brave the depths of Carrows Way again?| {Yes} {No}"

        return output

    def the_end(self, input):

        text = textDAO("pojihudew")
        output = text.parchment_pieces(int(self.character.items["parchment piece"]))
        whisper = Whispers
        whisper.the_note()

############################### No Mans Land **********************************************
