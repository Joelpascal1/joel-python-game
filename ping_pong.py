import time
import turtle
import random

# Game window configuration
WIDTH = 900
HEIGHT = 600
PADDLE_SPEED = 40
# Base ball speed (increased for a faster default; multiplied by chosen difficulty)
BASE_BALL_SPEED = 1.8


def make_paddle(x, y):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


def make_ball(speed):
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    # Start stationary; direction assigned after countdown
    ball.dx = 0
    ball.dy = 0
    # store base speed for later assignment
    ball._base_speed = speed
    return ball


def pre_game_countdown(screen, seconds=3):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color("yellow")
    pen.goto(0, 0)
    for s in range(seconds, 0, -1):
        pen.clear()
        pen.write(str(s), align="center", font=("Courier", 48, "bold"))
        screen.update()
        time.sleep(1)
    pen.clear()
    pen.write("Go!", align="center", font=("Courier", 40, "bold"))
    screen.update()
    time.sleep(0.5)
    pen.clear()


def choose_speed():
    """Prompt the player to choose a speed level before the game starts.

    Levels: 1 (slow) .. 5 (fast). Returns a multiplier applied to the base speed.
    """
    print("Choose ball speed level 1-5 (1=slowest, 5=fastest). Default is 3.")
    try:
        raw = input("Speed level [1-5] (default 3): ")
        level = int(raw) if raw.strip() else 3
    except Exception:
        level = 3
    level = max(1, min(5, level))
    # Faster multipliers so even level 1 feels brisk and level 5 is challenging
    multipliers = {1: 1.0, 2: 1.25, 3: 1.5, 4: 1.9, 5: 2.5}
    mult = multipliers.get(level, 1.0)
    print(f"Starting with speed level {level} (x{mult})")
    return mult


def choose_score_limit():
    """Prompt for a score limit (default 10). Returns an int >= 1."""
    print("Set score limit to win the game (default 10).")
    try:
        raw = input("Score limit (default 10): ")
        limit = int(raw) if raw.strip() else 10
    except Exception:
        limit = 10
    if limit < 1:
        limit = 10
    print(f"First to {limit} wins.")
    return limit


def make_scoreboard():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, HEIGHT // 2 - 40)
    pen.write("Player A: 0    Player B: 0", align="center", font=("Courier", 24, "normal"))
    return pen


def update_scoreboard(pen, score_a, score_b):
    pen.clear()
    pen.write(
        f"Player A: {score_a}    Player B: {score_b}",
        align="center",
        font=("Courier", 24, "normal"),
    )


def paddle_a_up():
    y = paddle_a.ycor()
    y += PADDLE_SPEED
    if y > HEIGHT // 2 - 50:
        y = HEIGHT // 2 - 50
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= PADDLE_SPEED
    if y < -HEIGHT // 2 + 50:
        y = -HEIGHT // 2 + 50
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += PADDLE_SPEED
    if y > HEIGHT // 2 - 50:
        y = HEIGHT // 2 - 50
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= PADDLE_SPEED
    if y < -HEIGHT // 2 + 50:
        y = -HEIGHT // 2 + 50
    paddle_b.sety(y)


