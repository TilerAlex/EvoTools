# Evo Tools

Program for "Twilight's Eve Evo" Warcraft 3 custom map:

  - In-game overlay
  - Arrows mechanics automation *(Imp2 / m1)*
  - Fishing automation
  - Leveling automation
  - Shows clue direction *(Imp1)*
  - Damage board with latest dungeon run data
  - Dynamically scalable in-game overlay

Made by Tiler

*(Reworked "Evo Arrows Helper" by RagingCat)*

## Requirements

- **Warcraft III**:
  - "1920x1080", "2560x1440" or "2560x1600" resolution
  - Original graphics
  - English locale
  - Game window not minimized

## Menu
 - **Main**:
   - `Ctrl+F1` Automation menu
   - `Ctrl+F2` Damage board menu
   - `Ctrl+F3` System menu
 - **Automation**:
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Clues menu
   - `Ctrl+F3` Arrows menu
   - `Ctrl+F4` Fishing menu
   - `Ctrl+F5` Leveling menu
 - **Clues**: *(Shows what direction to go. Imp1 mechanics)*
   - `Ctrl+F1` Automation menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Print [yes/no] *(Prints direction to chat)*
 - **Arrows**: *(Automatically clicks required arrow used in Imp2 and m1 mechanics)*
   - `Ctrl+F1` Automation menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Camera back [yes/no] *(Clicks the opposite direction to bring camera back)*
 - **Fishing**: *(Does fishing cycle)*
   - `Ctrl+F1` Automation menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Fishing mode: *(rod must be in num8 inventory)*
     - Perfect
     - Perfect (no Flying with fish)
     - Great
     - Standard
   - `Ctrl+F4` Respawn point *(Sets point where hero will run with auto-attack after death)*
   - `Ctrl+F5` Auto-save interval [none,5,10,30] *(Drops caught fish by executing "-s" command)*
 - **Leveling**: *(Allows to level in idle)*
   - `Ctrl+F1` Automation menu
   - `Ctrl+F2` Turn on/off functionality
   - `Ctrl+F3` Click button *(Allows to set a key that will be periodically clicked. Used to start and finish quests)*
   - `Ctrl+F4` Click interval [none,1,2,3] *(Sets click periodicity in secords)*
   - `Ctrl+F5` Auto-save interval [none,5,10,30] *(Saves hero with "-s" command)*
 - **Damage board**: *(Shows content of Damage.txt file sorted by damage sum)*
   - `Ctrl+F1` Main menu
   - `Ctrl+F2` Show/hide overlay
   - `Ctrl+F3` Position [Top right, Bot right]
 - **System**: *(Shows system data)*
   - `Ctrl+F1` Main menu

## Instructions

Program can be run using 2 ways:

1. Using executable file:
    - Download and run `EvoTools.X.X.exe`

2. Using compiled files:
    - Install [Python 3.12](https://www.python.org/downloads/release/python-3129/)
      - **Important**: During installation, make sure to check the option to "Add Python to PATH".
    - Upack `EvoTools.X.X.zip` archive
    - Run `start.bat` file
    - The program will start once all required libraries are installed for the first time
