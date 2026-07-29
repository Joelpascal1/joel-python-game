"""

Simple Snake Game using Python's built-in turtle module.



Controls:

    Arrow keys  -> Move the snake (Up, Down, Left, Right)

    Q           -> Quit the game



Goal:

    Eat the red food to grow longer and increase your score.

    Don't run into the walls or into your own body!

"""



import random

import time

import turtle



# ---------------------------------------------------------------------------

# Game configuration (tweak these values to experiment and learn!)

# ---------------------------------------------------------------------------

WIDTH = 800           # Width of the game window in pixels

HEIGHT = 800          # Height of the game window in pixels

SEGMENT_SIZE = 20     # Size of each snake segment / grid step in pixels

START_DELAY = 0.15    # Seconds between moves (smaller = faster snake)

BG_COLOR = "black"

SNAKE_COLOR = "green"

HEAD_COLOR = "lightgreen"

FOOD_COLOR = "red"

TEXT_COLOR = "white"





class SnakeGame:

    """Encapsulates all state and behavior for the Snake game."""



    def __init__(self):

        # --- Set up the screen -------------------------------------------

        self.screen = turtle.Screen()

        self.screen.bgcolor("black")

        self.screen.setup(width=WIDTH, height=HEIGHT)

        self.screen.title("Snake Game")
        try:
            self.screen._root.title("Snake Game")
        except AttributeError:
            pass

        self.screen.tracer(0)  # Turn off auto-updates; we update manually



        # --- Game state ---------------------------------------------------

        self.direction = "stop"

        self.score = 0

        self.high_score = 0

        self.delay = START_DELAY

        self.running = True



        # --- Create the snake head ---------------------------------------

        self.head = turtle.Turtle()

        self.head.shape("square")

        self.head.color(HEAD_COLOR)

        self.head.penup()

        self.head.goto(0, 0)



        # --- The body segments (list of turtles) -------------------------

        self.segments = []



        # --- Create the food ---------------------------------------------

        self.food = turtle.Turtle()

        self.food.shape("circle")

        self.food.color(FOOD_COLOR)

        self.food.penup()

        self.place_food()



        # --- Create the scoreboard ---------------------------------------

        self.pen = turtle.Turtle()

        self.pen.hideturtle()

        self.pen.penup()

        self.pen.color(TEXT_COLOR)

        self.pen.goto(0, HEIGHT // 2 - 40)

        self.update_scoreboard()



        # --- Keyboard bindings -------------------------------------------

        self.screen.listen()

        self.screen.onkeypress(self.go_up, "Up")

        self.screen.onkeypress(self.go_down, "Down")

        self.screen.onkeypress(self.go_left, "Left")

        self.screen.onkeypress(self.go_right, "Right")

        self.screen.onkeypress(self.quit_game, "q")



    # -- Direction handlers ----------------------------------------------

    # Prevent the snake from instantly reversing into itself.

    def go_up(self):

        if self.direction != "down":

            self.direction = "up"



    def go_down(self):

        if self.direction != "up":

            self.direction = "down"



    def go_left(self):

        if self.direction != "right":

            self.direction = "left"



    def go_right(self):

        if self.direction != "left":

            self.direction = "right"



    def quit_game(self):

        self.running = False



    # -- Core mechanics ---------------------------------------------------

    def move(self):

        """Move the head one step in the current direction."""

        x, y = self.head.xcor(), self.head.ycor()

        if self.direction == "up":

            self.head.sety(y + SEGMENT_SIZE)

        elif self.direction == "down":

            self.head.sety(y - SEGMENT_SIZE)

        elif self.direction == "left":

            self.head.setx(x - SEGMENT_SIZE)

        elif self.direction == "right":

            self.head.setx(x + SEGMENT_SIZE)



    def place_food(self):

        """Move the food to a random spot aligned to the grid."""

        max_x = (WIDTH // 2 - SEGMENT_SIZE) // SEGMENT_SIZE

        max_y = (HEIGHT // 2 - SEGMENT_SIZE) // SEGMENT_SIZE

        x = random.randint(-max_x, max_x) * SEGMENT_SIZE

        y = random.randint(-max_y, max_y) * SEGMENT_SIZE

        self.food.goto(x, y)



    def grow(self):

        """Add a new segment to the snake's body."""

        segment = turtle.Turtle()

        segment.shape("square")

        segment.color(SNAKE_COLOR)

        segment.penup()

        self.segments.append(segment)



    def move_body(self):

        """Move each body segment to the position of the one ahead of it."""

        for i in range(len(self.segments) - 1, 0, -1):

            x = self.segments[i - 1].xcor()

            y = self.segments[i - 1].ycor()

            self.segments[i].goto(x, y)

        # Move the first segment to where the head is.

        if self.segments:

            self.segments[0].goto(self.head.xcor(), self.head.ycor())



    def check_wall_collision(self):

        """Return True if the head has hit a wall."""

        half_w = WIDTH // 2 - SEGMENT_SIZE // 2

        half_h = HEIGHT // 2 - SEGMENT_SIZE // 2

        x, y = self.head.xcor(), self.head.ycor()

        return abs(x) > half_w or abs(y) > half_h



    def check_self_collision(self):

        """Return True if the head has hit one of its own body segments."""

        for segment in self.segments:

            if segment.distance(self.head) < SEGMENT_SIZE / 2:

                return True

        return False



    def check_food_collision(self):

        """Return True if the head is on top of the food."""

        return self.head.distance(self.food) < SEGMENT_SIZE



    def update_scoreboard(self):

        """Redraw the score and high score at the top of the screen."""

        self.pen.clear()

        self.pen.write(

            f"Score: {self.score}   High Score: {self.high_score}",

            align="center",

            font=("Courier", 20, "normal"),

        )



    def reset(self):

        """Reset the game after the snake dies."""

        time.sleep(1)

        self.head.goto(0, 0)

        self.direction = "stop"



        # Hide and clear all body segments.

        for segment in self.segments:

            segment.goto(1000, 1000)  # Move off-screen before deleting

        self.segments.clear()



        # Update the high score, then reset the current score.

        if self.score > self.high_score:

            self.high_score = self.score

        self.score = 0

        self.delay = START_DELAY

        self.update_scoreboard()



    # -- Main loop --------------------------------------------------------

    def run(self):

        """Run the main game loop until the player quits."""

        while self.running:

            self.screen.update()



            # Handle wall collisions.

            if self.check_wall_collision():

                self.reset()



            # Handle food collisions.

            if self.check_food_collision():

                self.place_food()

                self.grow()

                self.score += 10

                self.delay = max(0.05, self.delay - 0.001)  # Speed up slightly

                self.update_scoreboard()



            # Move the body first, then the head.

            self.move_body()

            self.move()



            # Handle self collisions (after moving).

            if self.check_self_collision():

                self.reset()



            time.sleep(self.delay)



        self.screen.bye()





def main():

    game = SnakeGame()

    game.run()





if __name__ == "__main__":

    main()