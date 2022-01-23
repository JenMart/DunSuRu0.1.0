from app.controllers.database_manager import DatabaseManager, check_user, add_user, check_character
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
from app.models.textGetter import textDAO
from app.models.UserData import UserData
from app.controllers.combat_manager import combatManager
from app.controllers.new_character import newCharacter
from app.controllers.interact_manager import interactManager
from app.controllers.talk_manager import TalkManager
from app.controllers.item_manager import itemManager
from app.controllers.puzzle_manager import puzzleManager
from app.controllers.whisper import Whispers
from app.models.parsers import parsers
import random
import time
import re
from time import gmtime, strftime


def username_checker(userName, created_time, tweetID):

    user_exists, user_time = check_user(userName)
    if not user_exists:  # If user not found, create new in DB.
        add_user(userName, created_time, tweetID)
    return


def character_checker(userName):
    checkChar = check_character(userName)

    return

# class ChoiceManager:
#     def __init__(self):
#         self.db_mgmt22222 = DatabaseManager()
#         self.twt_print = printTwt()
#         self.CharDAO = CharDAO
#         self.textDAO = textDAO
#         self.userData = UserData
#         self.combatManager = combatManager
#         self.newCharacter = newCharacter
#         self.interact = interactManager
#         self.talk = TalkManager
#         self.items = itemManager
#         self.puzzles = puzzleManager
#         self.parser = parsers
#         self.whisper = Whispers
