class Skill(object):
    def __init__(self):
        self.name = ""
        self.description = ""

    @staticmethod
    def factory(type):
        if type == "Strengh":
            return Strengh()
        if type == "Dexterity":
            return Dexterity()
        if type == "Armor":
            return Armor()
        if type == "Warrior":
            return Warrior()
        else:
            print ('SKILL INCONNU')

class Strengh(Skill):
    def __init__(self):
        super(Strengh, self).__init__()
        self.name = "Nailer"
        self.description = "You get a better aiming, inflicting terrible wounds to monsters. 1 more dammage with any weapon"

class Dexterity(Skill):
    def __init__(self):
        super(Dexterity, self).__init__()
        self.name = "Thief"
        self.description = "You are good at avoid things. Your moves are efficient and unpredictable, confusing your ennemies. It's harder to hit you and gives you 10% more chance to avoid attacks"

class Armor(Skill):
    def __init__(self):
        super(Armor, self).__init__()
        self.name = "Hard skin"
        self.description = "Your skin is hard as a troll one, only fool monsters would try to defy you. 1 less dammage per attack"

class Warrior(Skill):
    def __init__(self):
        super(Warrior, self).__init__()
        self.name = "Warrior"
        self.description = "You made hundred of battles and you know how to stay alive. You are an expert with health kits, giving you extra bonus"

"""
lucker roll*2
runner
faster than light
good sight
more drops
reloader
"""
