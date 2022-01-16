from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO
from app.models.parsers import parsers

class talkManager:

    def __init__(self):
        charDAO = CharDAO
        self.textDAO = textDAO

    def converse(self, input, char):
        #
        # Under construction.
        #
        output = "This is not a valid choice. "
        text = textDAO("nfeqwhgwtwg")
        x = char.tracker.split(",")
        counter = ""
        for i in x:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter (name of thing you're talking to)
        phs = counter.split("|")[2]  # Encounter phase (Where in conversation)
        freindly = counter.split("|")[3]  # friendliness meter. (add feature later)
        conversation = text.get_talk(enc, phs).split("|")
        parse = parsers()
        choice = parse.parser(conversation[0], input)

        if choice != False:
            out = text.get_talk(enc, choice)
            output = out.split("|")[0]
            update_cell = char.POS + "|" + enc + "|" + choice + "|" + "5" + "|" + "5" + "|" + "5"
            char.tracker = char.tracker.replace(counter, update_cell)
            char.state = out.split("|")[1]
        # for i in conversation:
        #     convParsed = re.search('{(.*)}', i)
        #     if convParsed is None:
        #         None
        #     else:
        #         response = convParsed.group(0)[1:-1].lower()
        #         if response in input:
        #             out = text.get_talk(enc, response)
        #             if not out:
        #                 # Note: If you're here, someone fucked up.
        #                 output = "Your response is invalid."
        #             else:
        #                 output = out.split("|")[-1]
        #                 updateCell = char.POS + "|" + enc + "|" + response + "|" + "5" + "|" + "5" + "|" + "5"
        #                 char.tracker = char.tracker.replace(counter, updateCell)
        #                 char.state = out[-3:]
        #             break
        #         else:
        #             output = "This is not a valid option"
        if char.state == "wlk":
            output += "You are now alone. " + self.lookAround()
        return output