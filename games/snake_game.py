import random
import tkinter as tk


CELL_SIZE = 20
BOARD_WIDTH = 20
BOARD_HEIGHT = 20


def move_snake(snake, direction):
    """Return the snake position after moving one step."""
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    return [new_head] + snake[:-1]


def check_collision(snake, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    """Check whether the snake hit a wall or itself."""
    head_x, head_y = snake[0]
    if head_x <= 0 or head_x >= width - 1 or head_y <= 0 or head_y >= height - 1:
        return True
    if len(snake) != len(set(snake)):
        return True
    return False


class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake for Beginners")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bg="#111111",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.direction = (1, 0)
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.food = self._spawn_food()
        self.score = 0
        self.game_over = False

        self.root.bind("<Left>", self._set_direction)
        self.root.bind("<Right>", self._set_direction)
        self.root.bind("<Up>", self._set_direction)
        self.root.bind("<Down>", self._set_direction)

        self._draw_board()
        self.root.after(120, self._tick)

    def _spawn_food(self):
        while True:
            food = (
                random.randint(0, BOARD_WIDTH - 1),
                random.randint(0, BOARD_HEIGHT - 1),
            )
            if food not in self.snake:
                return food

    def _set_direction(self, event):
        if event.keysym == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif event.keysym == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif event.keysym == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif event.keysym == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)

    def _draw_board(self):
        self.canvas.delete("all")
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                self.canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    x * CELL_SIZE + CELL_SIZE,
                    y * CELL_SIZE + CELL_SIZE,
                    fill="#222222",
                    outline="#333333",
                )

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                x * CELL_SIZE + CELL_SIZE,
                y * CELL_SIZE + CELL_SIZE,
                fill="#4ade80",
                outline="#111111",
            )

        food_x, food_y = self.food
        self.canvas.create_rectangle(
            food_x * CELL_SIZE,
            food_y * CELL_SIZE,
            food_x * CELL_SIZE + CELL_SIZE,
            food_y * CELL_SIZE + CELL_SIZE,
            fill="#f87171",
            outline="#111111",
        )

        self.canvas.create_text(
            10,
            10,
            anchor="nw",
            text=f"Score: {self.score}",
            fill="white",
            font=("Helvetica", 12, "bold"),
        )

    def _tick(self):
        if self.game_over:
            return

        new_snake = move_snake(self.snake, self.direction)
        self.snake = new_snake

        if check_collision(self.snake):
            self.game_over = True
            self.canvas.create_text(
                BOARD_WIDTH * CELL_SIZE // 2,
                BOARD_HEIGHT * CELL_SIZE // 2,
                text="Game Over",
                fill="white",
                font=("Helvetica", 20, "bold"),
            )
            return

        if self.snake[0] == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])
            self.food = self._spawn_food()

        self._draw_board()
        self.root.after(120, self._tick)

    def run(self):
        self.root.mainloop()


def main():
    game = SnakeGame()
    game.run()
