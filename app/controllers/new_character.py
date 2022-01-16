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
        firstHalf = "Ger Sym Hugh Ger Bysh Riff Vin Heg Gile Gau Ewl Gyl Van Syn Gath Par" \
                  "Rar Helm Thu Coel Erf Cane Fol Knet Leth Dene Hav Tun Thun Ara Bur Arn Bid Ao Bo Co " \
                    "Fo Go Ko Po Qo Zo Sun Ro Tor Ru Hal Sten Sven Bjo Knu Od Age".split() #24

        seconHalf = "y ey te nah ney ley alt ort man der dar dor da ess ke fin son kin wyn nia bre ia mir".split() #18

        nickName1 = "Silent Horse Iron Grim Shadow Warrior Cold Queen King Prince Princess" \
                    " Mumble Quick  Flame".split() #14

        nickName2 = "Tongue Preserver Mouth Phantom Wonder Guardian Watcher Fist " \
                    "Slayer Hammer Sword Arrow".split() #12

        nickName3 = "Big Small Flamming Last First Great Final Burning Smug".split()

        nickName = ""
        output = userName + " has been created. "
        return output