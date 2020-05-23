from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO

class itemManager:

    def __init__(self):
        self.CharDAO = CharDAO
        self.textDAO = textDAO

    def useItem(self, input, char):
        # itemsCut = char.items.lower().split(",")
        output = ""
        if "show" in input:
            output = "You hold in your possession:"
            for i in char.items:
                output += " {} {},".format(char.items[i], i.capitalize())
            output = output[:-1]
        elif "use" in input:
            for i in char.items:
                print(i)
                if i in input:
                    if char.state == "cmb": # Holy Water|1,Alch Fire|3,Egg|5,lit candle|1
                        if char.encounter == "R":
                            if "alch fire" in input:
                                char.phaseNum -= random.randint(2, 4)
                                char.items.update({i: str(int(char.items[i]) - 1)})
                    else:
                        if "candle" in input:   # Secrets.
                            if char.POS == "8^4":
                                char.state = "itr"
                                # char.tracker = char.tracker.replace("8^4|E|xx|4|4|4","8^4|0|start|5|5|5")
                                char.encounter = "0"
                                char.phase = "start"
                                output = " You blow out the candle. In the shining darkness, you see a chest." \
                                         "| {Open} the lid.| Examine the {sides}.| Examine the {lock}."
                                char.items.update({i: str(int(char.items[i]) - 1)})
                                break
                            else:
                                output = "You do not blow out the candle. Not yet."
                                break
                        else:
                            output = "You use {}. Nothing happens.".format(i.capitalize())
                            char.items.update({i: str(int(char.items[i])-1)})
                            break
                else:
                    output = "You do not possess this item."
        else:
            output = "You have selected an invalid option."


        return output