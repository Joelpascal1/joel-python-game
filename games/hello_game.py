import tkinter as tk


class BounceGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Game Starter")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="black")
        self.canvas.pack()

        self.x = 50
        self.y = 50
        self.dx = 3
        self.dy = 3
        self.size = 24

        self.ball = self.canvas.create_oval(
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
            fill="lightgreen",
            outline="white",
        )

        self.root.after(16, self.animate)

    def animate(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x + self.size >= 600:
            self.dx *= -1
        if self.y <= 0 or self.y + self.size >= 400:
            self.dy *= -1

        self.canvas.coords(self.ball, self.x, self.y, self.x + self.size, self.y + self.size)
        self.root.after(16, self.animate)

    def run(self):
        self.root.mainloop()


def main():
    game = BounceGame()
    game.run()
