"""
Unit tests for Bayesian reasoning logic in the Cluedo game.

This module tests the `BayesianReasoner` class, which uses probabilities to model
the likelihood of various character, weapon, and room combinations based on
player suggestions and refutations.

Tests include:
- Verifying that probabilities update correctly when suggestions are refuted or not refuted.
- Ensuring that probabilities are normalized and always sum to 1.
- Validating that the most likely combination is identified correctly.
"""

import unittest
from game_logic import BayesianReasoner  # Ensure this matches the location of your BayesianReasoner class

class TestBayesianReasoner(unittest.TestCase):
    """
    Unit tests for the BayesianReasoner class in the Cluedo game.

    These tests ensure that the Bayesian reasoning logic updates and normalizes
    probabilities correctly based on player suggestions and refutations.
    """
    def setUp(self):
        """
        Set up the test environment.

        Initializes the BayesianReasoner with:
        - Characters: ["Scarlett", "Mustard"]
        - Weapons: ["Rope", "Revolver"]
        - Rooms: ["Kitchen", "Library"]

        This provides a controlled environment for testing probability updates
        and reasoning logic.
        """
        self.characters = ["Scarlett", "Mustard"]
        self.weapons = ["Rope", "Revolver"]
        self.rooms = ["Kitchen", "Library"]
        self.reasoner = BayesianReasoner(self.characters, self.weapons, self.rooms)

    def test_update_probabilities(self):
        """
        Test the probability updates in BayesianReasoner.

        Verifies:
        - Probabilities increase when a suggestion is not refuted.
        - Probabilities decrease when a suggestion is refuted.
        - Probabilities are normalized to sum to 1 after updates.
        - The most likely combination is correctly identified based on updates.

        Scenarios:
        - Update probabilities for "Scarlett", "Rope", "Kitchen" (not refuted).
        - Update probabilities for "Mustard", "Revolver", "Library" (refuted).
        """

        # Update probabilities and check the most likely suggestion
        self.reasoner.update_probabilities("Scarlett", "Rope", "Kitchen", refuted=False)
        most_likely = self.reasoner.get_most_likely()
        self.assertEqual(most_likely, ("Scarlett", "Rope", "Kitchen"))

        # Refute another suggestion and check probabilities
        self.reasoner.update_probabilities("Mustard", "Revolver", "Library", refuted=True)
        updated_prob = self.reasoner.probabilities[("Mustard", "Revolver", "Library")]
        self.assertLess(updated_prob, 1, "Probability should decrease when refuted.")

        # Check normalization
        total_prob = sum(self.reasoner.probabilities.values())
        self.assertAlmostEqual(total_prob, 1, msg="Probabilities should sum to 1.")

if __name__ == "__main__":
    unittest.main()
