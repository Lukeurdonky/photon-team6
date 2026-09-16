from PIL import Image, ImageTk
import tkinter as tk


# ATTEMPTING to copy the programming style we learned from Paradigms
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True

    def update():
        pass

# model may not expressly be needed because the database will be the backend.
class Model:
    def __init__(self):
        pass

    def update():
        pass

class View:
    def __init__(self, model):
        self.model = model

    def update():
        pass



# This here-on acts sort of as "main" and the game loop
root = tk.Tk()
m = Model()
v = View(m)
c = Controller(m, v)


def game_loop():
    c.update()
    m.update()
    v.update()

    # more reliable than sleep for tkinter (ALLEGEDLY)
    while c.keep_going:
        root.after(40, game_loop)

# starts the game loop
game_loop()