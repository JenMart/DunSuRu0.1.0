from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO
from app.models.parsers import parsers

class helpManager:

    def __init__(self):
        charDAO = CharDAO
        self.textDAO = textDAO
        self.parser = parsers
        self.db_mgmt = DatabaseManager()

    def help(self, input, char):
        x = char.tracker.split(",")
        text = textDAO("76hj34fejlk")
        message = ""
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

        if "where" in input:
            if char.state == "cmb":
                output = "you are in group combat."
            elif char.state == "wlk":
                None
            elif char.state == "mel":
                None
            elif char.state == "itr":
                None
            elif char.state == "pzl":
                None
            elif char.state == "tlk":
                None
        elif "combat" in input:
            None
        elif "talk" in input:
            None
        elif "melee" in input:
            None
        elif "puzzle" in input:
            None
        elif "walk" in input:
            None
        elif "interact" in input:
            None


        return output
