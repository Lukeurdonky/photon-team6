# Import the Tkinter library and the ipaddress module
import tkinter as tk
import ipaddress

# Constant values for the application
MAX_PLAYERS = 15
DEFAULT_NETWORK = "127.0.0.1"

# Current network being used
selected_networkg = DEFAULT_NETWORK

# Function to create a team panel with player rows
def build_team_panel(parent, team_name, team_color):
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
def apply_network():
    global selected_network

    address = network_entry.get().strip()

    # Make sure an address was entered
    if address == "":
        status_label.config(text = "Please enter a network address.")
        return

    # Make sure the network address is valid
    try:
        ipaddress.ip_address(address)
    except ValueError:
        status_label.config(text = "Please enter a valid IPv4 or IPv6 address.")
        return

    # Store the selected network
    selected_network = address

    # Update the status message
    status_label.config(text = "Selected network: " + address)

    # Print selected network for testing
    print("Selected UDP network:", selected_network)

# Function for clearing all player entries
def clear_game(event = None):
    # Go through every player row on both teams
    for row in red_rows + green_rows:
        # Clear the player ID entry box
        row["player_id"].delete(0, tk.END)

        # Clear the codename entry box
        row["codename"].delete(0, tk.END)

        # Clear the equipment ID entry box
        row["equipment_id"].delete(0, tk.END)

    # Update the status message
    status_label.config(text = "GAME CLEARED")

    # Return the cursor to the first player ID box
    red_rows[0]["player_id"].focus_set()

# Function for getting player information from a team
def get_players(player_rows, team_name):
    players = []

    # Go through every player row
    for row in player_rows:
        player_id = row["player_id"].get().strip()
        codename = row["codename"].get().strip()
        equipment_id = row["equipment_id"].get().strip()

        # Ignore rows that are completely empty
        if player_id == "" and codename == "" and equipment_id == "":
            continue

        # Make sure partially filled rows are completed
        if player_id == "" or codename == "" or equipment_id == "":
            status_label.config(text = "Please complete all fields for " + team_name + ".")
            return None

        # Make sure player ID is an integer
        if not player_id.isdigit():
            status_label.config(text = "Player ID must be an integer.")
            return None

        # Make sure equipment ID is an integer
        if not equipment_id.isdigit():
            status_label.config(text = "Equipment ID must be an integer.")
            return None

        # Store the player information
        players.append({"player_id": int(player_id), "codename": codename, "equipment_id": int(equipment_id), "team": team_name})

    return players

# Function for checking duplicate player and equipment IDs
def check_duplicates(red_players, green_players):
    all_players = red_players + green_players

    player_ids = set()
    equipment_ids = set()

    # Go through all players on both teams
    for player in all_players:
        player_id = player["player_id"]
        equipment_id = player["equipment_id"]

        # Check for duplicate player IDs
        if player_id in player_ids:
            status_label.config(text = "Player IDs cannot be duplicated.")
            return False

        player_ids.add(player_id)

        # Check for duplicate equipment IDs
        if equipment_id in equipment_ids:
            status_label.config(text = "Equipment IDs cannot be duplicated.")
            return False

        equipment_ids.add(equipment_id)

    return True

# Create the main window
root = tk.Tk()

# Function for starting the game
def start_game(event = None):
    # Get players from both teams
    red_players = get_players(red_rows, "RED TEAM")
    green_players = get_players(green_rows, "GREEN TEAM")

    # Stop if there was an error
    if red_players is None or green_players is None:
        return

    # Make sure at least one player was entered
    if len(red_players) == 0 and len(green_players) == 0:
        status_label.config(text = "Please enter at least one player.")
        return

    # Make sure there are no duplicate IDs
    if not check_duplicates(red_players, green_players):
        return

    # Print players for testing
    print("Red Team:", red_players)
    print("Green Team:", green_players)

    # Update the status message
    status_label.config(text = "GAME READY")

# Main window settings
root.title("Entry Terminal")
root.geometry("1280x850")
root.configure(bg = "#0B0712")

# Main heading
tk.Label(root, text = "EDIT CURRENT GAME", bg = "black", fg = "#5CE1E6", font = ("Arial", 20, "bold")
).pack(pady = 15)

# Subheading
tk.Label(root, text = "PHOTON LASER TAG SYSTEM", bg = "black", fg = "#5CE1E6", font = ("Arial", 12)
).pack(pady = 15)

# Frame to hold both teams
teams_frame = tk.Frame(root, bg = "black")
teams_frame.pack()

# Create red team panel
red_frame, red_rows = build_team_panel(teams_frame, "RED TEAM", "#B22222")
red_frame.grid(row = 0, column = 0, padx = 15)

# Create green team panel
green_frame, green_rows = build_team_panel(teams_frame, "GREEN TEAM", "#228B22")
green_frame.grid(row = 0, column = 1, padx = 15)

# Frame for network selection
network_frame = tk.Frame(root, bg = "black")
network_frame.pack(pady = 20)

# Network address label
tk.Label(network_frame, text = "Network Address:", bg = "black", fg = "white"
).grid(row = 0, column = 0, padx = 5)

# Network address entry box
network_entry = tk.Entry(network_frame, bg = "#2A1633", fg = "#F7F4F6", insertbackground = "#F7F4F6", width = 20)
network_entry.grid(row = 0, column = 1, padx = 5)

# Set localhost as the default network
network_entry.insert(0, DEFAULT_NETWORK)

# Button to apply a different network
tk.Button(network_frame, text = "Apply", command = apply_network
).grid(row = 0, column = 2, padx = 5)

# Frame for game controls
controls_frame = tk.Frame(root, bg = "#0B0712")
controls_frame.pack(pady = 5)

# Button to start the game
tk.Button(controls_frame, text = "F5 - START GAME", command = start_game
).grid(row = 0, column = 0, padx = 5)

# Button to clear all player entries
tk.Button(controls_frame, text = "F12 - CLEAR GAME", command = clear_game
).grid(row = 0, column = 1, padx = 5)

# Status message at the bottom
status_label = tk.Label(root, text = "SYSTEM READY", bg = "black", fg = "#5CE1E6")
status_label.pack()

# Bind the F5 key to start the game
root.bind("<F5>", start_game)

# Bind the F12 key to clear the game
root.bind("<F12>", clear_game)

# Keep the window running
root.mainloop()