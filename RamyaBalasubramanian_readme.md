# Cluedo Game (Part 1)

## Project Overview
This is a command-line version of the Cluedo game. The objective is to randomly select a character, weapon, and room as the solution to the murder mystery. Players can move through different rooms, make suggestions, and try to solve the mystery.

## Project Structure
RAMYABALASUBRAMANIAN_PROJECT2_SOURCECODE
├── main.py                # Main entry point for the game
├── game_logic.py          # Core game functionality
├── classes/
│   ├── room.py            # Room-related classes and logic
│   ├── character.py       # Character-related classes and logic
│   ├── weapon.py          # Weapon-related classes and logic│
├── utils/
│   ├── random_selection.py # Logic for random solution selection
│   └── movement.py        # Room navigation logic
├── data/
│   ├── rooms.json         # Mansion layout data
│   └── characters.json    # Character and weapon definitions
├── tests/
│   ├── test_movement.py   # Unit tests for player movement logic in the game
│   ├── test_bayesian.py   # Unit tests for Bayesian reasoning used by the AI player.
│   ├── test_suggestions.py # Unit tests for validating the suggestion feature in the game.
│   ├── test_accusations.py # Unit tests for handling accusations in the game.
│
│── RamyaBalasubramanian_readme.md  # Instructions for running the game

## Setup Instructions

1. Install Python 3.x (I have tested with Python version - 3.10.12)

2. Virtual Environment
   Install python virtual environment, so that we can manage the virtual environment to issolate our dependences from the global version of python. We need to do this once on our computer, this is a global python package using command - pip3 install virtualenv

4. Once Python and Virtual Environment Installed:
Clone the repository :
   - `git clone git@github.com:Ramya-Ravisankar/AI_Project2_CleudoGame.git

   Repository link - https://github.com/Ramya-Ravisankar/AI_Project2_CleudoGame

5. Navigate to the project directory:
   - `cd RamyaBalasubramanian_Project2_SourceCode`

6. python3 -m venv venv <- Create Virtual Environment using this command.
   It's a good practice to create a fresh virtual environment for each project.

   virtualenv venv <- Makes a virtual environment in the venv directory
   source ./venv/bin/activate < - Activate the virtual environment

6. Once the Virtual Environment is active, Install Dependencies using pip
   - pip3 install pytest pytest-pylint pytest-cov

7. Once we have the libraries installed we need to freeze the requirements and create our
   requirments.txt file - pip3 freeze > requirements.txt

8. pip install -r requirements.txt [ When another person copies / clones my repository they will have to install the specfic library / dependency requirements for my project using the above command.]

9. How to Run the Tests:
   pytest -v <-runs the tests without pylint or coverage, enable verbose for more detailed output

   pytest --pylint -v <- Runs tests with pylint static code analysis, Enable verbose for more detailed output [ OR ]
   pytest --pylint --pylint-rcfile=pylintrc <-Runs tests with a custom Pylint configuration file that includes verbose settings.

   pytest --pylint --cov -v <-Runs tests, pylint, and coverage to check if you have all your code tested.Enable verbose for more detailed output

10. Run the cleudo game:
   - `python3 main.py`
   - A random solution selection is displayed initially ( differs each time as its random)
   - Input options available - follow the instructions and continue to play the game
   - Post accusation, If the mystery is solved or not solved, game exits

## Dependencies
- Required libraries (list in requirements.txt) - steps as above on how to install dependencies.

## Game Flow
1. The game starts by randomly selecting a character, weapon, and room as the solution.
2. Players can move between rooms and make suggestions.
3. The game displays messages on the actions taken by the players.

## Version Control:
    git