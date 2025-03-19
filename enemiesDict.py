import random
from player import Player
class Enemy:
    def __init__(self, name, health, damage, gold, xp, weight):
        self.name = name
        self.health = health
        self.damage = damage
        self.gold = gold
        self.xp = xp
        self.weight = weight
    
    def isAlive(self):
        return self.health > 0

    def attack(self, player):
        return random.randint(3 * self.damage // 4, 5 * self.damage // 4) - player.stats["defense"]

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    @staticmethod
    def createEnemy(location):
        if location == "cave":
            enemies = [
                Enemy("Goblin", 30, 10, 40, 5, 70),
                Enemy("Skeleton", 20, 15, 15, 30, 40),
                Enemy("Orge", 50, 22, 30, 110, 15),
                Enemy("Dragon", 100, 30, 200, 200, 4)
            ]
        elif location == "catacombs":
            enemies = [
                Enemy("Skeleton", 30, 20, 22, 45, 60),
                Enemy("King Crab", 50, 28, 38, 73, 20),
                Enemy("Vampire", 35, 22, 35, 55, 30),
                Enemy("Mimic", 20, 10, 500, 5, 2)
            ]
        elif location == "treasure":
            enemies = [
                Enemy("Golden Dragon", 90, 30, 200, 200, 100)
            ]
        else:
            raise ValueError("Invalid location")

        # Extract weights from the list of Enemy objects
        weights = [enemy.weight for enemy in enemies]

        # Randomly select an enemy based on their weight
        selectedEnemy = random.choices(enemies, weights=weights, k=1)[0]
        return selectedEnemy