import time
import turtle

# Game window configuration
WIDTH = 900
HEIGHT = 600
PADDLE_SPEED = 30
BALL_SPEED_X = 0.25
BALL_SPEED_Y = 0.25


def make_paddle(x, y):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


def make_ball():
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = BALL_SPEED_X
    ball.dy = BALL_SPEED_Y
    return ball


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

    screen = turtle.Screen()
    screen.title("Ping Pong")
    screen.bgcolor("black")
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.tracer(0)

    paddle_a = make_paddle(-WIDTH // 2 + 40, 0)
    paddle_b = make_paddle(WIDTH // 2 - 40, 0)
    ball = make_ball()
    scoreboard = make_scoreboard()

    score_a = 0
    score_b = 0

    screen.listen()
    screen.onkeypress(paddle_a_up, "w")
    screen.onkeypress(paddle_a_down, "s")
    screen.onkeypress(paddle_b_up, "Up")
    screen.onkeypress(paddle_b_down, "Down")
    screen.onkeypress(screen.bye, "q")

    while True:
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
            ball.goto(0, 0)
            ball.dx *= -1

        if ball.xcor() < -WIDTH // 2 + 10:
            score_b += 1
            update_scoreboard(scoreboard, score_a, score_b)
            ball.goto(0, 0)
            ball.dx *= -1

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

        time.sleep(0.01)


if __name__ == "__main__":
    main()
