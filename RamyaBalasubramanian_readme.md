# Cluedo Game (PART 1 AND PART 2)

## Project Overview
This is a command-line implementation of the Cluedo game. The goal is to uncover the mystery by deducing the randomly selected character, weapon, and room involved in the crime. Players navigate through various rooms, make suggestions, and attempt to solve the mystery.

## Setup Instructions

1. Install Python 3.x (I have tested with Python version - 3.10.12)

2. Virtual Environment
   Install python virtual environment, so that we can manage the virtual environment to issolate our dependences from the global version of python. We need to do this once on our computer, this is a global python package using command - pip3 install virtualenv

3. Once Python and Virtual Environment Installed:
Clone the repository :
   - `git clone git@github.com:Ramya-Ravisankar/AI_Project2_CleudoGame.git

   Repository link - https://github.com/Ramya-Ravisankar/AI_Project2_CleudoGame

4. Navigate to the project directory:
   - `cd RamyaBalasubramanian_Project2_SourceCode`

5. python3 -m venv venv <- Create Virtual Environment using this command.
   It's a good practice to create a fresh virtual environment for each project.

   virtualenv venv <- Makes a virtual environment in the venv directory
   source ./venv/bin/activate < - Activate the virtual environment

6. Once the Virtual Environment is active, Install Dependencies using pip
   - pip3 install pytest pytest-pylint pytest-cov
   - pip3 install pytest-pylint

7. Once we have the libraries installed we need to freeze the requirements and create our
   requirments.txt file - pip3 freeze > requirements.txt

8. pip install -r requirements.txt [ When another person copies / clones my repository they will have to install the specfic library / dependency requirements for my project using the above command.]

9. How to Run the Tests:
   pytest -v <-runs the tests without pylint or coverage, enable verbose for more detailed output

   pytest --pylint -v <- Runs tests with pylint static code analysis, Enable verbose for more detailed output

   pytest --pylint --pylint-rcfile=pylintrc <-Runs tests with a custom Pylint configuration file that includes verbose settings.

   pytest --pylint -v --cache-clear <-checks all files, including those that previously passed,so that it does not skip files

   pylint main.py <- Example format , in case need to run individual files. Similarly can be run for all files

   pytest --cov=game_logic.py - <- Example format , in case need to run individual files. Similarly can be run for all files to know individual test case coverage

   pytest --pylint --cov -v <-Runs tests, pylint, and for code coverage. Enable verbose for more detailed output


10. Instructions to Run the cleudo game:
   - NAVIGATE TO PROJECT DIRECTORY :
   In the terminal ensure that the current working directory points to  RamyaBalasubramanian_Project2_SourceCode

   - RUN THE GAME :
   Execute the following command to start the game:- `python3 main.py`

   - REVEALING THE MYSTERY :
   At the start of the game, you will be prompted to choose whether the mystery solution (the murderer, weapon, and room) should be revealed. This is optional and varies each time, as the solution is randomly generated.

   - INPUT OPTIONS AND COMMANDS :
      Follow the on-screen instructions to provide input in the specified format
      If an input does not match the expected format, it will be flagged as an "unknown command".
      Regex patterns are implemented to handle inputs (e.g., case-insensitive commands).

   - GAME PLAY FLOW
      Players can make moves, suggest suspects, accuse someone, or manage notes during their turn.
      The game ends either when the mystery is solved through a correct accusation or when all players quit.

   - PLAYER NOTES :
      Players can add or remove notes during the game to track suggestions, refutations, or any custom observations.

## Version Control:
    git