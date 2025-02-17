import random
import item

# WEAPONS
weapons = {
    "unarmed": {"damage": 2},
    "claws": {"damage": 3},
    "bite": {"damage": 4}
}

# BUFFS AND DEBUFFS
buffs_debuffs = {
    "health_regen_potion": [{"effect": "health_regeneration", "change": 1, "mult": False}],
    "stamina_regen_potion": [{"effect": "stamina_regeneration", "change": 1, "mult": False}],
    "injury": [{"effect": "accuracy", "change": 0.8, "mult": True}, {"effect": "dodge", "change": 0.8, "mult": True}],
    "strength": [{"effect": "strength", "change": 1.5, "mult": True}]
}

EXPERIENCE_MULT = 1.15

# BASE STATS
BASE_HEALTH_REGEN = 0.1
BASE_MAX_HEALTH = 10
BASE_MAX_STAMINA = 10
BASE_STAMINA_REGEN = 0.05
BASE_CRIT_DAMAGE = 2
BASE_CRIT_CHANCE = 0.01
BASE_ACCURACY = 0.5
BASE_MELEE_WEAPON_DAMAGE = 1
BASE_RANGED_WEAPON_DAMAGE = 1
BASE_PHYS_PROTECTION = 0
BASE_VISION_RADIUS = 2

# VITALITY STATS
MAX_HEALTH_PER_VITALITY = 2
MAX_STAMINA_PER_VITALITY = 0.75
HEALTH_REGEN_PER_VITALITY = 0.025
STAMINA_REGEN_PER_VITALITY = 0.01

# DEXTERITY STATS
DODGE_PER_DEXTERITY = 0.01
RANGED_DAMAGE_PER_DEXTERITY = 0.015

# PERCEPTION STATS
ACCURACY_PER_PERCEPTION = 0.01
CRIT_CHANCE_PER_PERCEPTION = 0.001
CRIT_DAMAGE_PER_PERCEPTION = 0.02

# STRENGTH STATS
MELEE_DAMAGE_PER_STRENGTH = 0.025


