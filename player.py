import random
class Player:
    classes = {
    "soldier": {
        "description": "A strong, defensive fighter that excels in combat.",
        "stats": {
            "vitality": 40,
            "strength": 4,
            "defense": 6,
            "luck": 1,
            "agility": 2
        }
    },
    "thief": {
        "description": "An assassin that is swift, damaging, and lucky.",
        "stats": {
            "vitality": 20,
            "strength": 4,
            "defense": 2,
            "luck": 5,
            "agility": 8
        }
    },
    "wizard": {
        "description": "Heavy-hitting mage that is slow but uses luck to help in battle.",
        "stats": {
            "vitality": 10,
            "strength": 12,
            "defense": 1,
            "luck": 4,
            "agility": 5
        }
    }
}


    def __init__(self):
        self.level = 1
        self.xp = 0
        self.levelUp = 30
        self.className = self.chooseClass()
        self.stats = self.setStats()
        self.health = 70 + self.stats["vitality"]
        self.maxHealth = 70 + self.stats["vitality"]
        self.gold = 50
        self.potions = 0
        self.weapon = None
        

    def isAlive(self):
        return self.health > 0

    def attack(self):
        if self.weapon == None:
            damage = random.randint(self.stats["luck"], 3 * self.stats["luck"]) + self.stats["strength"] 
        else:
            damage = random.randint(self.stats["luck"], 3 * self.stats["luck"]) + self.stats["strength"] + self.weapon["damage"]
        return damage

    def takeDamage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def equipWeapon(self, weapon):
        self.weapon = weapon
        print(f"You have equipped the {weapon['name']}")

    def heal(self):
        if self.potions > 0:
            self.health += 30
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            self.potions -= 1
            print("You drank a health potion and restored 30 health!")
        else:
            print("You have no health potions!")

    def checkLvUp(self):
        numOfLevels = 0
        while self.xp >= self.levelUp:
            print("")
            print("*LEVEL UP*")
            print("")
            numOfLevels += 1
            self.level += 1
            self.xp -= self.levelUp
            self.levelUp = int(self.levelUp * 1.2) 
            print(f"You are now level {self.level}")
        for _ in range(numOfLevels):
            self.updateStats()

    def gainXp(self, amount):
        self.xp += amount
        self.checkLvUp()

    def checkStats(self):
        print("\n--- Player Stats ---")
        print(f"Health: {self.health} / {self.maxHealth}")
        print(f"Gold: {self.gold}")
        print(f"Level: {self.level}")
        print(f"XP: {self.xp}/{self.levelUp}")
        print("Attributes:")
        for stat, value in self.stats.items():
            print(f"- {stat.capitalize()}: {value}")
        print("---------------------")

        
    def updateStats(self):
        flag = True
        while flag:
            print("")
            print("Which stat would you like to improve?")
            print("")
            print("1. Strength")
            print("2. defense")
            print("3. Luck")
            print("4. Agility")
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.stats["strength"] += 1
                flag = False
            elif choice == "2":
                self.stats["defense"] += 1
                flag = False
            elif choice == "3":
                self.stats["luck"] += 1
                flag = False
            elif choice == "4":
                self.stats["agility"] += 1
                flag = False
            else:
                print("Invalid choice. Try again.")
        
        # Apply a small health buff based on luck and vitality
        healthBuff = random.randint(self.stats["luck"], self.stats["vitality"] // 8)
        self.health += healthBuff
        self.maxHealth += healthBuff
        print(f"Your health has increased by {healthBuff}!")
        
        # Display updated stats
        print("\nYour stats have been improved:")
        print(f"Strength: {self.stats['strength']}")
        print(f"defense: {self.stats['defense']}")
        print(f"Luck: {self.stats['luck']}")
        print(f"Agility: {self.stats['agility']}")
        print(f"Health: {self.health}")

    def chooseClass(self):
        print("Choose your class: ")
        print("")
        for name, info in self.classes.items():
            print(f"{name.capitalize()}: {info['description']}")
        
        while True:
            print("")
            choice = input("Enter your choice (soldier, thief, or wizard): ").strip().lower()
            if choice in self.classes:
                return choice
            else:
                print("Invalid choice. Try again.")

    def setStats(self):
        return self.classes[self.className]["stats"]
    
    def __str__(self):
        return f"Level: {self.level}, XP: {self.xp} / {self.levelUp}, Health: {self.health}, Gold: {self.gold}, Potions: {self.potions}"