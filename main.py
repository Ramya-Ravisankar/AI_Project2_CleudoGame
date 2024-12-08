"""
This is the main module for the Cluedo game.

It initializes the game, loads the game state, processes user inputs, and manages
core game actions such as moving, suggesting, and accusing. It also integrates player
notes for tracking suggestions and refutations.
"""
import re
import difflib
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic, PlayerNotes
from utils.random_selection import select_solution
from utils.json_loader import load_rooms_from_json  # Import the JSON loader

def parse_command(command):
    """
    Parse the player's command using regex patterns to identify the action and relevant arguments.
        Args:
        command (str): The raw input string entered by the player.
        Returns:
        tuple: A tuple containing the action (str) and a dictionary of matched arguments.
               If the command doesn't match any pattern, the action will be "unknown" and
              the dictionary will be empty.
    """
    patterns = {
        "move": r"(move|go|travel)\s*(to)?\s+(?P<room>\w+(\s+\w+)*)",
        "suggest": (
            r"suggest\s+"
            r"(?P<character>\w+(\s+\w+)*)\s*"
            r"(with)?\s+"
            r"(?P<weapon>\w+(\s+\w+)*)\s*"
            r"(in)?\s+"
            r"(?P<room>\w+(\s+\w+)*)"
            ),

        "accuse": (
                r"accuse\s+"
                r"(?P<character>\w+(\s+\w+)*)\s+with\s+"
                r"(?P<weapon>\w+(\s+\w+)*)\s+in\s+"
                r"(?P<room>\w+(\s+\w+)*)"
            ),

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

def display_room_connections(rooms):
    """
     Display all rooms and their connections. Useful for debugging or understanding
     the game map's layout.
     Args:
         rooms (list[Room]): List of Room objects to display connections for.
     Prints:
         A list of rooms with their connected rooms.
    """
    print("Room Connections:")
    for room in rooms:
        connections = ", ".join(room.list_connections())
        print(f"{room.name} -> {connections}")
    print("\n")


# Initialize PlayerNotes
player_notes = PlayerNotes()

# Load Rooms Dynamically from JSON
JSON_FILE = "data/rooms.json"
loaded_rooms = load_rooms_from_json(JSON_FILE)

# Debugging: Display room connections
display_room_connections(loaded_rooms)

# Ensure valid room names for character placement
valid_room_names = [room.name for room in loaded_rooms]
if len(valid_room_names) < 3:
    raise ValueError("Insufficient rooms available to place all characters.")

# Initialize Characters
characters = [
    Character("Miss Scarlett", "Kitchen" if "Kitchen" in valid_room_names else valid_room_names[0]),
    Character("Colonel Mustard", "Library" if "Library" in valid_room_names else valid_room_names[1]),
    Character("Professor Plum", "Ballroom" if "Ballroom" in valid_room_names else valid_room_names[2]),
]

# Initialize Weapons
weapons = [
    Weapon("Candlestick"),
    Weapon("Revolver"),
    Weapon("Rope"),
]

# Prompt user to reveal solution for debugging (optional)
reveal_solution = input("Reveal the solution for debugging? (yes/no): ").strip().lower() == "yes"

# Select Solution
solution = select_solution(characters, weapons, loaded_rooms, reveal_solution=True)

if reveal_solution:
    print("\nThe solution is:")
    print(f"Character: {solution[0].name}, Weapon: {solution[1].name}, Room: {solution[2].name}\n")

# Initialize GameLogic
game_logic = GameLogic(loaded_rooms, characters, weapons, solution)

# Game Start
print("Welcome to Cluedo!")
print("Solve the mystery of who committed the murder, with what weapon, and in which room.\n")

# Add the `current_turn` tracker here
CURRENT_TURN = 0  # Tracks the index of the current player in the `characters` list # pylint: disable=invalid-name

def advance_turn(current_turn,total_players):
    """
     Advance to the next player's turn.
    Args:
        current_turn (int): The current player's index.
        total_players (int): The total number of players.

    Returns:
        int: The next player's index.
    """
    return (current_turn + 1) % total_players

while True:
    current_player = characters[CURRENT_TURN]

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
    parsed_action, arguments = parse_command(raw_command)

    if parsed_action == "move":
        # Handles the player's movement to a specified room.
        # Validates the room and checks its connectivity to the player's current position.
        #   Updates the player's position if the move is valid.
        #    Args:
        #       room (str): The name of the room the player wants to move to.
        #    Outputs:
        #       Messages indicating whether the move was successful or why it failed.

        target_room = arguments.get("room")  # Extract room name
        target_room = correct_input(target_room, [r.name for r in loaded_rooms])  # Spell-check room name

        if target_room.lower() == current_player.position.lower():
            print(f"You are already in the {current_player.position}. No need to move!")
        elif target_room.lower() not in [r.name.lower() for r in loaded_rooms]:
            print(f"The room '{target_room}' does not exist. Please check the room name and try again.")
        else:
            available_rooms = game_logic.get_room_connections(current_player.position)
            if target_room.lower() in [r.lower() for r in available_rooms]:
                current_player.position = target_room
                print(f"You moved to the {current_player.position}.")
            else:
                print(
                    f"Invalid move: The room '{target_room}' is not connected to the '{current_player.position}'. "
                    f"Connected rooms are: {', '.join(available_rooms)}."
                )
        CURRENT_TURN = advance_turn(CURRENT_TURN, len(characters))

    elif parsed_action == "suggest":
        # Processes a player's suggestion.
        # Validates the suggested character, weapon, and room, ensuring the player is in
        #       the correct room.
        # Handles movement of suggested characters and weapons and checks if any player
        #       can refute the suggestion.
        # Args:
        #     character (str): The name of the suggested character.
        #     weapon (str): The name of the suggested weapon.
        #     room (str): The name of the suggested room.
        #  Outputs: Messages indicating the outcome of the suggestion, such as
        #       refutations or lack thereof.

        character = arguments.get("character")  # Extract character name
        weapon = arguments.get("weapon")        # Extract weapon name
        target_room = arguments.get("room")            # Extract room name

        # Apply fuzzy matching for inputs
        character = correct_input(character, [c.name for c in characters])
        weapon = correct_input(weapon, [w.name for w in weapons])
        target_room = correct_input(target_room, [r.name for r in loaded_rooms])

        if not character or not weapon or not target_room:
            print("Invalid suggestion. Example format: suggest Scarlett with Rope in Kitchen.")
            continue

        result = game_logic.make_suggestion(current_player, character, weapon, current_player.position) # pylint: disable=invalid-name
        print(result)
        player_notes.add_suggestion(character, weapon, current_player.position)
        CURRENT_TURN = advance_turn(CURRENT_TURN, len(characters))

    elif parsed_action == "accuse":
        # Processes a player's accusation.
        # Validates the accused character, weapon, and room against the solution.
        # Provides feedback if the accusation is incorrect, specifying which components are wrong.
        # Args:
        #      character (str): The name of the accused character.
        #        weapon (str): The name of the accused weapon.
        #       room (str): The name of the accused room.
        # Outputs:Messages indicating whether the accusation was correct or incorrect, along with feedback.
        character = arguments.get("character")  # Extract character name
        weapon = arguments.get("weapon")        # Extract weapon name
        target_room = arguments.get("room")            # Extract room name

        # Apply fuzzy matching for inputs
        character = correct_input(character, [c.name for c in characters])
        weapon = correct_input(weapon, [w.name for w in weapons])
        target_room = correct_input(target_room, [r.name for r in loaded_rooms])

        if not character or not weapon or not target_room:
            print("Invalid accusation. Example format: accuse Mustard with Revolver in Library.")
            continue

        accusation_feedback = game_logic.process_accusation(current_player.name, character, weapon, target_room) # # pylint: disable=invalid-name
        print(accusation_feedback)
        if "Accusation correct" in accusation_feedback:
            break  # End the game if the accusation is correct

        CURRENT_TURN = advance_turn(CURRENT_TURN, len(characters))

    elif parsed_action == "notes":
        # Displays the player's notes.
        # calls the `view_notes` method of the `PlayerNotes` class to show a summary of all stored
        # suggestions and refutations.
        player_notes.view_notes()

    elif parsed_action == "quit":
        # Handles the player's decision to quit the game.
        # Removes the quitting player from the `characters` list. If all players quit, ends the game.
        print(f"{current_player.name} has quit the game.")
        characters.pop(CURRENT_TURN)

        if len(characters) == 0:
            print("All players have left. The game is over!")
            break

        CURRENT_TURN %= len(characters)
        continue

    elif parsed_action == "help":
        # Displays a list of valid commands to help the player understand their options.
        print("\nValid commands:")
        print("- Move: 'move to Library', 'go Kitchen'")
        print("- Suggest: 'suggest Scarlett with Rope in Kitchen'")
        print("- Accuse: 'accuse Mustard with Revolver in Library'")
        print("- View notes: 'notes'")
        print("- Quit the game: 'quit'\n")

    else:
        print("Unknown command. Try again.")
