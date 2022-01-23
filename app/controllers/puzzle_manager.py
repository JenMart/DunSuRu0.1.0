from app.controllers.database_manager import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO
from app.models.parsers import parsers

class puzzleManager:

    def __init__(self):
        self.CharDAO = CharDAO
        self.textDAO = textDAO

    def puzzles(self, input, char):
        #
        # Note: "x" gonna give it to you, so find another solution in the future.
        #
        text = textDAO("76hj34fejlk")
        x = char.tracker.split(",")
        parse = parsers()
        for i in x:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]
        phs = counter.split("|")[2]
        third = counter.split("|")[3]
        forth = counter.split("|")[4]
        fifth = counter.split("|")[5]
        shift = ["V", "X", "I"]
        # if phs == "first":
        #     third = "2"
        #     forth = "000"
        #     fifth = "x"
        #     phs = "fixed"

        puzzlePieces = {
            "top": int(forth[0]),
            "middle": int(forth[1]),
            "bottom": int(forth[2])
        }
        top = int(forth[0])
        middle = int(forth[1])
        bottom = int(forth[2])
        ablities = text.get_puzzle("x").split("|")
        puzzleChoiceOne = parse.parser(ablities[0], input) # Top/middle/bottom
        puzzleChoiceTwo = parse.parser(ablities[1], input) # Right/left







        if puzzleChoiceOne != False and puzzleChoiceTwo != False:
            if "right" in puzzleChoiceTwo.lower():  # here?
                if puzzlePieces[puzzleChoiceOne] + 1 <= 2:
                    puzzlePieces[puzzleChoiceOne] += 1
                    output = "You have moved the " + puzzleChoiceOne + " to the " + puzzleChoiceTwo
                else:
                    output = "You cannot turn the puzzle this direction"
            elif "left" in puzzleChoiceTwo.lower():
                if puzzlePieces[puzzleChoiceOne] - 1 >= 0:
                    puzzlePieces[puzzleChoiceOne] -= 1
                    output = "You have moved the " + puzzleChoiceOne + " to the " + puzzleChoiceTwo
                else:
                    output = "You cannot turn the puzzle this direction"

            forth = str(puzzlePieces["top"]) + str(puzzlePieces["middle"]) + str(puzzlePieces["bottom"])
            # print("what puzzle looks like")
            # print(forth)
            if forth != "111":
                third = 4
                updateEncounter = text.get_encounters(enc, third).split("|")
                output += ". You see..." +". Top: " + str(shift[puzzlePieces[list(puzzlePieces)[0]]]) + ", Middle: " \
                          + str(shift[puzzlePieces[list(puzzlePieces)[1]]]) + ", Bottom " + shift[puzzlePieces[list(puzzlePieces)[2]]]  + "." + updateEncounter[0]
                output += text.get_puzzle("x")
                # You have moved the bottom to the right. Top: X Middle: V Bottom: I
                char.state = updateEncounter[1]
            else:
                updateEncounter = text.get_encounters(enc, "x").split("|")
                output += updateEncounter[0] + " The passage is now empty."
                third = 0
                char.state = updateEncounter[1]

        else:
            output = "You have not selected a valid option."
    
        updateCell = char.POS + "|" + enc + "|" + phs + "|" + str(third) + "|" + forth + "|" + fifth
        char.tracker = char.tracker.replace(counter, updateCell)

        return output