class Creature:
    def __init__(self, starting_coords, base_max_health=10, base_max_stamina=5, base_health_regen=0.05, base_stamina_regen=0.01,
                 strength=5, dexterity=5, vitality=5, intelligence=5, perception=5, wisdom=5):

        # ATTRIBUTES
        self.attributes = {
            "strength": strength,
            "vitality": vitality,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "perception": perception,
            "wisdom": wisdom
        }
        # STATS
        self.base_max_health = base_max_health
        self.base_max_stamina = base_max_stamina
        self.base_health_regen = base_health_regen
        self.base_stamina_regen = base_stamina_regen
        # BONUS STATS
        self.stats_bonus = {
            "max_health": 0,
            "max_stamina": 0,
            "health_regeneration": 0,
            "stamina_regeneration": 0,
            "dodge": 0,
            "melee_weapon_damage": 0,
            "ranged_weapon_damage": 0,
            "accuracy": 0,
            "crit_chance": 0,
            "crit_damage": 0,
            "phys_protection": 0,
            "vision_radius": 0,
            "strength": 0,
            "dexterity": 0,
            "vitality": 0,
            "perception": 0,
            "intelligence": 0
                            }
        # DEFENSIVE
        self.stats = {
            "max_health": self.base_max_health + self.attributes["vitality"]*MAX_HEALTH_PER_VITALITY,
            "max_stamina": self.base_max_stamina + self.attributes["vitality"]*MAX_STAMINA_PER_VITALITY,
            "health_regeneration": self.stats_bonus["health_regeneration"] + self.base_health_regen + self.attributes["vitality"]*HEALTH_REGEN_PER_VITALITY,
            "stamina_regeneration": self.stats_bonus["stamina_regeneration"] + self.base_stamina_regen + self.attributes["vitality"]*STAMINA_REGEN_PER_VITALITY,
            "dodge": self.attributes["dexterity"]*DODGE_PER_DEXTERITY,
            "melee_weapon_damage": BASE_MELEE_WEAPON_DAMAGE + self.attributes["strength"] * MELEE_DAMAGE_PER_STRENGTH,
            "ranged_weapon_damage": BASE_RANGED_WEAPON_DAMAGE + self.attributes["dexterity"] * RANGED_DAMAGE_PER_DEXTERITY,
            "accuracy": BASE_ACCURACY + self.attributes["perception"] * ACCURACY_PER_PERCEPTION,
            "crit_chance": BASE_CRIT_CHANCE + self.attributes["perception"] * CRIT_CHANCE_PER_PERCEPTION,
            "crit_damage": BASE_CRIT_DAMAGE + self.attributes["perception"] * CRIT_DAMAGE_PER_PERCEPTION,
            "phys_protection": self.stats_bonus["phys_protection"] + BASE_PHYS_PROTECTION,  # protection lessens damage by this value
            "frost_protection": 0,
            "fire_protection": 0,
            "acid_protection": 0,
            "shock_protection": 0,
            "vision_radius": self.stats_bonus["vision_radius"] + BASE_VISION_RADIUS
                      }
        self.health = self.stats["max_health"]
        self.stamina = self.stats["max_stamina"]
        self.attacked_recently = 0

        # BUFFS
        self.buffs = {}

        # EQUIPMENT
        self.equipment = {
            "main_hand": item.createWeapon("axe"),
            "off_hand": item.createWeapon("axe"),
            "head": item.createWeapon("axe"),
            "torso": item.createWeapon("axe"),
            "legs": item.createWeapon("axe"),
            "gloves": item.createWeapon("axe"),
            "feet": item.createWeapon("axe"),
            "back": item.createWeapon("axe")
        }

        # COORDINATES
        self.x = starting_coords[1]
        self.y = starting_coords[0]

        # ACTION BUFFER
        self.action_buffer = []

    # Movement functions
    def moveUp(self):
        self.y -= 1

    def moveDown(self):
        self.y += 1

    def moveRight(self):
        self.x += 1

    def moveLeft(self):
        self.x -= 1

    # This function recalculates the given stat automatically
    def recalculateStat(self, stat):
        if stat == "health_regeneration":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["vitality"]+self.stats_bonus["vitality"])*HEALTH_REGEN_PER_VITALITY + self.base_health_regen
        elif stat == "stamina_regeneration":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["vitality"]+self.stats_bonus["vitality"]) * STAMINA_REGEN_PER_VITALITY + self.base_stamina_regen
        elif stat == "dodge":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["dexterity"]+self.stats_bonus["dexterity"]) * DODGE_PER_DEXTERITY
        elif stat == "melee_weapon_damage":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["strength"]+self.stats_bonus["strength"]) * MELEE_DAMAGE_PER_STRENGTH + BASE_MELEE_WEAPON_DAMAGE
        elif stat == "ranged_weapon_damage":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["dexterity"]+self.stats_bonus["dexterity"]) * RANGED_DAMAGE_PER_DEXTERITY + BASE_RANGED_WEAPON_DAMAGE
        elif stat == "accuracy":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["perception"]+self.stats_bonus["perception"]) * ACCURACY_PER_PERCEPTION + BASE_ACCURACY
        elif stat == "crit_chance":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["perception"]+self.stats_bonus["perception"]) * CRIT_CHANCE_PER_PERCEPTION + BASE_CRIT_CHANCE
        elif stat == "crit_damage":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["perception"]+self.stats_bonus["perception"]) * CRIT_DAMAGE_PER_PERCEPTION + BASE_CRIT_DAMAGE
        elif stat == "max_health":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["vitality"]+self.stats_bonus["vitality"]) * MAX_HEALTH_PER_VITALITY + self.base_max_health
        elif stat == "max_stamina":
            self.stats[stat] = self.stats_bonus[stat] + (self.attributes["vitality"]+self.stats_bonus["vitality"]) * MAX_STAMINA_PER_VITALITY + self.base_max_stamina
        elif stat == "phys_protection":
            self.stats[stat] = self.stats_bonus[stat] + BASE_PHYS_PROTECTION
        elif stat == "strength":
            print(f'Strength: {self.attributes["strength"]+self.stats_bonus["strength"]}')
            self.recalculateStat("melee_weapon_damage")

    # This function changes the stats_bonus according to the buffs_debuffs dictionary
    # Should be called when tha buff is added or when it is removed
    def changeBuffStat(self, buffname, add=True):
        if add:
            for effect in buffs_debuffs[buffname]:
                if effect["effect"] not in self.attributes.keys():
                    if effect["mult"]:
                        # Here I subtract stats.bonus from stats before multiplying so that it only affects the base stat and bugs like
                        # (1. Multiply, 2. Add, 3. Divide, 4. Subtract and the stat value won't be the same as before)
                        # don't appear
                        self.stats_bonus[effect["effect"]] += (self.stats[effect["effect"]]-self.stats_bonus[effect["effect"]]) * (effect["change"]-1)
                    else:
                        self.stats_bonus[effect["effect"]] += effect["change"]
                else:
                    if effect["mult"]:
                        # Here I subtract stats.bonus from stats before multiplying so that it only affects the base stat and bugs like
                        # (1. Multiply, 2. Add, 3. Divide, 4. Subtract and the stat value won't be the same as before)
                        # don't appear
                        self.stats_bonus[effect["effect"]] += self.attributes[effect["effect"]] * (effect["change"]-1)
                    else:
                        self.stats_bonus[effect["effect"]] += effect["change"]
                self.recalculateStat(effect["effect"])
        else:
            for effect in buffs_debuffs[buffname]:
                if effect["effect"] not in self.attributes.keys():
                    if effect["mult"]:
                        # Here I subtract stats.bonus from stats before multiplying so that it only affects the base stat and bugs like
                        # (1. Multiply, 2. Add, 3. Divide, 4. Subtract and the stat value won't be the same as before)
                        # don't appear
                        self.stats_bonus[effect["effect"]] -= (self.stats[effect["effect"]] - self.stats_bonus[
                            effect["effect"]]) * (effect["change"] - 1)
                    else:
                        self.stats_bonus[effect["effect"]] -= effect["change"]
                else:
                    if effect["mult"]:
                        # Here I subtract stats.bonus from stats before multiplying so that it only affects the base stat and bugs like
                        # (1. Multiply, 2. Add, 3. Divide, 4. Subtract and the stat value won't be the same as before)
                        # don't appear
                        self.stats_bonus[effect["effect"]] -= self.attributes[effect["effect"]] * (effect["change"] - 1)
                    else:
                        self.stats_bonus[effect["effect"]] -= effect["change"]
                self.recalculateStat(effect["effect"])

    # This function adds a buff to the buffs
    def addBuff(self, buffname, time):
        if buffname not in self.buffs.keys():
            self.buffs.update({buffname: {"time": time}})
            self.changeBuffStat(buffname)
        else:
            self.buffs.update({buffname: {"time": time}})

    def removeBuff(self, buffname):
        del self.buffs[buffname]
        self.changeBuffStat(buffname, add=False)

    def dealDamage(self, dmg):
        damage_done = {}
        for type in dmg.keys():
            print(type, max(0, dmg[type] - self.stats[f"{type}_protection"]))
            damage_done.update({type: max(0, dmg[type] - self.stats[f"{type}_protection"])})
            self.health -= max(0, dmg[type] - self.stats[f"{type}_protection"])
        self.attacked_recently = 10
        return damage_done

    def dealFatigue(self, dmg):
        self.stamina -= dmg

    def addAction(self, action):
        self.action_buffer.append(action)

    def removeAction(self):
        self.action_buffer.pop(0)

    # Function for adding permanent attributes
    def addAttribute(self, att_name, amount):
        self.attributes[att_name] += amount
        if att_name == "strength":
            self.recalculateStat("melee_weapon_damage")
        elif att_name == "dexterity":
            self.recalculateStat("dodge")
            self.recalculateStat("ranged_weapon_damage")
        elif att_name == "perception":
            self.recalculateStat("accuracy")
            self.recalculateStat("crit_chance")
            self.recalculateStat("crit_damage")
        elif att_name == "vitality":
            self.recalculateStat("max_health")
            self.recalculateStat("max_stamina")
            self.recalculateStat("health_regeneration")
            self.recalculateStat("stamina_regeneration")

        elif att_name == "intelligence":
            pass

    def attack(self, enemy):
        total_damage = {}
        roll = random.randint(1, 100)
        print(f"Roll: {roll}. Self accuracy: {self.stats['accuracy']*self.equipment['main_hand'].accuracy}, enemy dodge: {enemy.stats['dodge']}.")
        #print(f"Roll threshold: {(self.stats['accuracy']*self.equipment['main_hand'].accuracy-enemy.stats['dodge'])*100}")

        if roll <= (self.stats["accuracy"]*self.equipment["main_hand"].accuracy-enemy.stats["dodge"])*100:  # if hit
            print("hit")
            dmg = {}
            for effect in self.equipment["main_hand"].on_hit_effects:
                effect_roll = random.randint(1, 100)
                print(f"{effect} chance: {item.enchantments[effect]['chance']*100}, roll: {effect_roll}")
                if effect_roll <= item.enchantments[effect]["chance"]*100:
                    print(f"Inflicted {item.enchantments[effect]['debuff']}")
                    enemy.addBuff(item.enchantments[effect]['debuff'], 5)

            for type in self.equipment["main_hand"].damage.keys():
                dmg.update({type: self.equipment["main_hand"].damage[type] * self.stats["melee_weapon_damage"]})

            if random.randint(1, 1000) <= self.stats["crit_chance"]*1000:
                print("crit!")
                for type in dmg.keys():
                    dmg[type] *= self.stats["crit_damage"]

            return enemy.dealDamage(dmg)
        else:
            #print("miss")
            return "Miss"

    def update(self):

        # health regeneration
        if self.attacked_recently > 0:
            self.attacked_recently -= 1
        elif self.health < self.stats["max_health"]:
            self.health += self.stats["health_regeneration"]
        else:
            self.health = self.stats["max_health"]

        # stamina regeneration
        if self.stamina < self.stats["max_stamina"]:
            self.stamina += self.stats["stamina_regeneration"]
            if self.stamina > self.stats["max_stamina"]:
                self.stamina = self.stats["max_stamina"]
        else:
            self.stamina = self.stats["max_stamina"]

        # bonus stats annulment
        # This function updates the state of the character and should be called once per turn
        expired_buffs = []

        # buffs update for turns
        for key in self.buffs.keys():
            self.buffs[key]["time"] -= 1
            if self.buffs[key]["time"] <= 0:
                expired_buffs.append(key)
        for buff in expired_buffs:
            self.removeBuff(buff)

