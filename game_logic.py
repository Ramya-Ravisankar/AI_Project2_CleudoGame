"""
This module contains the GameLogic class, which manages the core mechanics of the game.

The GameLogic class handles suggestions, accusations, and game state tracking.
"""
class GameLogic:
    """
    Manages the core mechanics of the game, including suggestions and accusations.

    Attributes:
        rooms (list[Room]): List of rooms in the game.
        characters (list[Character]): List of characters in the game.
        weapons (list[Weapon]): List of weapons in the game.
        solution (tuple): The correct combination of character, weapon, and room.
    """
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

        Room Validation:

The code validates that the suggesting player is in the correct room (room_name), ensuring suggestions are only made from the player's current location.
Character and Weapon Existence Check:

Ensures the suggested character and weapon exist in the game, avoiding invalid suggestions.
Character and Weapon Movement:

Moves the suggested character and weapon to the suggested room (room_name), which is a requirement for game state consistency.
Refutation Logic:

Iterates over all players except the suggesting player to check if any of them can refute the suggestion.
Each player's cards attribute is checked to see if they hold the suggested character, weapon, or room card.
The first player who can refute does so, and the function returns immediately with the refutation details.
Handles No Refutation:

If no players can refute the suggestion, a message is returned stating that no one could refute.
        """
        # Validate current room
        current_room = next((room for room in self.rooms if room.name == suggesting_player.position), None)
        if current_room is None or current_room.name != room_name:
            return f"Invalid suggestion: You must be in the {room_name} to suggest it."

        # Find the suggested character and weapon
        suggested_character = next((char for char in self.characters if char.name == character_name), None)
        suggested_weapon = next((weap for weap in self.weapons if weap.name == weapon_name), None)

        if not suggested_character or not suggested_weapon:
            return "Invalid suggestion: Character or weapon does not exist."

        # Move character and weapon to the suggested room
        suggested_character.position = room_name
        suggested_weapon.location = room_name

        # Handle refutations
        for player in self.characters:
            if player == suggesting_player:
                continue  # Skip the suggesting player

            # Check if the player can refute the suggestion
            refutable_cards = []
            if character_name in player.cards:
                refutable_cards.append(character_name)
            if weapon_name in player.cards:
                refutable_cards.append(weapon_name)
            if room_name in player.cards:
                refutable_cards.append(room_name)

            if refutable_cards:  # If the player can refute
                return f"Suggestion refuted by {player.name} with {refutable_cards[0]}."

        # No refutations found
        return f"Suggestion made: {character_name} with the {weapon_name} in the {room_name}. No one could refute."

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

    def display_filtered_game_state(self, current_player):
        """Display state relevant to the current player."""
        print(f"\n{current_player.name}'s Current Room: {current_player.position}")
        print("Nearby Rooms:")
        for room in self.get_room_connections(current_player.position):
            print(f"- {room}")

        print("\nCharacters in your room:")
        for char in self.characters:
            if char.position == current_player.position:
                print(f"- {char.name}")

        print("\nWeapons in your room:")
        for weapon in self.weapons:
            if weapon.location == current_player.position:
                print(f"- {weapon.name}")


    def process_accusation(self, accusing_character,accused_character, accused_weapon, accused_room):
        """
        Process a player's accusation and provide feedback.

        Args:
        accused_character (str): The name of the character being accused.
        accusing_character (str): The name of the character making the accusation
        accused_weapon (str): The name of the weapon being accused.
        accused_room (str): The name of the room being accused.

        Logic:
        The method extracts the correct solution (character, weapon, and room) stored in the game.
        Each part of the accusation (accused_character, accused_weapon, accused_room) is compared (case-insensitively) to the corresponding part of the solution.
        If all three components match, the accusation is correct, and the method returns True.
        If the accusation is incorrect, the method:
        Constructs a feedback list describing which parts of the accusation are incorrect.
        Prints detailed feedback for the player to use for future deductions.

        Returns:
        bool: True if the accusation is correct (game ends), False otherwise.
        """
        # Check for self-accusation
        if accusing_character.lower() == accused_character.lower():
            print(f"{accusing_character}, you cannot accuse yourself!")
            return None

        # Extract the solution components
        solution_character, solution_weapon, solution_room = self.solution

        # Check if the accusation matches the solution
        if (
            accused_character.lower() == solution_character.name.lower()
            and accused_weapon.lower() == solution_weapon.name.lower()
            and accused_room.lower() == solution_room.name.lower()
        ):
            return True  # Correct accusation;game ends

        # Mark the player as having made an accusation
        for player in self.characters:
            if player.name.lower() == accusing_character.lower():
                player.has_made_accusation = True

        # Provide feedback for incorrect accusation
        feedback = []
        if accused_character.lower() != solution_character.name.lower():
            feedback.append(f"Character '{accused_character}' is incorrect.")
        if accused_weapon.lower() != solution_weapon.name.lower():
            feedback.append(f"Weapon '{accused_weapon}' is incorrect.")
        if accused_room.lower() != solution_room.name.lower():
            feedback.append(f"Room '{accused_room}' is incorrect.")

        print("Accusation incorrect. Feedback:")
        for item in feedback:
            print(item)

        return False # Incorrect accusation

class PlayerNotes:
    """Tracks player notes, suggestions, and refutations."""
    def __init__(self):
        self.suggestions = []

    def add_suggestion(self, character, weapon, room, refuted_by=None):
        """Log a suggestion."""
        self.suggestions.append({
            "character": character,
            "weapon": weapon,
            "room": room,
            "refuted_by": refuted_by
        })

    def view_notes(self):
        """Display all recorded notes."""
        print("\nPlayer Notes:")
        for note in self.suggestions:
            print(f"Suggested: {note['character']} with {note['weapon']} in {note['room']}")
            if note["refuted_by"]:
                print(f" - Refuted by {note['refuted_by']}")
        print("\n")

    def add_manual_entry(self, note):
        """Add a manual note."""
        self.suggestions.append({"manual_note": note})

    def remove_manual_entry(self, note):
        """Remove a manual note."""
        self.suggestions = [n for n in self.suggestions if n.get("manual_note") != note]

