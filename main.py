"""
This is the main module for the Cluedo game.
It initializes the game, processes user inputs, and manages game actions such as moving, suggesting, and accusing.
"""
import re
import difflib
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from utils.random_selection import select_solution
from game_logic import GameLogic, PlayerNotes


def parse_command(command):
    """
    Parse the player's command using regex patterns.
    """
    patterns = {
        "move": r"(move|go|travel)\s*(to)?\s+(?P<room>\w+(\s+\w+)*)",
        "suggest": r"suggest\s+(?P<character>\w+(\s+\w+)*)\s*(with)?\s+(?P<weapon>\w+(\s+\w+)*)\s*(in)?\s+(?P<room>\w+(\s+\w+)*)",
        "accuse": r"accuse\s+(?P<character>\w+(\s+\w+)*)\s+with\s+(?P<weapon>\w+(\s+\w+)*)\s+in\s+(?P<room>\w+(\s+\w+)*)",
        "notes": r"(view\s*)?notes",
        "quit": r"quit\s*",
        "help": r"help"
    }

    for action, pattern in patterns.items():
        match = re.match(pattern, command, re.IGNORECASE)
        if match:
            return action, match.groupdict()

    return "unknown", {}


def correct_input(input_value, valid_options):
    """
    Suggest or correct the input_value against a list of valid options.
    Args:
        input_value (str): The player's input.
        valid_options (list): List of valid strings to match against.

    Returns:
        str: Closest match if found, else the original input.
    """
    matches = difflib.get_close_matches(input_value.lower(), [v.lower() for v in valid_options], n=1, cutoff=0.6)
    if matches:
        return next((option for option in valid_options if option.lower() == matches[0]), input_value)
    return input_value  # If no match, return the input as is


# Initialize PlayerNotes
player_notes = PlayerNotes()

# Initialize Rooms
kitchen = Room("Kitchen")
ballroom = Room("Ballroom")
library = Room("Library")
study = Room("Study")

# Connect Rooms
kitchen.connect(ballroom)
ballroom.connect(library)
library.connect(study)

rooms = [kitchen, ballroom, library, study]

# Initialize Characters
characters = [
    Character("Miss Scarlett", "Kitchen"),
    Character("Colonel Mustard", "Library"),
    Character("Professor Plum", "Ballroom"),
]

# Initialize Weapons
weapons = [
    Weapon("Candlestick"),
    Weapon("Revolver"),
    Weapon("Rope"),
]

# Select Solution
solution = select_solution(characters, weapons, rooms, reveal_solution=True)
reveal_solution = True

if reveal_solution:
    print("\nThe solution is:")
    print(f"Character: {solution[0].name}, Weapon: {solution[1].name}, Room: {solution[2].name}\n")

# Initialize GameLogic
game_logic = GameLogic(rooms, characters, weapons, solution)

# Game Start
print("Welcome to Cluedo!")
print("Solve the mystery of who committed the murder, with what weapon, and in which room.\n")

# Add the `current_turn` tracker here
current_turn = 0  # Tracks the index of the current player in the `characters` list

def advance_turn():
    """Advance to the next player's turn."""
    global current_turn
    current_turn = (current_turn + 1) % len(characters)


while True:
    current_player = characters[current_turn]

    # Human player's turn
    print(f"\n{current_player.name}, it's your turn!")
    print("\nOptions:")
    print(" - Move to a room: 'move to Library' or 'go Kitchen'")
    print(" - Suggest a suspect: 'suggest Scarlett with Rope in Kitchen'")
    print(" - Accuse someone: 'accuse Mustard with Revolver in Library'")
    print(" - View notes: 'notes'")
    print(" - Quit the game: 'quit'\n")

    game_logic.display_filtered_game_state(current_player)

    # Get the player's raw input
    raw_command = input("Enter your command: ").strip()

    # Parse the command
    action, arguments = parse_command(raw_command)

    if action == "move":
        room = arguments.get("room")  # Extract room name
        room = correct_input(room, [r.name for r in rooms])  # Spell-check room name

        if room.lower() == current_player.position.lower():
            print(f"You are already in the {current_player.position}. No need to move!")
        elif room.lower() not in [r.name.lower() for r in rooms]:
            print(f"The room '{room}' does not exist. Please check the room name and try again.")
        else:
            available_rooms = game_logic.get_room_connections(current_player.position)
            if room.lower() in [r.lower() for r in available_rooms]:
                current_player.position = room
                print(f"You moved to the {current_player.position}.")
            else:
                print(
                    f"Invalid move: The room '{room}' is not connected to the '{current_player.position}'. "
                    f"Connected rooms are: {', '.join(available_rooms)}."
                )
        advance_turn()

    elif action == "suggest":
        character = arguments.get("character")  # Extract character name
        weapon = arguments.get("weapon")        # Extract weapon name
        room = arguments.get("room")            # Extract room name

        # Apply fuzzy matching for inputs
        character = correct_input(character, [c.name for c in characters])
        weapon = correct_input(weapon, [w.name for w in weapons])
        room = correct_input(room, [r.name for r in rooms])

        if not character or not weapon or not room:
            print("Invalid suggestion. Example format: suggest Scarlett with Rope in Kitchen.")
            continue

        result = game_logic.make_suggestion(current_player, character, weapon, current_player.position)
        print(result)
        player_notes.add_suggestion(character, weapon, current_player.position)
        advance_turn()

    elif action == "accuse":
        character = arguments.get("character")  # Extract character name
        weapon = arguments.get("weapon")        # Extract weapon name
        room = arguments.get("room")            # Extract room name

        # Apply fuzzy matching for inputs
        character = correct_input(character, [c.name for c in characters])
        weapon = correct_input(weapon, [w.name for w in weapons])
        room = correct_input(room, [r.name for r in rooms])

        if not character or not weapon or not room:
            print("Invalid accusation. Example format: accuse Mustard with Revolver in Library.")
            continue

        result = game_logic.process_accusation(current_player.name, character, weapon, room)
        print(result)
        if "Accusation correct" in result:
            break  # End the game if the accusation is correct

        advance_turn()

    elif action == "notes":
        player_notes.view_notes()

    elif action == "add_note":
        note = input("Enter a note to add: ").strip()
        player_notes.add_manual_entry(note)
        print("Note added.")

    elif action == "remove_note":
        note = input("Enter a note to remove: ").strip()
        player_notes.remove_manual_entry(note)
        print("Note removed.")

    elif action == "quit":
        print(f"{current_player.name} has quit the game.")
        characters.pop(current_turn)

        if len(characters) == 0:
            print("All players have left. The game is over!")
            break

        current_turn %= len(characters)
        continue

    elif action == "help":
        print("\nValid commands:")
        print("- Move: 'move to Library', 'go Kitchen'")
        print("- Suggest: 'suggest Scarlett with Rope in Kitchen'")
        print("- Accuse: 'accuse Mustard with Revolver in Library'")
        print("- View notes: 'notes'")
        print("- Quit the game: 'quit'\n")

    else:
        print("Unknown command. Try again.")
