class CharDAO:
    def __init__(self, name, job, health, gold, items, state, region, regionType, POS, tracker, WINCON):
        # self.charID = charID
        # self.user = user
        self.name = name
        self.job = job
        self.health = health
        self.gold = gold
        self.state = state
        self.region = region
        self.regionType = regionType
        self.POS = POS
        self.tracker = tracker
        self.WINCON = WINCON
        for i in tracker.split(","):
            if POS in i:
                self.POS_Tracker = i
                self.encounter = i.split("|")[1]
                self.phase = i.split("|")[2]
                self.phaseNum = i.split("|")[3]
                self.undefined_one = i.split("|")[4]
                self.undefined_two = i.split("|")[5]
                break
        self.items = {}
        for i in items.split(","):
            self.items.update({i.split("|")[0] : i.split("|")[1]})






