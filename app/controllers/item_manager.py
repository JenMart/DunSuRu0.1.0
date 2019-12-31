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
        itemsCut = char.items.lower().split(",")
        output = ""
        if "show" in input:
            output = "You hold in your possession: "
            for i in itemsCut:
                output += i.replace("|"," x") + ", "
            output = output[:-1]
        elif "use" in input:
            for i in itemsCut:
                i = i.split("|")[0]
                print(i)
                if i in input:
                    output = "You use " + i
                    break
                else:
                    output = "You do not possess this item."
        else:
            output = "You have selected an invalid option."
        return output