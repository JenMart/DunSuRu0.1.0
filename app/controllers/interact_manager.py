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
        charDAO = CharDAO
        self.textDAO = textDAO
        self.parser = parsers
        self.db_mgmt = DatabaseManager()

    def interact(self, input, char):
        #
        # Under construction.
        #
        x = char.tracker.split(",")
        text = textDAO("76hj34fejlk")
        parse = parsers()
        for i in x:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]
        phs = counter.split("|")[2]
        num = counter.split("|")[3]
        forth = counter.split("|")[4]
        fifth = counter.split("|")[5]



        if enc == "T": # Traps
            ablities = text.get_traps("1", None)

            choice = parse.parser(ablities, input)
            if choice != False:
                if phs in choice:
                    output = "You deftly avoid the swinging blades."
                    char.tracker = char.tracker.replace(enc + str(num), enc + str(0))
                    char.state = "wlk"
                else:
                    output = "You fail to dodge the trap."
                    char.tracker = char.tracker.replace(enc + str(num), enc + str(0))
                    char.state = "wlk"
            else:
                output = "This is not a valid choice."

        elif enc == "L" or enc == "0": # Loot (i.e. treasure)
            path = text.get_interact(enc, phs).split("|")
            choice = parse.parser(path, phs)
            if choice != False:
                out = text.get_interact(enc, choice)
                output = out.split("^")[0]
                updateCell = self.char.POS + "|" + enc + "|" + choice + "|" + "0" + "|" + "0"
                self.char.tracker = self.char.tracker.replace(counter, updateCell)
                self.char.state = out.split("^")[1]
                if enc == 0 and choice == "inside":
                    self.db_mgmt.for_this_moment_all_is_well(self.char.name)
            else:
                output = "This is not a valid choice."

        return output