class Player(Creature):
    def __init__(self, starting_coords, base_max_health=15, base_max_stamina=10, base_health_regen=0.1, base_stamina_regen=0.05,
                 strength=10, dexterity=10, vitality=10, intelligence=10, perception=10,
                 experience=0, level=1):
        super().__init__(starting_coords, base_max_health=base_max_health, base_max_stamina=base_max_stamina,
                         base_health_regen=base_health_regen, base_stamina_regen=base_stamina_regen,
                         strength=strength, dexterity=dexterity, vitality=vitality, intelligence=intelligence,
                         perception=perception)

        # PLAYER ONLY STATS
        self.experience = experience
        self.level = level
        self.experience_for_level_up = 100+100*level
        self.attribute_points = 0
        self.inventory_size = 40

        # INVENTORY
        axe = item.Weapon("nordic_axe", "legendary")
        axe.addEnchantment("Frost")
        #axe.addEnchantment("Fire")
        #axe.addEnchantment("Injuring")
        #axe.addEnchantment("Acid")
        self.inventory = [item.Weapon("hatchet", "common"),
                          item.Weapon("hatchet", "uncommon"),
                          item.Weapon("hatchet", "epic"),
                          item.Weapon("hatchet", "legendary"),
                          item.Weapon("hatchet", "rare"),
                          item.Weapon("hatchet", "rare"),
                          axe,
                          item.Weapon("hand_axe", "rare"),
                          item.Weapon("war_axe", "legendary")]  # It will have limited space, 40 slots?

    def addExperience(self, exp):
        self.experience += exp
        if self.experience >= self.experience_for_level_up:
            while self.experience > self.experience_for_level_up:
                self.experience -= self.experience_for_level_up
                self.experience_for_level_up *= EXPERIENCE_MULT
                self.level_up()

    def level_up(self):  # unfinished obviously
        self.attribute_points += 3
        self.level += 1
