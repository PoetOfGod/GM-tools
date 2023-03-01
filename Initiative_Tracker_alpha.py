#   This script is a child for GM Tools, this is the functionality for the Initiative Tracker
#   This will initially be functionally a Notepad file but will eventually incorporate significant automation
#
# Import required libraries
import tkinter as tk

# Global Variables to Act Like Macros
from GM_Basics_alpha import *

# Automatically Save the textArea when GM_Tools is closed
def initTrackerSave(textArea):
    try:
        with open("dynamic\\initTracker.txt","w") as f:
            textToSave = textArea.get(1.0, tk.END).rstrip()
            f.write(textToSave)
    except:
        pass
 
def initializeInitiativeTracker(master):
    textArea = tk.Text(master)
    
    # To add scrollbar
    scrollBar = tk.Scrollbar(textArea)    

    # To make the textArea auto resizable
    master.grid_rowconfigure(0, weight=1)
    master.grid_columnconfigure(0, weight=1)
 
    # Add controls (widget)
    textArea.grid(sticky = tk.N + tk.E + tk.S + tk.W)
 
    scrollBar.pack(side=tk.RIGHT,fill=tk.Y)                   
         
    # Scrollbar will adjust automatically according to the content       
    scrollBar.config(command=textArea.yview)    
    textArea.config(yscrollcommand=scrollBar.set)

    # Always attempt to load an existing text file
    try:
        with open("dynamic\\initTracker.txt","r") as f:
            textArea.insert(1.0, f.read())
    except:
        pass

    return textArea