class GameLogic:
    def __init__(self, rooms, characters, weapons, solution):
        """
        Initialize the game logic.

        :param rooms: List of Room objects.
        :param characters: List of Character objects.
        :param weapons: List of Weapon objects.
        :param solution: Tuple containing the solution (character, weapon, room).
        """
        self.rooms = rooms
        self.characters = characters
        self.weapons = weapons
        self.solution = solution  # Tuple: (Character, Weapon, Room)

    def make_suggestion(self, suggesting_player, character_name, weapon_name, room_name):
        """
        Process a player's suggestion.

        :param suggesting_player: The player making the suggestion.
        :param character_name: Name of the character being suggested.
        :param weapon_name: Name of the weapon being suggested.
        :param room_name: Name of the room being suggested.
        :return: A message summarizing the result of the suggestion.
        """
        # Validate current room
        current_room = next((room for room in self.rooms if room.name == suggesting_player.position), None)
        if current_room is None or current_room.name != room_name:
            return (
            f"Invalid suggestion: "
            f"You must be in the {room_name} to suggest it."
        )

        # Find the suggested character and weapon
        suggested_character = next((char for char in self.characters if char.name == character_name), None)
        suggested_weapon = next((weap for weap in self.weapons if weap.name == weapon_name), None)

        if not suggested_character or not suggested_weapon:
            return "Invalid suggestion: Character or weapon does not exist."

        # Move character and weapon to the suggested room
        suggested_character.position = room_name
        suggested_weapon.location = room_name

        return f"Suggestion made: {character_name} with the {weapon_name} in the {room_name}."

    def check_solution(self, character_name, weapon_name, room_name):
        """
        Check if a player's accusation matches the solution.

        :param character_name: Name of the character being accused.
        :param weapon_name: Name of the weapon being accused.
        :param room_name: Name of the room being accused.
        :return: A message stating if the accusation is correct or not.
        """
        solution_character, solution_weapon, solution_room = self.solution

        if (
            solution_character.name == character_name
            and solution_weapon.name == weapon_name
            and solution_room.name == room_name
        ):
            return "Accusation correct! You've solved the murder!"
        else:
            return "Accusation incorrect. The mystery remains unsolved."

    def get_room_connections(self, room_name):
        """
        Get a list of connected rooms for the given room.

        :param room_name: The room name for which connections are to be retrieved.
        :return: A list of names of connected rooms.
        """
        room = next((r for r in self.rooms if r.name == room_name), None)
        if room:
            return [connected_room.name for connected_room in room.connected_rooms]
        return []

    def display_game_state(self):
        """
        Display the current state of the game for debugging purposes.
        """
        print("\nGame State:")
        print("Characters:")
        for char in self.characters:
            print(f"- {char.name} is in {char.position}")
        print("Weapons:")
        for weap in self.weapons:
            print(f"- {weap.name} is in {weap.location}")
        print("Rooms:")
        for room in self.rooms:
            print(f"- {room.name} connects to {[r.name for r in room.connected_rooms]}")

    def process_accusation(self, accused_character, accused_weapon, accused_room):
        """
        Process the player's accusation and provide feedback.

    Args:
        accused_character (str): Name of the character being accused.
        accused_weapon (str): Name of the weapon being accused.
        accused_room (str): Name of the room being accused.

    Returns:
        bool: True if the accusation matches the solution, False otherwise.
        """
        # Extract the solution components
        solution_character, solution_weapon, solution_room = self.solution

        # Normalize accused and solution values to lowercase for comparison
        accused = {
            "character": accused_character.strip().lower(),
            "weapon": accused_weapon.strip().lower(),
            "room": accused_room.strip().lower(),
        }

        solution = {
            "character": solution_character.name.strip().lower(),
            "weapon": solution_weapon.name.strip().lower(),
            "room": solution_room.name.strip().lower(),
        }

        # Check if the accusation matches the solution
        if accused == solution:
            return True

        # Provide feedback for incorrect accusation
        print("Accusation incorrect. Here's your feedback:")
        for key in accused:
            status = "correct" if accused[key] == solution[key] else "incorrect"
            print(f"- {key.capitalize()} is {status}.")
        return False