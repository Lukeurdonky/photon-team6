import tkinter


# ATTEMPTING to copy the programming style we learned from Paradigms
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True

class Model:
    def __init__(self):
        self.test = True

class View:
    def __init__(self, model):
        self.test = True



# This here-on acts sort of as "main" and the game loop
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

# def