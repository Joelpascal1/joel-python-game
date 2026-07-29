# 🐍 Snake Game



A simple Snake game built with Python's built-in `turtle` module — no external

dependencies required. Great for learning Python and building your own features!



## Requirements



- Python 3.7+ (the `turtle` module ships with Python, so nothing to install)



> On macOS, `turtle` uses Tkinter. If you get a `ModuleNotFoundError: No module

> named '_tkinter'`, install Python with Tk support (e.g. `brew install

> python-tk`).



## How to Play



Run the game from the project folder:



```bash

python3 snake_game.py

```



### Controls



| Key         | Action          |

| ----------- | --------------- |

| Arrow Up    | Move up         |

| Arrow Down  | Move down       |

| Arrow Left  | Move left       |

| Arrow Right | Move right      |

| Q           | Quit the game   |



### Goal



Eat the red food to grow longer and score points. Avoid running into the walls

or into your own tail!



## Ideas to Build Upon (Learn Python!)



The code lives in [snake_game.py](snake_game.py) and is organized in a

`SnakeGame` class with clear methods. Here are some fun things to try:



1. **Change the colors and speed** — tweak the constants at the top of the file.

2. **Add sound effects** when eating food (try the `winsound` or `playsound` module).

3. **Add a pause key** that freezes the game.

4. **Save the high score to a file** so it persists between runs.

5. **Add obstacles or walls** the snake must avoid.

6. **Add a "wrap around" mode** where the snake exits one side and appears on the other.

7. **Add multiple food types** worth different points.



Have fun! 🎮


## Ping Pong Game


A simple two-player Ping Pong game built with Python's built-in `turtle` module.


### Run

From the project folder run:

```bash
python3 ping_pong.py
```


### Controls

| Key | Action |
| ---- | ------ |
| `w` | Player A paddle up |
| `s` | Player A paddle down |
| Arrow Up | Player B paddle up |
| Arrow Down | Player B paddle down |
| `q` | Quit the game |


### Notes

- Uses the same requirements as the Snake game (Python 3.7+ and `turtle`).
- Scores are displayed at the top of the window and update live.
