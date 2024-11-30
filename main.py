# main.py
import random
from mansion import Mansion
from characters import characters
from weapons import weapons

mansion = Mansion()

solution = {
    "character": random.choice(list(characters.keys())),
    "weapon": random.choice([weapon.name for weapon in weapons]),
    "room": random.choice(list(mansion.rooms.keys()))
}

player = {"current_room": "Kitchen"}

def print_room_info():
    print(f"\nYou are in the {player['current_room']}.")
    neighbors = mansion.get_neighbors(player["current_room"])
    print(f"Connected rooms: {', '.join(neighbors)}")

def move_player():
    print_room_info()
    destination = input("Enter the room you want to move to: ").strip()
    if destination in mansion.get_neighbors(player["current_room"]):
        player["current_room"] = destination
        print(f"You moved to the {destination}.")
    else:
        print("You cannot move to that room.")

def make_suggestion():
    print("\nMake a suggestion!")
    character = input("Which character? ").strip()
    weapon = input("Which weapon? ").strip()
    room = player["current_room"]

    print(f"\nYou suggested: {character}, {weapon}, {room}")
    feedback = []
    if character != solution["character"]:
        feedback.append(f"The character is not {character}.")
    if weapon != solution["weapon"]:
        feedback.append(f"The weapon is not {weapon}.")
    if room != solution["room"]:
        feedback.append(f"The room is not {room}.")

    if feedback:
        print("\n".join(feedback))
    else:
        print("Congratulations! You've solved the mystery!")
        return True
    return False

def main():
    print("Welcome to Cluedo!")
    print("Move between rooms and make suggestions to solve the mystery.")
    print("Type 'move' to navigate and 'suggest' to make a suggestion.")

    while True:
        command = input("\nWhat would you like to do? (move/suggest/quit): ").strip().lower()
        if command == "move":
            move_player()
        elif command == "suggest":
            if make_suggestion():
                break
        elif command == "quit":
            print("Thanks for playing!")
            break
        else:
            print("Invalid command. Please enter 'move', 'suggest', or 'quit'.")

if __name__ == "__main__":
    main()
