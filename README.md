# Battleship
My attempt at the classic minigame "Battleship", refurbishing the traditional gamerules to implement 3 separate gamemodes.

Features:
- Customizable board dimension, ships' sizes and number of them, as well as placement

Gamemodes:
- (Singleplayer) "Battleship (hide)": player hides their ships manually, and computer will try and determine the location within a given number of guesses
- (Singleplayer) "Battleship (guess)": computer hides their ships automatically, and the player will try and determine the location within a given number of guesses
- (Singleplayer) "Battleship (hide and guess)": both computer and player hide their ships, and both will take turn trying to determine the location of all opponent's ships

Gameover:
- If number of guesses run out before locating all ships, guesser loses >< hider wins and vice-versa
- First one to locate all of their opponent's ships wins

Limit:
- Can only take manual coordinate input at this stage (can be cumbersome if too many ships)
- Playing board can only be either 7x7, 8x8, 9x9 big at this stage
- Ships can only be 1-dimensional at this stage (1x2, 1x3, 1x4...)
- Computer AI for (hide) mode is lacking in difficulty

Usage:
- "Polyhedron" is the source code, written in Python.

Possible future update:
- A GUI interface for all 3 gamemodes
- Support for more dynamic ship placement
- More ship sizes
- Bigger playing board
