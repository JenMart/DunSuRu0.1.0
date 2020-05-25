from app.controllers.db_mgmt import DatabaseManager
from app.controllers.twt_print import printTwt
from app.models.charDAO import CharDAO
import random
import re
from time import gmtime, strftime
from app.models.textGetter import textDAO
from app.models.parsers import parsers

class combatManager:

    def __init__(self):
        charDAO = CharDAO
        self.textDAO = textDAO
        self.parser = parsers


    def meleeCombat(self, input, char):
        text = textDAO("lkjge9423r")
        tracker = char.tracker.split(",")
        for i in tracker:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter
        phase = counter.split("|")[2]  # Encounter phase
        enemyHealth = int(counter.split("|")[3])  # number of things in encounter
        playerHealth = int(counter.split("|")[4])
        moveTracker = counter.split("|")[5]
        #
        # Moves array is inefficient. Find better solution later.
        #
        moves = ["slash", "lunge", "push", "pierce", "riposte", "parry", "feint"]
        #
        # This part finds the time by seconds.
        # Changes what the enemy counters with based on if # is divis by 3.
        #
        secTracker = int(strftime("%S", gmtime()))
        inputSplit = input.split(" ")
        moveCounter = text.get_melee(phase)
        for i in inputSplit:
            # If incorrect
            if phase == "win": # If you win the fight.
                if "spare" in input:
                    output = "You have spared the enemies life."
                    enemyHealth = 0
                    break
                elif "slay" in input:
                    output = "You have slain the enemy."
                    enemyHealth = 0
                    break
                else:
                    output = "The world unfocuses for a moment."
                    enemyHealth = 0
            elif phase == "lose": # If you lose the fight,
                if "surrender" in input:
                    output = "You successfully barter for your life."
                    playerHealth = 0
                    break
                elif "last ditch" in input: # Gives a tiny chance of turning a lose into a win.
                    if (secTracker % 4) == 0:  # gives players 1/4 chance of success
                        output = "Your attack surprises the enemy."
                        enemyHealth = 0
                    else:
                        output = "Your last ditch effort failed."
                        playerHealth = 0
                    break
                else:
                    output = "The world inverses but soon returns to normal."
            else: # If the phase is normal.
                if i not in moveCounter and i in moves or i in moveTracker or i == "fail":
                    if secTracker < len(moves) and phase != moves[secTracker]:
                        phase = moves[secTracker]
                    else:
                        rand = random.randint(1, len(moves)) - 1
                        if phase != moves[rand]:
                            phase = moves[rand]
                        else:
                            phase = text.get_melee(i).split("|")[0]
                    playerHealth -= 1
                    output = "You failed to counter. P: " + str(playerHealth) + " E: " + str(enemyHealth)
                    break
                # If correct
                elif i in moveCounter and i != "|":
                    if (secTracker % 3) == 0:
                        phase = text.get_melee(i).split("|")[0]
                    else:
                        phase = text.get_melee(i).split("|")[1]
                    enemyHealth -= 1
                    output = "You countered the attack. P: " + str(playerHealth) + " E: " + str(enemyHealth)
                    moveTracker += i
                else:
                    output = "That is not a valid option."
        if enemyHealth > 1 and playerHealth > 1:  # If battle is normal
            updateCell = char.POS + "|" + enc + "|" + phase + "|" + str(enemyHealth) + "|" + str(
                playerHealth) + "|" + moveTracker
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            char.state = updateEncounter[1]
            output += updateEncounter[0] + " The enemy tries a " + phase
            for x in moves:
                if x not in moveTracker:
                    output += "|{" + x + "}"
        elif enemyHealth == 1 and playerHealth > 0:  # If enemy is brought to 1 HP
            updateCell = char.POS + "|" + enc + "|" + "win" + "|" + str(enemyHealth) + "|" + str(
                playerHealth) + "|" + moveTracker
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            char.state = updateEncounter[1]
            output = updateEncounter[0] + "|{Spare}|{Slay}"
        elif playerHealth == 1 and enemyHealth > 0:  # If player is brought to 1 HP
            updateCell = char.POS + "|" + enc + "|" + "lose" + "|" + str(enemyHealth) + "|" + str(
                playerHealth) + "|" + moveTracker
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, enemyHealth).split("|")
            char.state = updateEncounter[1]
            output = updateEncounter[0] + " You are at the mercy of its sword|{Last Ditch}|{Surrender}"
        elif enemyHealth <= 0:  # If enemy is defeated
            updateCell = char.POS + "|" + enc + "|" + "EP" + "|" + str(0) + "|" + str(playerHealth) + "|" + moveTracker
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, "x").split("|")
            char.state = updateEncounter[1]
            output += updateEncounter[0] + " The passage is now empty."
        else:  # If player is defeated. NOTE: Will default to player wining ATM.
            updateCell = char.POS + "|" + enc + "|" + "EP" + "|" + str(0) + "|" + str(playerHealth) + "|" + moveTracker
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncounter = text.get_encounters(enc, "x").split("|")
            char.state = updateEncounter[1]
            output += " Your failure goes unrecorded." + " The passage is now empty."
            char.health -= 1
        # print(updateCell)
        return output

    
    def groupCombat(self, input, char):
        text = textDAO("ntergo;ybw")
        damage = 0
        tracker = char.tracker.split(",")
        counter = ""
        for i in tracker:
            if char.POS in i:
                counter = i
                break
        enc = counter.split("|")[1]  # encounter
        phase = counter.split("|")[2]  # Encounter phase
        num = int(counter.split("|")[3])  # number of things in encounter

        #
        # Keeping this around for now in case the new setup breaks.
        #
        # ##################### Code sectioned off for future effeciency purposes.
        # abilities = text.get_special(enc, phase).split("|")
        # for i in abilities:
        #     ablitiesParsed = re.search('{(.*)}', i)  # Searched for any word (options) surrounded by curly brackets.
        #     if ablitiesParsed is None:
        #         None
        #     else:
        #         action = ablitiesParsed.group(0)[1:-1].lower()  # Removes curly brackets.
        #         # Looks for instances of options in input- allows user to write full sentences.
        #         if action in input:
        #             damage = text.get_damage(action,"bandit").split("|")
        #             num -= int(damage[1])
        #             break
        #         else:
        #             damage = ["that is not a valid option you do $$ damage.",0]
        # #####################

        ##################### New setup,
        parse = parsers()
        abilities = text.get_special(enc, phase)
        textCheck = parse.parser(abilities, input)

        #####################

        if textCheck:
            if textCheck == "attack":
                damage = text.get_damage(textCheck, "bandit").split("|")
                num -= int(damage[1])
            else:
                damage = ["that is not a valid option you do $$ damage.", 0]

        #####################
        if num > 0:
            updateCell = char.POS + "|" + enc + "|" + "BP" + "|" + str(num )
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncount = text.get_encounters(enc, num).split("|")
            output = damage[0].replace("$$",str(damage[1])) +  updateEncount[0] + text.get_special(enc, phase)
            char.state = updateEncount[1]
        else:
            updateCell = char.POS + "|" + enc + "|" + "EP" + "|" + str(0)
            char.tracker = char.tracker.replace(counter, updateCell)
            updateEncount = text.get_encounters(enc, "x").split("|")
            output = updateEncount[0] + " The passage is now empty."
            char.state = updateEncount[1]
        return output
