from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO

class newCharacter:

    def __init__(self):
        self.CharDAO = CharDAO
        self.textDAO = textDAO
    def newCharacter(self,userName):
        #
        # Full character creator will be added in later.
        #
        # look = self.lookAround()
        output = userName + " has been created."
        return output