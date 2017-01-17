# slithery
Terminal-based snake game
## Installation
Python 2 needs to be installed. (preferably 2.7 but other versions should work fine). It should include the built-in library `curses`.

- First clone the repo: `git clone https://github.com/greysome/slithery`
- Then `cd` into slithery and run the script with default configuration: `python main.py`
- Have fun! Use the default i,k,j and l keys to move.

## Configuration
There is an editable configuration file, `slithery.conf`, which stores the default settings. 
Other files may be used for configuration. 
To use those files instead, specify their name as the 2nd argument: `python main.py <filename>`

### boardsize
Sets the size of the game board.

- `boardsize=<length>x<width>` sets fixed dimensions. `length` and `width` must both be greater than 10 and even (for display purposes).

- `boardsize=MAX` fills up as much of the screen as possible.


### Displaying items
For all items, `char` must be exactly 1 character long.
- `displaysnake=<char>` (pretty self explanatory)
- `displayfood=<char>` (and so is this)
- `displayempty=<char>` sets the character for an empty spot (not occupied by the snake or any powerup)

### iterdelay
Sets the delay between each iteration of the game. In other words, the shorter the delay, the faster the snake moves.

- `iterdelay=<delay>`, `delay` should be a floating point number and it should be between 0.025 and 2 seconds

### quitkey
Sets the key which when pressed quits the game

- `quitkey=<key>`, `key` must be exactly 1 character long

### player1-keys
Sets the movement keys for the 1st player
- `player1keys=<keys>`, `keys` should consist of 4 characters separated by a comma. They should be in the order "up, down, left, right"
