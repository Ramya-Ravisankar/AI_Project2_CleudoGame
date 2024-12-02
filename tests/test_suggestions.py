import unittest
from classes.room import Room
from classes.character import Character
from classes.weapon import Weapon
from game_logic import GameLogic

class TestSuggestions(unittest.TestCase):

    def setUp(self):
        """Set up the game environment for testing."""
        # Initialize Rooms
        self.kitchen = Room("Kitchen")
        self.ballroom = Room("Ballroom")
        self.library = Room("Library")

        # Connect Rooms
        self.kitchen.connect(self.ballroom)
        self.ballroom.connect(self.library)

        self.rooms = [self.kitchen, self.ballroom, self.library]

        # Initialize Characters
        self.miss_scarlett = Character("Miss Scarlett", "Kitchen")
        self.colonel_mustard = Character("Colonel Mustard", "Library")
        self.professor_plum = Character("Professor Plum", "Ballroom")
        self.characters = [self.miss_scarlett, self.colonel_mustard, self.professor_plum]

        # Initialize Weapons
        self.candlestick = Weapon("Candlestick")
        self.revolver = Weapon("Revolver")
        self.rope = Weapon("Rope")
        self.weapons = [self.candlestick, self.revolver, self.rope]

        # Initialize GameLogic
        self.solution = (self.miss_scarlett, self.candlestick, self.kitchen)
        self.game_logic = GameLogic(self.rooms, self.characters, self.weapons, self.solution)

    def test_valid_suggestion(self):
        """Test if a valid suggestion moves the suggested character and weapon to the current room."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Kitchen"  # Player is in the Kitchen
        character_name = "Colonel Mustard"
        weapon_name = "Revolver"
        room_name = "Kitchen"

        result = self.game_logic.make_suggestion(suggesting_player, character_name, weapon_name, room_name)

        # Assertions for the suggestion
        self.assertEqual(result, "Suggestion made: Colonel Mustard with the Revolver in the Kitchen.")
        self.assertEqual(self.colonel_mustard.position, "Kitchen", "Colonel Mustard should now be in the Kitchen.")
        self.assertEqual(self.revolver.location, "Kitchen", "Revolver should now be in the Kitchen.")

    def test_invalid_suggestion_room(self):
        """Test behavior when suggesting a room the player is not in."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Ballroom"  # Player is in the Ballroom
        character_name = "Colonel Mustard"
        weapon_name = "Revolver"
        room_name = "Kitchen"

        result = self.game_logic.make_suggestion(suggesting_player, character_name, weapon_name, room_name)

        # Assertion for invalid room suggestion
        self.assertEqual(result, "Invalid suggestion: You must be in the Kitchen to suggest it.")

    def test_invalid_character_or_weapon(self):
        """Test behavior when suggesting a non-existent character or weapon."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Kitchen"  # Player is in the Kitchen

        # Invalid character
        result = self.game_logic.make_suggestion(suggesting_player, "Invalid Character", "Revolver", "Kitchen")
        self.assertEqual(result, "Invalid suggestion: Character or weapon does not exist.")

        # Invalid weapon
        result = self.game_logic.make_suggestion(suggesting_player, "Colonel Mustard", "Invalid Weapon", "Kitchen")
        self.assertEqual(result, "Invalid suggestion: Character or weapon does not exist.")

    def test_suggestion_does_not_affect_solution(self):
        """Test that making a suggestion does not alter the game's solution."""
        suggesting_player = self.miss_scarlett
        suggesting_player.position = "Kitchen"  # Player is in the Kitchen
        character_name = "Professor Plum"
        weapon_name = "Rope"
        room_name = "Kitchen"

        # Make a suggestion
        self.game_logic.make_suggestion(suggesting_player, character_name, weapon_name, room_name)

        # Assert that the solution remains unchanged
        solution_character, solution_weapon, solution_room = self.solution
        self.assertEqual(solution_character, self.miss_scarlett, "Solution character should not change.")
        self.assertEqual(solution_weapon, self.candlestick, "Solution weapon should not change.")
        self.assertEqual(solution_room, self.kitchen, "Solution room should not change.")

if __name__ == "__main__":
    unittest.main()
