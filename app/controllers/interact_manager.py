from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO
from app.models.parsers import parsers

class interactManager:

    def __init__(self):
        self.charDAO = CharDAO
        self.textDAO = textDAO
        self.parser = parsers
        self.db_mgmt = DatabaseManager()

    def interact(self, input, char):
        #
        # Under construction.
        #
        # x = char.tracker.split(",")
        text = textDAO("76hj34fejlk")
        parse = parsers()
        # for i in x:
        #     if char.POS in i:
        #         counter = i
        #         break
        # enc = counter.split("|")[1]
        # phs = counter.split("|")[2]
        # num = counter.split("|")[3]
        # forth = counter.split("|")[4]
        # fifth = counter.split("|")[5]



        if char.encounter == "T": # Traps
            ablities = text.get_traps("1", None)

            choice = parse.parser(ablities, input)
            if choice:
                if char.phase in choice:
                    output = "You deftly avoid the swinging blades."
                    # char.tracker = char.tracker.replace(enc + str(num), enc + str(0))
                    char.encounter = "0"
                    char.state = "wlk"
                else:
                    output = "You fail to dodge the trap."
                    # char.tracker = char.tracker.replace(enc + str(num), enc + str(0))
                    char.encounter = "0"
                    char.state = "wlk"
            else:
                output = "This is not a valid choice."

        elif char.encounter == "L" or char.encounter == "0": # Loot (i.e. treasure)
            path = text.get_interact(char.encounter, char.phase)
            choice = parse.parser(path, input)
            if choice:
                out = text.get_interact(char.encounter, choice)
                output = out.split("^")[0]
                # updateCell = char.POS + "|" + char.encounter + "|" + choice + "|" + "5" + "|" + "5" + "|" + "5"
                # char.tracker = char.tracker.replace(counter, updateCell)
                char.phase = choice
                char.state = out.split("^")[1]
                if char.encounter == "0" and choice == "inside":
                    char.WINCON = "Permitted."
                    print("All is well.")
                    # self.db_mgmt.for_this_moment_all_is_well(char.name)
            else:
                output = "This is not a valid choice."

        return output
