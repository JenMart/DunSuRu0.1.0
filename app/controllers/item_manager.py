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
            output += " {} gold.".format(str(char.gold))
        elif "use" in input:
            for i in char.items:
                i = i.split("|")[0]
                # print(i)
                if i in input:
                    if char.state == "cmb": # This is all terribly written but temporary. Probably.
                        text = textDAO("ntergo;ybw")
                        tracker = char.tracker.split(",")
                        counter = ""
                        for x in tracker:
                            if char.POS in x:
                                counter = x
                                break
                        enc = counter.split("|")[1]  # encounter
                        phase = counter.split("|")[2]  # Encounter phase
                        num = int(counter.split("|")[3])  # number of things in encounter
                        if "lit candle" in input:
                            output = "You do not blow out the candle. Not yet."
                            break
                        elif "parchment piece" in input:
                            output = "You are unable to make out the words in this light."
                            break
                        elif "candle stub" in input:
                            output = "You do not risk the candle stub. Even though it is spent it is not without worth."
                            break
                        elif enc == "R":
                            if "alch fire" in i:
                                damage = random.randint(2, 4)
                                num -= damage
                                char.items.update({i : str(int(char.items[i]))})
                                if num > 0:
                                    updateCell = char.POS + "|" + enc + "|" + "BP" + "|" + str(num)
                                    char.tracker = char.tracker.replace(counter, updateCell)
                                    updateEncount = text.get_encounters(enc, num).split("|")
                                    output = "You toss a flask of alchemist fire at the swarm and deals {} damage".format(damage)
                                    output += updateEncount[0] + text.get_special(
                                        enc, phase)
                                    char.state = updateEncount[1]
                                    break
                                else:
                                    updateCell = char.POS + "|" + enc + "|" + "EP" + "|" + str(0)
                                    char.tracker = char.tracker.replace(counter, updateCell)
                                    updateEncount = text.get_encounters(enc, "x").split("|")
                                    output = "Liquid flames wipes away the swarm of rodents. The passage is now empty."
                                    char.state = updateEncount[1]
                                    break
                            else:
                                updateEncount = text.get_encounters(enc, num).split("|")
                                output = "You toss a {} but it does nothing.".format(i)
                                output += updateEncount[0] + text.get_special(
                                    enc, phase)
                                break
                        if enc == "M":
                            if "holy water" in i:
                                char.items.update({i: str(int(char.items[i]))})
                                updateCell = char.POS + "|" + enc + "|" + "EP" + "|" + str(0)
                                char.tracker = char.tracker.replace(counter, updateCell)
                                updateEncount = text.get_encounters(enc, "x").split("|")
                                output = "The holy water shows a brief glimmer of who once was before fading. You are alone."
                                char.state = updateEncount[1]
                                break
                            else:
                                updateEncount = text.get_encounters(enc, num).split("|")
                                output = "You toss a {} but it does nothing.".format(i)
                                output += updateEncount[0] + text.get_special(
                                    enc, phase)
                                break
                    else:
                        if "lit candle" in input:   # Secrets.
                            if char.POS == "8^4":
                                char.state = "itr"
                                char.tracker = char.tracker.replace("8^4|E|xx|4|4|4","8^4|0|start|5|5|5")
                                output = " You blow out the candle. In the shining darkness, you see a chest." \
                                         "| {Open} the lid.| Examine the {sides}.| Example the {lock}."
                                char.items.update({i: int(char.items[i]) - 1})
                                char.items.update({"candle stub" : 1})
                                break
                            else:
                                output = "You do not blow out the candle. Not yet."
                                break
                        elif "parchment piece" in input:
                            output = " You are unable to make out the words in this light."
                            break
                        else:
                            output = "You use {}. Nothing happens.".format(i)
                            char.items.update({i: int(char.items[i]) - 1})
                            break
                else:
                    output = "You do not possess this item."
        else:
            output = "You have selected an invalid option."

        for i in char.items: # If item is at zero, system removes it.
            if int(char.items[i]) <= 0:
                char.items.pop(i)
                break
        return output