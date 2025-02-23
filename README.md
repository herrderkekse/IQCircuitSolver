
# Disclaimer  
This is an independent, unofficial, open-source project created for educational and non-commercial purposes. This project is not affiliated with, endorsed by, or otherwise officially connected to the developers, publishers, or licensors of the **IQ Circuit** game. The names, trademarks, logos, and other proprietary designations associated with **IQ Circuit** belong solely to their respective owners (**SmartGames**) and are used here solely for reference. All code, graphics, and other materials in this repository have been developed independently. Use of this project is at your own risk, and no warranties or guarantees are provided.

# IQCircuitSolver  
This project aims to provide a solver for the game "[IQ Circuit](https://www.smartgames.eu/uk/one-player-games/iq-circuit)" by "SmartGames", simply as a coding and algorithmic challenge.

Currently, there is only one (wildly inefficient) solver available. The goal is to implement a few options, exploring different algorithms. Feel free to play around yourself and create a pull request. There is still a lot of room for algorithmic improvements, so Python should be sufficient for now. But implementing the solver itself in a faster language could be an option if you prefer. C, for example, works quite nicely with Python.

# About IQ Circuit  
Again, the game is called "[IQ Circuit](https://www.smartgames.eu/uk/one-player-games/iq-circuit)" by "SmartGames". You can download the booklet from their [website](https://www.smartgames.eu/uk/one-player-games/iq-circuit#downloads).

Run game.py for a minimal simulated version of the game.

### Game Objective:  
Cover the entire playing field with pieces without any overlap.

### Piece Connections:  
Each piece features lines with specific entry and exit points (referred to as "IO" in the code). When placing a piece, every line must either connect directly to a line on an adjacent piece or end on the piece itself. In other words, there should be no loose or unconnected ends, regardless of how the lines are drawn — the focus is solely on their connection points. (Therefore, we don't draw them in the simulation.)

### Level Constraints:  
Each level designates specific locations for endpoints (known as "vertices" in the code). A piece can only be placed if one of its vertices aligns exactly with one of these predetermined endpoint positions. Moreover, if a piece covers any of these locations, it must include a matching vertex at that spot, ensuring all endpoints are properly connected.

Overall, the challenge is to strategically fill the playing field by aligning pieces correctly, ensuring all lines connect seamlessly, and adhering to the endpoint constraints specified by each level.

# Solver

### Solver1.py  
Implements a variation of a [backtracking](https://en.wikipedia.org/wiki/Backtracking) algorithm.

# Acknowledgements

- [SmartGames](https://www.smartgames.eu/uk/one-player-games/iq-circuit), obviously, for creating the game. If you enjoy problem-solving, there's a good chance you'd enjoy it too.
- [pygame](https://github.com/pygame/pygame) to emulate a rudimentary framework to display the steps it's taking.
