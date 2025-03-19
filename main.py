import random
from player import Player
from enemiesDict import Enemy
import weaponsDict
def nl():
    print("")

weapons = {
    "dagger": {"name": "Dagger", "damage": 3, "cost": 70},
    "sword": {"name": "Sword", "damage": 8, "cost": 150},
    "hammer": {"name": "Hammer", "damage": 12, "cost": 200},
}

def getLocationOptions(player, location):
    choices = []
    if location == "forest":
        choices.extend([
            {"name": "Go to Cave", "action": lambda: combat(player, "cave")},
            {"name": "Go to River", "action": lambda: river(player)},
            {"name": "Go to Tavern", "action": lambda: tavern(player)},
        ])
    elif location == "cave":
        choices.extend([
            {"name": "Stay in Cave", "action": lambda: combat(player, "cave")},
            {"name": "Leave Cave", "action": lambda: forest(player)}
        ])
    elif location == "catacombs":
        choices.extend([
            {"name": "Stay in Catacombs", "action": lambda: combat(player, "catacombs")},
            {"name": "Leave Catacombs", "action": lambda: scottCity(player)}
        ])
    elif location == "scott city":
        choices.extend([
            {"name": "Go to Catacombs", "action": lambda: combat(player, "catacombs")},
            {"name": "Go to Shop", "action": lambda: shop(player)},
            {"name": "Go to Treasure Room", "action": lambda: treasureRoom(player)},
            {"name": "Return to Forest", "action": lambda: forest(player)}
        ])
    elif location == "tavern":
        choices.extend([
            {"name": "Buy Health Potion", "action": lambda: buyPotion(player)},
            {"name": "Leave Tavern", "action": lambda: forest(player)}
        ])
    elif location == "shop":
        choices.extend([
            {"name": "Buy Weapon", "action": lambda: shop(player)},
            {"name": "Leave Shop", "action": lambda: forest(player)}
        ])
    elif location == "river":
        if player.level >= 5:
            choices.append({"name": "Cross River", "action": lambda: scottCity(player)})
        else:
            choices.append({"name": "Try to Cross River", "action": lambda: river(player)})

    choices.append({"name": "Heal", "action": lambda: player.heal()})
    choices.append({"name": "Check Stats", "action": lambda: player.checkStats()})

    return choices

def giveLocationOptions(player, location):
    choices = getLocationOptions(player, location)
    while True:
        print(f"You are in {location.capitalize()}. You can: ")
        nl()
        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice['name']}")
        nl()
        choice = input("What do you want to do? ").strip()
        choice = int(choice)
        if 1 <= choice <= len(choices):
            choices[choice-1]['action']()
        else:
            print("Invalid Choice. Try Again.")

#-------------------------------------------------------------------------------------

def forest(player):
    nl()
    giveLocationOptions(player, "forest")


# ------------------------------------------------------------------------------------

# There are enemies in the cave where the player can get experience and gold.
def combat(player, location):
    # Battle Phase
    print("You enter a dark cave and something attacks you!")
    enemy = Enemy.createEnemy(location)
    enemy.health = random.randint(3 * enemy.health // 4, 5 * enemy.health // 4)
    print(f"A {enemy.name} with {enemy.health} health appears!")
    while enemy.isAlive() and player.isAlive():
        nl()
        print(f"Your health: {player.health}")
        print(f"Monster health: {enemy.health}")
        nl()
        action = input("Do you want to ATTACK (1) or RUN (2)? ")
        if action == "1":
            damage = player.attack()
            enemy.takeDamage(damage)
            print(f"You dealt {damage} damage to the {enemy.name}!")
            if enemy.health > 0:
                damage = enemy.attack(player)
                player.takeDamage(damage)
                print(f"The monster hit you for {damage} damage!")
        elif action == "2" and location == "cave":
            print("You ran back to the forest!")
            forest(player)
            return
        elif action == "2" and location == "catacombs":
            print("You run back to Scott City")
            scottCity(player)
            return
        else:
            print("Invalid choice. Try again.")
    if player.isAlive():
        nl()
        print(f"You defeated the {enemy.name}!")
        enemyXP = random.randint(3 * enemy.xp // 4, 5 * enemy.xp // 4)
        enemyGold = random.randint(3 * enemy.gold // 4, 5 * enemy.gold // 4)
        print(f"You gain {enemyXP} experience and {enemyGold} gold.")
        player.gainXp(enemyXP)
        player.gold += enemyGold
    else:
        print("You have died. Thank you for playing.")
        exit()

        #Choice Phase
    giveLocationOptions(player, location)

# ------------------------------------------------------------------------------------

def tavern(player):
    print("You enter a cozy tavern. A health potion costs 30 gold.")
    print(f"You have {player.gold} gold.")
    nl()
    while True:
        choice = giveLocationOptions(player, "tavern")
        
def buyPotion(player):
    if player.gold >= 30:
        player.gold -= 30
        player.potions += 1
        nl()
        print("You bought a health potion!")
        nl()
    else:
        nl()
        print("You don't have enough gold!")
        nl()

# ------------------------------------------------------------------------------------

def shop(player):
    allWeapons = list(weapons.items())
    print("Welcome to the Scott City shop! Would you like to buy any weapons?")
    print(f"You have {player.gold} gold.")
    nl()
    while True:
        print("Weapons for sale: ")
        nl()
        for i, (name, weapon) in enumerate(allWeapons, start=1):
            print(f"{i}. {weapon['name']}. Costs {weapon['cost']} gold.")
        nl()
        choice = input(f"What would you like to buy (1-{len(allWeapons)}) or leave to leave. ").strip().lower()
        if choice == "leave":
            print("You leave the shop.")
            scottCity(player)
        else:
            choice = int(choice)
            if 1 <= choice <= len(allWeapons):
                (name, weapon) = allWeapons[choice-1]
                if player.gold >= weapon['cost']:
                    player.gold -= weapon['cost']
                    player.equipWeapon(weapon)
                    print(f"You have bought the {weapon['name']}")
                else:
                    print("You do not have enough gold.")
            else:
                print("Invalid choice. Try again.")





def river(player):
    if player.level >= 5:
        print("You cross the river and arrive at Scott City!")
        scottCity(player)
    else:
        print("The river is too dangerous to cross. You need to be at least level 5.")
        forest(player)


# ------------------------------------------------------------------------------------



def scottCity(player):
    while True:
        choice = giveLocationOptions(player, "scott city")

# ------------------------------------------------------------------------------------

def treasureRoom(player):
    if player.level >= 8:
        print("You are allowed in the treasure room")
        nl()
        print("...")
        print("While you were looting the treasure, a giant dragon attacks you!")
        combat(player, "treasure")
        nl()
        print("CONGRATS! YOU BEAT THE GAME! Thank you for playing.")
        exit()
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------


def main():
    print("Welcome to the Text Adventure Game!")
    # Creates a character
    player = Player()
    print("\nYour character has been created!")
    print(f"Class: {player.className.capitalize()}")
    print("")
    forest(player)
if __name__ == "__main__":
    main()