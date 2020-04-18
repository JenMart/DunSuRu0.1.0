from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO

class parsers:

    def __init__(self):
        self.CharDAO = CharDAO
        self.textDAO = textDAO

    def parser(self, text, input):
        output = ""
        print(text[0])
        for i in text: # Note: Text is assumed to be pre-split up before being sent to parser.
            textParsed = re.search('{(.*)}', i)  # Searched for any word (options) surrounded by curly brackets.
            if textParsed is None:
                return False # I don't think it's actually possible to get here.
            else:
                action = textParsed.group(0)[1:-1].lower()  # Removes curly brackets.
                # Looks for instances of options in input- allows user to write full sentences.
                if action in input: # If action is found in input,
                    output = action
                    break
                else:
                    output = False
                    #
                    # If action not found in output, returns false.
                    # NOTE: It's up to the other method to deal with that. SO DON'T FORGET.
                    #
        return output