def main():
    global paddle_a, paddle_b

    # Ask the player which speed level and score limit to use before opening
    # the window
    speed_mult = choose_speed()
    score_limit = choose_score_limit()

    screen = turtle.Screen()
    screen.title("Ping Pong")
    screen.bgcolor("black")
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.tracer(0)

    paddle_a = make_paddle(-WIDTH // 2 + 40, 0)
    paddle_b = make_paddle(WIDTH // 2 - 40, 0)
    ball = make_ball(BASE_BALL_SPEED * speed_mult)
    scoreboard = make_scoreboard()

    # Create a visible "Click to Start" prompt and wait for user click
    started = {"flag": False}
    start_pen = turtle.Turtle()
    start_pen.hideturtle()
    start_pen.penup()
    start_pen.color("yellow")
    start_pen.goto(0, 0)
    start_pen.write("Click to Start", align="center", font=("Courier", 32, "bold"))

    def _on_start(x, y):
        started["flag"] = True
        start_pen.clear()
        # unregister click handler so further clicks don't restart
        screen.onclick(None)

    screen.onclick(_on_start)
    # Wait until user clicks to start
    while not started["flag"]:
        screen.update()
        time.sleep(0.05)

    # Countdown before start so players can get ready
    pre_game_countdown(screen, seconds=3)

    # Randomize initial direction (left/right and up/down)
    base = getattr(ball, "_base_speed", BASE_BALL_SPEED * speed_mult)
    ball.dx = base * random.choice([-1, 1])
    ball.dy = base * random.choice([-1, 1])

    score_a = 0
    score_b = 0

    # Allow quitting at any time using 'q'
    running = {"flag": True}

    def quit_game():
        running["flag"] = False
        try:
            screen.bye()
        except Exception:
            pass

    screen.listen()
    screen.onkeypress(paddle_a_up, "w")
    screen.onkeypress(paddle_a_down, "s")
    screen.onkeypress(paddle_b_up, "Up")
    screen.onkeypress(paddle_b_down, "Down")
    screen.onkeypress(quit_game, "q")

    while running["flag"]:
        screen.update()

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Top and bottom border collisions
        if ball.ycor() > HEIGHT // 2 - 10:
            ball.sety(HEIGHT // 2 - 10)
            ball.dy *= -1

        if ball.ycor() < -HEIGHT // 2 + 10:
            ball.sety(-HEIGHT // 2 + 10)
            ball.dy *= -1

        # Left and right border collisions
        if ball.xcor() > WIDTH // 2 - 10:
            score_a += 1
            update_scoreboard(scoreboard, score_a, score_b)
            if score_a >= score_limit:
                winner_pen = turtle.Turtle()
                winner_pen.hideturtle()
                winner_pen.color("yellow")
                winner_pen.penup()
                winner_pen.goto(0, 0)
                winner_pen.write("Player A wins!", align="center", font=("Courier", 36, "bold"))
                screen.update()
                time.sleep(3)
                try:
                    screen.bye()
                except Exception:
                    pass
                return
            # Reset ball and countdown before resuming
            ball.goto(0, 0)
            ball.dx = 0
            ball.dy = 0
            pre_game_countdown(screen, seconds=3)
            base = getattr(ball, "_base_speed", BASE_BALL_SPEED * speed_mult)
            ball.dx = base * random.choice([-1, 1])
            ball.dy = base * random.choice([-1, 1])

        if ball.xcor() < -WIDTH // 2 + 10:
            score_b += 1
            update_scoreboard(scoreboard, score_a, score_b)
            if score_b >= score_limit:
                winner_pen = turtle.Turtle()
                winner_pen.hideturtle()
                winner_pen.color("yellow")
                winner_pen.penup()
                winner_pen.goto(0, 0)
                winner_pen.write("Player B wins!", align="center", font=("Courier", 36, "bold"))
                screen.update()
                time.sleep(3)
                try:
                    screen.bye()
                except Exception:
                    pass
                return
            # Reset ball and countdown before resuming
            ball.goto(0, 0)
            ball.dx = 0
            ball.dy = 0
            pre_game_countdown(screen, seconds=3)
            base = getattr(ball, "_base_speed", BASE_BALL_SPEED * speed_mult)
            ball.dx = base * random.choice([-1, 1])
            ball.dy = base * random.choice([-1, 1])

        # Paddle collisions
        if (
            ball.xcor() > WIDTH // 2 - 60
            and ball.xcor() < WIDTH // 2 - 40
            and ball.ycor() < paddle_b.ycor() + 50
            and ball.ycor() > paddle_b.ycor() - 50
        ):
            ball.setx(WIDTH // 2 - 60)
            ball.dx *= -1

        if (
            ball.xcor() < -WIDTH // 2 + 60
            and ball.xcor() > -WIDTH // 2 + 40
            and ball.ycor() < paddle_a.ycor() + 50
            and ball.ycor() > paddle_a.ycor() - 50
        ):
            ball.setx(-WIDTH // 2 + 60)
            ball.dx *= -1

        # Lower sleep for smoother and faster motion
        time.sleep(0.004)


if __name__ == "__main__":
    main()
