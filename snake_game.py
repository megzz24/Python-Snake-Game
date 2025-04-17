import turtle
import time
import random
import os


def create_turtle(shape, color, position, hide=False):
    t = turtle.Turtle()
    t.speed(0)
    t.shape(shape)
    t.color(color)
    t.penup()
    t.goto(position)
    if hide:
        t.hideturtle()
    return t


def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)


def update_score():
    global score, high_score

    pen.clear()
    pen.write(
        f"Score: {score}  High Score: {high_score}",
        align="center",
        font=("Courier", 24, "normal"),
    )


def move_food():
    while True:
        x = random.randint(-290, 290)
        y = random.randint(-290, 250)

        collision = False
        if head.distance(x, y) < 20:
            collision = True
        for segment in segments:
            if segment.distance(x, y) < 20:
                collision = True
                break

        if not collision:
            food.goto(x, y)
            break


def reset_game():
    global score, delay

    save_highscore()

    food.hideturtle()
    head.hideturtle()
    for segment in segments:
        segment.hideturtle()

    pen.goto(0, 0)
    pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
    screen.update()
    time.sleep(1)
    pen.clear()
    pen.goto(0, 260)

    head.goto(0, 0)
    head.direction = "stop"
    head.showturtle()
    food.showturtle()
    delay = 0.3

    segments.clear()
    score = 0

    update_score()
    move_food()


def load_highscore():
    if not os.path.exists("highscore.txt"):
        return 0
    with open("highscore.txt", "r") as f:
        return int(f.read())


def save_highscore():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))


screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

head = create_turtle("square", "grey", (0, 0))
head.direction = "stop"

food = create_turtle("circle", "red", (0, 100))

segments = []

score = 0
high_score = load_highscore()
delay = 0.25

pen = create_turtle("square", "white", (0, 260), hide=True)
update_score()

move_food()

while True:
    screen.update()

    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        reset_game()

    if head.distance(food) < 20:
        move_food()

        new_segment = create_turtle("square", "white", (head.xcor(), head.ycor()))
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score

        if score % 30 == 0:
            delay = max(0.05, delay - 0.02)

        update_score()

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)
