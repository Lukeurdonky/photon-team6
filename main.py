from PIL import Image, ImageTk
import tkinter as tk
import socket
import time
import random
import threading

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

class UDPSocket():
    def __init__(
        self,
        #Receive init
        rc_host = "0.0.0.0",
        rc_port = 7501,
        buffer_size = 4096,
        #Transmit init
        source_ip = "127.0.0.1",
        tr_port = 7500,
        broadcast_ip = "127.0.0.255",
        message = "UDP TEST" #change later
        ):
        self.rc_host = rc_host
        self.rc_port = rc_port
        self.buffer_size = buffer_size

        self.source_ip = source_ip
        self.tr_port = tr_port
        self.broadcast_ip = broadcast_ip
        self.message = message

        # Receive socket
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_sock.bind((self.rc_host, self.rc_port))
        self.recv_sock.settimeout(0.5)

        # Transmit socket
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.running = False

    # loop for receiving transmissions
    def _receive_loop(self):
        print(f"Listening for UDP on {self.rc_host}:{self.rc_port}...")
        while self.running:
            try:
                data, addr = self.recv_sock.recvfrom(self.buffer_size)
                print(f"From {addr}: {data.decode(errors='ignore')}")
            except KeyboardInterrupt:
                print("\nShutting down.")
                break
            except socket.timeout:
                continue
            except OSError:
                break

    # loop for sending transmissions
    def _send_loop(self):
        print(f"Broadcasting from {self.source_ip} to {self.broadcast_ip}:{self.tr_port}")
        while self.running:
            self.send_sock.sendto(self.message.encode(), (self.broadcast_ip, self.tr_port))
            print("Sent:", self.message)
            time.sleep(1)

    # simultaneously starts sending and receiving via threading
    def start(self):
        self.running = True

        self.recv_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.send_thread = threading.Thread(target=self._send_loop, daemon=True)
        self.recv_thread.start()
        self.send_thread.start()

    # sends a single message, or at least it should.
    def send(self, message):
        self.send_sock.sendto(message.encode(), (self.broadcast_ip, self.tr_port))

    # stops running the UDP
    def stop(self):
        self.running = False
        try:
            self.recv_sock.close()
        except Exception:
            pass

        try:
            self.send_sock.close()
        except Exception:
            pass

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

####   UDP TEST
udp = UDPSocket()
udp.start()

# send a custom message
udp.send("PLAYER_HIT:123")

# stop it later
udp.stop()
################

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