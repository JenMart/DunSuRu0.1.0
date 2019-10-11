import random
import sqlite3

class char_creator:
    #
    # Currently the same as from DunSuRu 2.0. Will improve later.
    #

        def new_game(self, userName):
            #
            # 456 name combinations. THOSE ARE ROOKIE NUMBERS.
            #
            firstHalf = "Ger Sym Hugh Ger Bysh Riff Vin Heg Gile Gau Ewl Gyl Van Syn Gath Par" \
                        "Rar Helm Thu Coel Erf Cane Fol Knet Leth Dene Hav Tun Thun Ara Bur".split()  # 24
            seconHalf = "y ey te nah ney ley alt ort man der dar dor da ess ke fin son kin wyn nia bre ia mir".split()  # 18
            nickName = ""
            nickName1 = "Silent Horse Iron Grim Shadow Warrior Cold Queen King Prince Princess" \
                        " Mumble Quick  Flame".split()  # 14
            nickName2 = "Tongue Preserver Mouth Phantom Wonder Guardian Watcher Fist " \
                        "Slayer Hammer Sword Arrow".split()  # 12
            nickName3 = "Big Small Flamming Last First Great Final Burning Smug".split()

            #
            # Flips coin, determines if name will have one or two syllables
            #
            if (random.randint(0, 1) == 0):
                firstName = random.choice(firstHalf) + random.choice(seconHalf)
            else:
                firstName = random.choice(firstHalf)

            if (random.randint(0, 1) == 0):  # Flips coin, determins if name will have one or two syllables
                secondName = random.choice(firstHalf) + random.choice(seconHalf)
            else:
                secondName = random.choice(firstHalf)
            while (firstName == secondName):  # If first and last name are both the same, remakes last name.
                if (random.randint(0, 1) == 0):
                    secondName = random.choice(firstHalf) + random.choice(seconHalf)
                else:
                    firstName = random.choice(firstHalf)

            #
            # Same as before but for nicknames.
            #
            if (random.randint(0, 1) == 0):

                if (random.randint(0, 1) == 0):
                    nickName += nickName1[random.randint(0, 13)] + " " + nickName2[random.randint(0, 11)]
                else:
                    nickName += nickName2[random.randint(0, 11)] + " " + nickName1[random.randint(0, 13)]
            else:  # Big Small Flamming Last First Great Final Burning
                if (random.randint(0, 1) == 0):
                    nickName = nickName1[random.randint(0, 13)]
                else:
                    nickName = nickName2[random.randint(0, 11)]
                if (random.randint(0,
                                   1) == 0):  # If Nickname appears as only one word then there is another flip to add another word
                    nickName = nickName3[random.randint(0, 6)] + " " + nickName

            fullName = firstName + " " + secondName

            # chkName = self.checkName(fullName)

        #
        # This doesn't work? Screw it, I'll figure out later.
        #
        def checkName(self, name):  # FINISH THIS!
            conn = sqlite3.connect('DunSuciRun.sqlite')
            c = conn.cursor()
            numerals = ['II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII',
                        'XVIII', 'XIX', 'XX']
            checkName = name
            c.execute('SELECT NAME FROM CHARACTERS WHERE NAME = ?', [checkName])

            chk = c.fetchall()
            count = 0
            secondCount = 0

            while count < len(chk):
                if chk[count] in name:
                    name = name + " The " + numerals[secondCount]
                    secondCount += 1
                    if secondCount > 18:
                        self.new_game()
                else:
                    count += 1
            return name

            conn.commit()
            conn.close()