import time
from pynput.mouse import Controller, Listener
from pynput.keyboard import Listener as KeyboardListener, Key
import threading
import tkinter as tk
from tkinter import Listbox, Button

# Initialize the mouse controller
mouse_controller = Controller()

# Global variables
saved_positions = []
last_position = None
last_move_time = None
hold_time = 1 
move_threshold = 10  
is_running = True

# Create the main window
root = tk.Tk()
root.title("QuickQursor")
root.geometry("300x450")

# Create a listbox to display saved positions
position_listbox = Listbox(root, width=50, height=20)
position_listbox.pack(padx=10, pady=10)

# Function to update the listbox
def update_listbox():
    current_selection = position_listbox.curselection()
    position_listbox.delete(0, tk.END)
    for pos in saved_positions:
        position_listbox.insert(tk.END, f"X: {pos[0]}, Y: {pos[1]}")

    if current_selection:
        position_listbox.selection_set(current_selection)

# Function to move the mouse to the selected position
def teleport_to_selected():
    try:
        selected_index = position_listbox.curselection()[0]
        selected_position = saved_positions[selected_index]
        print(f"Teleporting to: {selected_position}")
        mouse_controller.position = selected_position
    except IndexError:
        print("No position selected.")

# Create a button to teleport to the selected position
teleport_button = Button(root, text="Teleport to Selected", command=teleport_to_selected)
teleport_button.pack(pady=5)

# Function to handle mouse movement and detect stillness
def on_move(x, y):
    global last_position, last_move_time

    if last_position is not None:
        distance = ((x - last_position[0]) ** 2 + (y - last_position[1]) ** 2) ** 0.5
        if distance > move_threshold:
            last_move_time = time.time()
        else:
            if last_move_time and time.time() - last_move_time >= hold_time:
                saved_position = (x, y)
                saved_positions.append(saved_position)
                print(f"Position saved: {saved_position}")
                root.after(0, update_listbox)
                last_move_time = time.time()
    else:
        last_move_time = time.time()

    last_position = (x, y)

# Function to handle keyboard input (for the hotkey)
def on_press(key):
    try:
        if key == Key.f1:
            if saved_positions:
                saved_position = saved_positions[-1]
                print(f"Moving mouse to saved position: {saved_position}")
                mouse_controller.position = saved_position
    except AttributeError:
        pass

# Function to stop the listeners
def stop_listeners():
    global is_running
    is_running = False
    mouse_listener.stop()
    keyboard_listener.stop()
    root.quit()

# Set up the mouse listener
mouse_listener = Listener(on_move=on_move)
mouse_listener.start()

# Set up the keyboard listener
keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", stop_listeners)

# Start the GUI main loop
root.mainloop()
