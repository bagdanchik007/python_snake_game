from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF00FF"
BACKGROUND_COLOR = "#000000"

START_SPEED = 150
MIN_SPEED = 50


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y,
                x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_oval(
            x, y,
            x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )


def next_turn():

    global score, speed, food

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y,
        x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    #  Essen
    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1
        label.config(text="Score: {}".format(score))

        canvas.delete("food")
        food = Food()

        # Schwierigkeit erhöhen
        if speed > MIN_SPEED:
            speed -= 5

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions():
        game_over()
    else:
        window.after(speed, next_turn)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions():

    x, y = snake.coordinates[0]

    # Wand
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    # Selbst
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=('consolas', 60),
        text="GAME OVER",
        fill="red"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 60,
        font=('consolas', 20),
        text="Press R to Restart",
        fill="white"
    )


def restart_game(event=None):
    global snake, food, score, direction, speed

    canvas.delete(ALL)

    score = 0
    speed = START_SPEED
    direction = "down"

    label.config(text="Score: 0")

    snake = Snake()
    food = Food()

    next_turn()


# ---------------- WINDOW ----------------

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"
speed = START_SPEED

label = Label(window, text="Score: 0", font=('consolas', 40))
label.pack()

canvas = Canvas(window,
                bg=BACKGROUND_COLOR,
                height=GAME_HEIGHT,
                width=GAME_WIDTH)
canvas.pack()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<r>', restart_game)
window.bind('<R>', restart_game)

snake = Snake()
food = Food()

next_turn()

window.mainloop()