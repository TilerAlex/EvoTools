# Evo Tools

Program for "Twilight's Eve Evo" Warcraft 3 custom map:

  - In-game overlay
  - Arrows mechanics automation *(Imp2 / m1)*
  - Fishing automation
  - Leveling automation
  - Shows clue direction *(Imp1)*

Made by Tiler

*(Reworked "Evo Arrows Helper" by RagingCat)*

## Requirements

- **Python 3.12**: ([download](https://www.python.org/downloads/release/python-3129/))
- **Warcraft III**:
  - "1920x1080" or "2560x1440" resolution
  - Original graphics
  - English locale
  - Game window not minimized

## Menu
 - **Main**:
   - `Ctrl+F1` Clues menu
   - `Ctrl+F2` Arrows menu
   - `Ctrl+F3` Fishing menu
   - `Ctrl+F4` Leveling menu
   - `Ctrl+F5` System menu
 - **Clues**: *(Shows what direction to go. Imp1 mechanics)*
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Print [yes/no] *(Prints direction to chat)*
 - **Arrows**: *(Automatically clicks required arrow used in Imp2 and m1 mechanics)*
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Camera back [yes/no] (Clicks the opposite direction to bring camera back)
 - **Fishing**: *(Does fishing cycle)*
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Fishing mode:
     - Perfect
     - Perfect (no Flying with fish)
     - Great
     - Standard
   - `Ctrl+F4` Respawn point *(Sets point where hero will run with auto-attack after death)*
   - `Ctrl+F5` Auto-save interval [none,5,10,30] *(Drops caught fish by doing "-s" saving)*
 - **Leveling**: *(Allows to level in idle)*
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Click button *(Allows to set a key that will be periodically clicked. Used to start and finish quests)*
   - `Ctrl+F4` Click interval [none,1,2,3] *(Sets click periodicity in secords)*
   - `Ctrl+F5` Auto-save interval [none,5,10,30] *(Saves hero with "-s" saving)*
 - **System**: *(Shows system data)*
   - `Ctrl+F1` Main menu

## Instructions

1. Ensure you have Python 3.12 installed. ([download](https://www.python.org/downloads/release/python-3129/))
   - **Important**: During installation, make sure to check the option to "Add Python to PATH".
2. Run the `start.bat` file.
3. The program will start once all prerequisite libraries are installed for the first time.
