# Import necessary libraries and modules
from PIL import Image, ImageTk
import tkinter as tk
import socket
import time
import random
import threading
import ipaddress

# Constant values for the player entry screen
MAX_PLAYERS = 15
DEFAULT_NETWORK = "127.0.0.1"

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

# Player entry screen
class PlayerEntryScreen(tk.Frame):
    def __init__(self, parent, controller, udp):
        super().__init__(parent, bg = "#0B0712")

        self.controller = controller
        self.udp = udp

        # Current network being used
        self.selected_network = DEFAULT_NETWORK

        # Main heading
        tk.Label(self, text = "EDIT CURRENT GAME", bg = "black", fg = "#5CE1E6", font = ("Arial", 20, "bold")
        ).pack(pady = 15)

        # Subheading
        tk.Label(self, text = "PHOTON LASER TAG SYSTEM", bg = "black", fg = "#5CE1E6", font = ("Arial", 12)
        ).pack(pady = 15)

        # Frame to hold both teams
        teams_frame = tk.Frame(self, bg = "black")
        teams_frame.pack()

        # Create red team panel
        red_frame, self.red_rows = self.build_team_panel(teams_frame, "RED TEAM", "#B22222")
        red_frame.grid(row = 0, column = 0, padx = 15)

        # Create green team panel
        green_frame, self.green_rows = self.build_team_panel(teams_frame, "GREEN TEAM", "#228B22")
        green_frame.grid(row = 0, column = 1, padx = 15)

        # Frame for network selection
        network_frame = tk.Frame(self, bg = "black")
        network_frame.pack(pady = 20)

        # Network address label
        tk.Label(network_frame, text = "Network Address:", bg = "black", fg = "white"
        ).grid(row = 0, column = 0, padx = 5)

        # Network address entry box
        self.network_entry = tk.Entry(network_frame, bg = "#2A1633", fg = "#F7F4F6", insertbackground = "#F7F4F6", width = 20)
        self.network_entry.grid(row = 0, column = 1, padx = 5)

        # Set localhost as the default network
        self.network_entry.insert(0, DEFAULT_NETWORK)

        # Button to apply a different network
        tk.Button(network_frame, text = "Apply", command = self.apply_network
        ).grid(row = 0, column = 2, padx = 5)

        # Frame for game controls
        controls_frame = tk.Frame(self, bg = "#0B0712")
        controls_frame.pack(pady = 5)

        # Button to start the game
        tk.Button(controls_frame, text = "F5 - START GAME", command = self.start_game
        ).grid(row = 0, column = 0, padx = 5)

        # Button to clear all player entries
        tk.Button(controls_frame, text = "F12 - CLEAR GAME", command = self.clear_game
        ).grid(row = 0, column = 1, padx = 5)

        # Status message at the bottom
        self.status_label = tk.Label(self, text = "SYSTEM READY", bg = "black", fg = "#5CE1E6")
        self.status_label.pack()

    # Function to create a team panel with player rows
    def build_team_panel(self, parent, team_name, team_color):
        # Create a frame for the team panel
        frame = tk.Frame(parent, bg = team_color, padx = 10, pady = 10)

        # List to store the entry boxes for each player
        player_rows = []

        # Team title
        tk.Label(frame, text = team_name, bg = team_color, fg = "#FAF8F6", font = ("Terminal", 18, "bold")
        ).grid(row = 0, column = 0, columnspan = 4, pady = 5)

        # Column titles
        tk.Label(frame, text = "#", bg = team_color, fg = "#FAF8F6"
        ).grid(row = 1, column = 0)

        tk.Label(frame, text = "Player ID", bg = team_color, fg = "#FAF8F6"
        ).grid(row = 1, column = 1)

        tk.Label(frame, text = "Codename", bg = team_color, fg = "#FAF8F6"
        ).grid(row = 1, column = 2)

        tk.Label(frame, text = "Equipment ID", bg = team_color, fg = "#FAF8F6"
        ).grid(row = 1, column = 3)

        # Create 15 player rows
        for i in range(MAX_PLAYERS):
            row_number = i + 1

            # Player number
            tk.Label(frame, text = str(row_number), bg = team_color, fg = "#FAF8F6"
            ).grid(row = i + 2, column = 0, padx = 5, pady = 2)

            # Player ID entry box
            player_id_entry = tk.Entry(frame, bg = "#2A1633", fg = "#F7F4F6", insertbackground = "#F7F4F6", width = 10)
            player_id_entry.grid(row = i + 2, column = 1, padx = 2, pady = 2)

            # Codename entry box
            codename_entry = tk.Entry(frame, bg = "#2A1633", fg = "#F7F4F6", insertbackground = "#F7F4F6", width = 16)
            codename_entry.grid(row = i + 2, column = 2, padx = 2, pady = 2)

            # Equipment ID entry box
            equipment_id_entry = tk.Entry(frame, bg = "#2A1633", fg = "#F7F4F6", insertbackground = "#F7F4F6", width = 10)
            equipment_id_entry.grid(row = i + 2, column = 3, padx = 2, pady = 2)

            # Store the entry boxes for the player
            player_rows.append({"player_id": player_id_entry, "codename": codename_entry, "equipment_id": equipment_id_entry})

        return frame, player_rows

    # Function for changing the network address
    def apply_network(self):
        address = self.network_entry.get().strip()

        # Make sure an address was entered
        if address == "":
            self.status_label.config(text = "Please enter a network address.")
            return

        # Make sure the network address is valid
        try:
            ipaddress.ip_address(address)
        except ValueError:
            self.status_label.config(text = "Please enter a valid IPv4 or IPv6 address.")
            return

        # Store the selected network
        self.selected_network = address

        # Update the status message
        self.status_label.config(text = "Selected network: " + address)

        # Print selected network for testing
        print("Selected UDP network:", self.selected_network)

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
