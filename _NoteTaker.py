#   This script is a child for DM Tools
#   This script defines the NoteTaker Child class
#
# Import required libraries
import tkinter as tk
# Load config
from ___Config import *

class NoteTaker:
    def __init__(self, master):
        self.window = master
        self.textBox = tk.Text(self.window)
        
        # Scrollbar
        scrollBar = tk.Scrollbar(self.textBox)
        
        # Auto Resize
        self.window.grid_rowconfigure(0, weight= 1)
        self.window.grid_columnconfigure(0, weight= 1)
        self.textBox.grid(sticky= tk.NSEW)
        scrollBar.pack(side= tk.RIGHT, fill= tk.Y)
        
        # Scrollbar auto adjust
        scrollBar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand= scrollBar.set)
        
        self.load()
    
    def clear(self):
        self.textBox.delete("1.0","end")
    
    def load(self, profile=DEFAULT_PROFILE):
        try:
            with open(f"dynamic/profiles/{profile}/noteTaker.txt","r") as f:
                self.textBox.insert(1.0, f.read())
        except:
            print("Note Taker failed to load.")
    
    def save(self, profile=DEFAULT_PROFILE):
        try:
            with open(f"dynamic/profiles/{profile}/noteTaker.txt","w+") as f:
                f.write(self.textBox.get(1.0, tk.END).rstrip())
        except:
            print("Note Taker failed to save.")