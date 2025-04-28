#   This script is a child for DM Tools
#   This script defines the DiceRoller Child class
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
import random
import re
# Load config
from ___Config import *

class DiceRoller:
    def __init__(self, master):
        self.window = master
        self.canvas = tk.Canvas(self.window, width = WIN_W, height = WIN_H)
        self.canvas.pack()
        try:
            self.background_image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["dieRoller"]["bg"]))
            self.canvas.create_image(0, 0, image= self.background_image, anchor= tk.NW)
        except:
            print("Dice Roller Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["dieRoller"]["bg"] +"\"")
            
        self.font = "times 16"
        self.def_width = 45
        
        tab_header = tk.Label(self.window, text="Dice Roller", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(B_DIST, B_DIST, anchor=tk.NW, window=tab_header)
        self.entry_1 = tk.Entry(self.window, width=self.def_width, font=self.font)
        self.canvas.create_window(30, 70, anchor=tk.NW, window=self.entry_1)
        
        self.result_label = tk.Label(self.window, text= "", bg= OFF_WHITE, fg= BLACK_BASE, font= self.font, justify= "left")
        
        self.entry_1.bind("<Return>", self.calculate)
    
    def calculate(self, event):
        dieString = self.entry_1.get()
        self.result_label.configure(text= self.parseDieString(dieString))
        self.result_id =self.canvas.create_window(45, 110, anchor=tk.NW, window=self.result_label)
    
    def parseDieString(self, dieString, mode="text"):
        # Find dice in the pattern XdY
        matches = re.findall(r'\b\d+d\d+\b', dieString)
        alt_resultString = dieString
        dice_found = False
        for die_match in matches:
            dice_found = True
            number_of_rolls, die_size = die_match.split('d')
            die_result = 0
            roll_track = []
            for i in range(int(number_of_rolls)):
                roll = random.randint(1, int(die_size))
                roll_track.append(str(roll))
                die_result += roll
            if len(roll_track) <= MAX_DICE_DISPLAY:
                alt_resultString = alt_resultString.replace(die_match, f"({', '.join(roll_track)})", 1)
            else:
                alt_resultString = alt_resultString.replace(die_match, f"({str(die_result)})", 1)
            dieString = dieString.replace(die_match, str(die_result), 1)
        
        # Find dice in the pattern dX
        matches = re.findall(r'\bd\d+\b', dieString)
        for die_match in matches:
            dice_found = True
            die_size = die_match[1:]
            die_result = random.randint(1, int(die_size))
            alt_resultString = alt_resultString.replace(die_match, f"({str(die_result)})", 1)
            dieString = dieString.replace(die_match, str(die_result), 1)
        
        # Attempt to solve any math operations in the pattern 
        # Do not eval() if non-math characters exist in the string
        allowed_chars = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-', '+', '*', '/', '%', '!', '^', '(', ')', ' '])
        if set(dieString) <= allowed_chars:
            try:
                dieString = eval(dieString)
            except:
                pass
        if dice_found and mode == "text":
            return f"{dieString}\nRoll Results:\n{alt_resultString}"
        elif mode == "text":
            return dieString
        elif mode == "num":
            try:
                return int(dieString)
            except:
                return 0   

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    rollDice = DiceRoller(tk.Tk())
    rollDice.run()