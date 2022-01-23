from app.controllers.database_manager import DatabaseManager
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
                output = "This is not a valid choice. "

        elif enc == "L" or enc == "0": # Loot (i.e. treasure)
            path = text.get_interact(enc, phs)
            choice = parse.parser(path, input)
            if choice != False:
                out = text.get_interact(enc, choice)
                output = out.split("|")[0]
                updateCell = char.POS + "|" + enc + "|" + choice + "|" + "5" + "|" + "5" + "|" + "5"
                char.tracker = char.tracker.replace(counter, updateCell)
                char.state = out.split("|")[1]
                if choice == "inside":
                    if enc == "0":
                        char.WINCON = "Permitted."
                        print("All is well.")
                        if "parchment piece" not in char.items:
                            char.items.update({"parchment piece": '1'})
                        else:
                            char.items.update({"parchment piece": str(int(char.items["parchment piece"]) + 1)})
                    elif enc == "L":
                        coin = random.randint(5,10)
                        char.gold = coin
            else:
                output = "This is not a valid choice. "

        return output
