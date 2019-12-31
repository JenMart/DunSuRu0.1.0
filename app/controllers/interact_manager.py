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

    def interact(self, input, char):
        #
        # Under construction.
        #
        x = char.tracker.split(",")
        text = textDAO("76hj34fejlk")
        for i in x:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]
        phs = counter.split("|")[2]
        num = counter.split("|")[3]
        forth = counter.split("|")[4]
        # fifth = counter.split("|")[5]
        parse = parsers()


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

        elif enc == "L": # Loot (i.e. treasure)
            secTracker = int(strftime("%S", gmtime()))
            path = text.get_interact(enc, phs)[:-4].lower()
            choice = parse.parser(path, input)
            if choice != False:
                for x in path.split("|"):
                    if "attempt" in x and "{"+choice+"}" in x:
                        # "Attempt" means failure is not perm
                        if (secTracker % 3) == 0:
                            choice = choice+"SUCCESS"
                            break
                        else:
                            choice = choice + "FAIL"
                            break
                    elif "try" in x and "{"+choice+"}" in x:
                        # try means failure is perm.
                        if (secTracker % 3) == 0:
                            choice = choice+"SUCCESS"
                        else:
                            choice = choice + "FAIL"
                            num = 0
                            break
                    break
                out = text.get_interact(enc, choice)
                char.state = out[-3:]
                if char.state == "wlk" and num != 0:
                    num = 1
                output = out[:-4]
                updateCell = char.POS + "|" + enc + "|" + choice + "|" + num + "|" + forth
                char.tracker = char.tracker.replace(counter, updateCell)

            else:
                output = "This is not a valid choice."

        return output
