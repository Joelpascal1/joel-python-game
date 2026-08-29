import random
import time
import turtle

WIDTH = 900
HEIGHT = 600
PADDLE_SPEED = 55
PUCK_SPEED = 3.5
GOAL_LIMIT = 5
GOAL_OPENING_MARGIN = 150


def make_paddle(x, y, color):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(stretch_wid=5, stretch_len=1)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


def make_puck():
    puck = turtle.Turtle()
    puck.speed(0)
    puck.shape("circle")
    puck.color("white")
    puck.penup()
    puck.goto(0, 0)
    puck.dx = 0
    puck.dy = 0
    return puck


def draw_field():
    border = turtle.Turtle()
    border.hideturtle()
    border.speed(0)
    border.color("white")
    border.penup()
    border.goto(-WIDTH // 2, -HEIGHT // 2)
    border.pendown()
    border.setheading(0)
    border.forward(WIDTH)
    border.setheading(90)
    border.forward(HEIGHT)
    border.setheading(180)
    border.forward(WIDTH)
    border.setheading(270)
    border.forward(HEIGHT)

    line = turtle.Turtle()
    line.hideturtle()
    line.speed(0)
    line.color("white")
    line.penup()
    line.goto(0, -HEIGHT // 2)
    line.pendown()
    line.setheading(90)
    line.forward(HEIGHT)

    goal_top = HEIGHT // 2 - GOAL_OPENING_MARGIN
    goal_bottom = -HEIGHT // 2 + GOAL_OPENING_MARGIN

    left_goal = turtle.Turtle()
    left_goal.hideturtle()
    left_goal.speed(0)
    left_goal.color("blue")
    left_goal.penup()
    left_goal.goto(-WIDTH // 2, goal_bottom)
    left_goal.pendown()
    left_goal.setheading(0)
    left_goal.forward(20)
    left_goal.setheading(90)
    left_goal.forward(goal_top - goal_bottom)
    left_goal.setheading(180)
    left_goal.forward(20)
    left_goal.setheading(270)
    left_goal.forward(goal_top - goal_bottom)

    right_goal = turtle.Turtle()
    right_goal.hideturtle()
    right_goal.speed(0)
    right_goal.color("red")
    right_goal.penup()
    right_goal.goto(WIDTH // 2 - 20, goal_bottom)
    right_goal.pendown()
    right_goal.setheading(0)
    right_goal.forward(20)
    right_goal.setheading(90)
    right_goal.forward(goal_top - goal_bottom)
    right_goal.setheading(180)
    right_goal.forward(20)
    right_goal.setheading(270)
    right_goal.forward(goal_top - goal_bottom)


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


def reset_puck(puck):
    puck.goto(0, 0)
    puck.dx = random.choice([-1, 1]) * PUCK_SPEED
    puck.dy = random.choice([-1, 1]) * PUCK_SPEED


def start_countdown(screen, seconds):
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color("yellow")
    pen.goto(0, 0)

    for count in range(seconds, 0, -1):
        pen.clear()
        pen.write(str(count), align="center", font=("Courier", 42, "bold"))
        screen.update()
        time.sleep(1)

    pen.clear()
    pen.write("Go!", align="center", font=("Courier", 36, "bold"))
    screen.update()
    time.sleep(0.6)
    pen.clear()


def paddle_a_up():
    y = paddle_a.ycor()
    y += PADDLE_SPEED
    if y > HEIGHT // 2 - 60:
        y = HEIGHT // 2 - 60
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= PADDLE_SPEED
    if y < -HEIGHT // 2 + 60:
        y = -HEIGHT // 2 + 60
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += PADDLE_SPEED
    if y > HEIGHT // 2 - 60:
        y = HEIGHT // 2 - 60
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= PADDLE_SPEED
    if y < -HEIGHT // 2 + 60:
        y = -HEIGHT // 2 + 60
    paddle_b.sety(y)


def main():
    global paddle_a, paddle_b

    screen = turtle.Screen()
    screen.title("Air Hockey")
    screen.bgcolor("black")
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.tracer(0)

    draw_field()

    paddle_a = make_paddle(-WIDTH // 2 + 50, 0, "darkblue")
    paddle_b = make_paddle(WIDTH // 2 - 50, 0, "darkred")
    puck = make_puck()
    scoreboard = make_scoreboard()

    start_pen = turtle.Turtle()
    start_pen.hideturtle()
    start_pen.penup()
    start_pen.color("yellow")
    start_pen.goto(0, 0)
    start_pen.write("Click or press Enter key", align="center", font=("Courier", 22, "bold"))

    started = {"flag": False}

    def _on_start(x, y):
        started["flag"] = True
        start_pen.clear()
        screen.onclick(None)

    screen.onkey(lambda: (_on_start(0, 0),), "Return")
    screen.listen()
    screen.onclick(_on_start)
    while not started["flag"]:
        screen.update()
        time.sleep(0.05)

    start_countdown(screen, 5)

    reset_puck(puck)
    score_a = 0
    score_b = 0
    update_scoreboard(scoreboard, score_a, score_b)

    screen.listen()
    screen.onkeypress(paddle_a_up, "w")
    screen.onkeypress(paddle_a_down, "s")
    screen.onkeypress(paddle_b_up, "Up")
    screen.onkeypress(paddle_b_down, "Down")
    screen.onkeypress(lambda: screen.bye(), "q")

    while True:
        screen.update()

        puck.setx(puck.xcor() + puck.dx)
        puck.sety(puck.ycor() + puck.dy)

        if puck.ycor() > HEIGHT // 2 - 10:
            puck.sety(HEIGHT // 2 - 10)
            puck.dy *= -1

        if puck.ycor() < -HEIGHT // 2 + 10:
            puck.sety(-HEIGHT // 2 + 10)
            puck.dy *= -1

        paddle_radius = 18

        if (
            puck.xcor() > paddle_b.xcor() - paddle_radius
            and puck.xcor() < paddle_b.xcor() + paddle_radius
            and puck.ycor() < paddle_b.ycor() + paddle_radius
            and puck.ycor() > paddle_b.ycor() - paddle_radius
        ):
            puck.setx(paddle_b.xcor() - paddle_radius)
            puck.dx *= -1
            puck.dx *= 1.04
            puck.dy *= 1.02

        if (
            puck.xcor() < paddle_a.xcor() + paddle_radius
            and puck.xcor() > paddle_a.xcor() - paddle_radius
            and puck.ycor() < paddle_a.ycor() + paddle_radius
            and puck.ycor() > paddle_a.ycor() - paddle_radius
        ):
            puck.setx(paddle_a.xcor() + paddle_radius)
            puck.dx *= -1
            puck.dx *= 1.04
            puck.dy *= 1.02

        left_goal_top = HEIGHT // 2 - GOAL_OPENING_MARGIN
        left_goal_bottom = -HEIGHT // 2 + GOAL_OPENING_MARGIN

        if puck.xcor() > WIDTH // 2 - 10:
            if left_goal_bottom <= puck.ycor() <= left_goal_top:
                score_a += 1
                update_scoreboard(scoreboard, score_a, score_b)
                if score_a >= GOAL_LIMIT:
                    winner = turtle.Turtle()
                    winner.hideturtle()
                    winner.penup()
                    winner.color("blue")
                    winner.goto(0, 0)
                    winner.write("Player A wins!", align="center", font=("Courier", 36, "bold"))
                    screen.update()
                    time.sleep(3)
                    screen.bye()
                    return
                start_countdown(screen, 3)
                reset_puck(puck)
            else:
                puck.setx(WIDTH // 2 - 10)
                puck.dx *= -1

        if puck.xcor() < -WIDTH // 2 + 10:
            if left_goal_bottom <= puck.ycor() <= left_goal_top:
                score_b += 1
                update_scoreboard(scoreboard, score_a, score_b)
                if score_b >= GOAL_LIMIT:
                    winner = turtle.Turtle()
                    winner.hideturtle()
                    winner.penup()
                    winner.color("red")
                    winner.goto(0, 0)
                    winner.write("Player B wins!", align="center", font=("Courier", 36, "bold"))
                    screen.update()
                    time.sleep(3)
                    screen.bye()
                    return
                start_countdown(screen, 3)
                reset_puck(puck)
            else:
                puck.setx(-WIDTH // 2 + 10)
                puck.dx *= -1

        time.sleep(0.01)


if __name__ == "__main__":
    main()
