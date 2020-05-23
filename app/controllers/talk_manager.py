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
        self.CharDAO = CharDAO
        self.textDAO = textDAO

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
        freindly = counter.split("|")[3]  # friendliness meter. (add feature later)
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
                        output = out.split("|")[-1]
                        updateCell = self.char.POS + "|" + enc + "|" + response + "|" + "5" + "|" + "5" + "|" + "5"
                        self.char.tracker = self.char.tracker.replace(counter, updateCell)
                        self.char.state = out[-3:]
                    break
                else:
                    output = "This is not a valid option"
        if self.char.state == "wlk":
            output += "You are now alone. " + self.lookAround()
        return output