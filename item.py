import random

# TYPE IDS
ids = {"axe": ["hatchet", "hand_axe", "war_axe", "nordic_axe"]}

# RARITIES
rarities = ["common", "uncommon", "rare", "epic", "legendary"]

# PRESETS
presets = {
    "hatchet": {"name": "Hatchet", "damage": 6, "accuracy": 1, "strength": 6, "type": "axe", "hands": "one_handed", "level": 1},
    "hand_axe": {"name": "Hand Axe", "damage": 9, "accuracy": 1.05, "strength": 8, "type": "axe", "hands": "one_handed", "level": 2},
    "war_axe": {"name": "War Axe", "damage": 13, "accuracy": 1.1, "strength": 11, "type": "axe", "hands": "one_handed", "level": 3},
    "nordic_axe": {"name": "Nordic Axe", "damage": 17, "accuracy": 1.2, "strength": 15, "type": "axe", "hands": "one_handed", "level": 4}
}

# ENCHANTMENTS
enchantments = {
    "Frost": {"effect": "change_damage", "damage_type": "frost", "damage_mult": 0.25},
    "Fire": {"effect": "change_damage", "damage_type": "fire", "damage_mult": 0.25},
    "Acid": {"effect": "change_damage", "damage_type": "acid", "damage_mult": 0.25},
    "Injuring": {"effect": "chance_debuff", "chance": 0.1, "debuff": "injury"}
}

class Weapon:
    def __init__(self, preset_name, rarity):
        self.name = preset_name
        self.title = presets[preset_name]["name"]
        self.damage = {"phys": presets[preset_name]["damage"]}
        self.accuracy = presets[preset_name]["accuracy"]
        self.strength = presets[preset_name]["strength"]
        self.type = "weapon"
        self.weapon_type = presets[preset_name]["type"]
        self.hands = presets[preset_name]["hands"]
        self.level = presets[preset_name]["level"]
        self.rarity = rarity
        self.enchantments = []
        self.on_hit_effects = []

    def addEnchantment(self, ench_name):
        print(len(self.enchantments), rarities.index(self.rarity))
        if len(self.enchantments) < rarities.index(self.rarity):
            self.enchantments.append(ench_name)
            phys_mult = 1
            if enchantments[ench_name]["effect"] == "change_damage":
                for ench in self.enchantments:
                    if enchantments[ench]["effect"] == "change_damage":
                        phys_mult -= enchantments[ench]["damage_mult"]
                self.damage.update({"phys": presets[self.name]["damage"]*phys_mult})
                for ench in self.enchantments:
                    if enchantments[ench]["effect"] == "change_damage":
                        self.damage.update({enchantments[ench]["damage_type"]: presets[self.name]["damage"] * (enchantments[ench]["damage_mult"])})
            elif enchantments[ench_name]["effect"] == "chance_debuff":
                self.on_hit_effects.append(ench_name)
            return True  # this means that the enchantments has been successfully added
        else:
            return False

    def changeRarity(self, rarity):
        self.rarity = rarity


def createWeapon(type):
    type1 = random.choice(ids[type])
    rarity = random.choice(rarities)
    return Weapon(type1, rarity)