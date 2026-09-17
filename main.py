from PIL import Image, ImageTk
import tkinter as tk

# Luca's attempt at a splash screen
class SplashScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        logo = Image.open("logo.jpg").convert("RGBA")
        logo.thumbnail((800, 600))
        black_bg = Image.new("RGBA", logo.size, (0, 0, 0, 255))

        # Pre-render the fade-in sequence once; fade-out just plays it backwards
        steps = 15
        self.frames = [
            ImageTk.PhotoImage(Image.blend(black_bg, logo, i / steps))
            for i in range(steps + 1)
        ]

        self.label = tk.Label(self, bg="black")
        self.label.pack(expand=True)
        self.index = 0
        self.direction = 1

    # starts the animation
    def on_show(self):
        self.index, self.direction = 0, 1
        self.animate()

    def animate(self):
        self.label.configure(image=self.frames[self.index])
        if self.direction == 1 and self.index < len(self.frames) - 1:
            self.index += 1
            self.after(30, self.animate)
        elif self.direction == 1:
            self.after(2000, self.start_fade_out)  # hold fully visible
        elif self.index > 0:
            self.index -= 1
            self.after(30, self.animate)
        else:
            # will eventually render the next screen
            self.controller.show_player_screen()

    # the fade out
    def start_fade_out(self):
        self.direction = -1
        self.animate()

# ATTEMPTING to copy the programming style we learned from Paradigms
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.keep_going = True

    def update(self):
        pass

    # eventually show player screen
    def show_player_screen(self):
        pass

    # eventually show game screen
    def show_game_screen(self):
        pass

# model may not expressly be needed because the database will be the backend.
class Model:
    def __init__(self):
        pass

    def update(self):
        pass

class View:
    def __init__(self, model):
        self.model = model

    def update(self):
        pass



# between here and game_loop acts as "main" (only called once)
root = tk.Tk()
# set window size
root.geometry("800x600")
m = Model()
v = View(m)
c = Controller(m, v)
splashScreen = SplashScreen(root, c)
# this makes the splash screen render
splashScreen.pack(fill="both", expand=True)
splashScreen.on_show()

# this is called every 40ms
def game_loop():
    c.update()
    m.update()
    v.update()

    # more reliable than sleep for tkinter (ALLEGEDLY)
    if c.keep_going:
        root.after(40, game_loop)

# starts the game loop
game_loop()
# listens for root.after to make the loop work
root.mainloop()