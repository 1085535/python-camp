def show_stats(player):
    print(f"\nHealth: {player['health']}\nStamina: {player['stamina']}\nInventory: {player['inventory']}")


def check_game_over(player):
    if player["health"] <= 0 or player["stamina"] <= 0:
        print("\nGame Over. Valiant Effort.")
        return True
    return False


def main():
    valid_weapons = ["Katana", "Bow", "Sword", "Dagger"]
    weapon = input("Choose a weapon out of the following: Katana, Bow, Sword, Dagger: ").strip()
    while weapon not in valid_weapons:
        weapon = input("Please choose a valid weapon (Katana, Bow, Sword, Dagger): ").strip()

    player = {
        "weapons": valid_weapons,
        "health": 100,
        "stamina": 50,
        "inventory": [weapon],
        "location": ["Forest", "Cave", "Castle", "Village"]
    }

    print("\nYou are in a dark forest.")
    print("You can see a path leading to a cave and a path leading to a village.")
    print("You can also see a castle in the distance.")
    show_stats(player)

    cave_input = input("\nDo you want to enter the cave? (yes/no): ").strip().lower()

    if cave_input == "no":
        print("\nYou decide not to enter the cave. Your journey is over.")
        print("You can try again. Come back next time!")
        return

    print("\nYou enter the cave and find a treasure chest. You open it and find a Map.")
    print("However, you don't get the map easily. You must fight the guardian of the cave, a giant spider.")

    spider_fight = input("Do you want to fight the spider? (yes/no): ").strip().lower()

    if spider_fight == "yes":
        print(f"You fight the spider with your {weapon} and defeat it. You take the map and add it to your inventory.")
        player["inventory"].append("Map")
        player["health"] -= 25
        player["stamina"] -= 10
    else:
        print("You decide not to fight the spider. You continue through the cave, mapless.")

    show_stats(player)
    if check_game_over(player):
        return

    print("\nAs you make your way through the cave, you come across a fork in the path.")
    fork_input = input("Do you want to go left or right? (left/right): ").strip().lower()

    if fork_input == "left":
        print("You go left and find a hidden passage leading to a secret room.")
        print("You find a treasure chest with a health potion inside. You add it to your inventory.")
        player["inventory"].append("Health Potion")
        player["health"] += 50
        player["stamina"] += 20
    elif fork_input == "right":
        print(f"You run into an onslaught of bats. You fight them off with your {weapon}.")
        print("You defeat them but take damage, and your weapon is blunted, becoming less effective.")
        print("You will lose more stamina in future fights with this weapon.")
        player["health"] -= 20
        player["stamina"] -= 30
    else:
        print("You hesitate too long and the path closes off. You stumble forward, losing time and stamina.")
        player["stamina"] -= 10

    # keep stats within sensible bounds
    player["health"] = max(0, min(100, player["health"]))
    player["stamina"] = max(0, min(100, player["stamina"]))

    print(f"\nYou have made it through the cave! Your health is now {player['health']}, your stamina is now {player['stamina']}.")
    if check_game_over(player):
        return

    forest_input = input("\nDo you want to continue? (yes/no): ").strip().lower()
    if forest_input == "no":
        print("Thanks for playing!")
        return

    print("\nGreat, you have made it to the forest. It is a land of rewards and treachery.")
    show_stats(player)
    health_input = input("Do you want to rest, or keep going? (rest/keep going): ").strip().lower()

    if health_input == "rest":
        print("You rest but are attacked in your sleep. You lose lots of health and stamina.")
        player["health"] -= 30
        player["stamina"] -= 10
    else:
        print("You walk for what feels like ages. You lose stamina.")
        player["stamina"] -= 30

    player["health"] = max(0, min(100, player["health"]))
    player["stamina"] = max(0, min(100, player["stamina"]))

    print(f"\nYour health is now {player['health']}, your stamina is now {player['stamina']}.")
    if check_game_over(player):
        return

    print("\nThe castle rises ahead of you, its gates guarded and its walls high.")
    print("This is the last obstacle standing between you and the safety of the village beyond.")
    show_stats(player)

    castle_input = input("Do you want to sneak past the guards, or fight your way through? (sneak/fight): ").strip().lower()

    if castle_input == "sneak":
        print("\nYou creep along the shadows of the outer wall. A guard patrol passes inches away.")
        print("Your heart pounds, but you slip through unseen, drained from the tension.")
        player["health"] -= 5
        player["stamina"] -= 20
    elif castle_input == "fight":
        print(f"\nYou draw your {weapon} and cut down the guards blocking the gate.")
        print("It's brutal and costs you dearly, but you loot a Shield off one of the fallen soldiers.")
        player["inventory"].append("Shield")
        player["health"] -= 30
        player["stamina"] -= 15
    else:
        print("\nCaught hesitating between the two paths, a guard spots you.")
        print("You're forced into a chaotic scramble through the gate, taking the worst of both approaches.")
        player["health"] -= 15
        player["stamina"] -= 25

    player["health"] = max(0, min(100, player["health"]))
    player["stamina"] = max(0, min(100, player["stamina"]))

    print(f"\nYour health is now {player['health']}, your stamina is now {player['stamina']}.")
    if check_game_over(player):
        return

    print("\nBeyond the castle walls, the village comes into view — warm lights, distant laughter, safety at last.")
    print("You've made it. Congratulations, adventurer — your journey is complete!")
    show_stats(player)


main()