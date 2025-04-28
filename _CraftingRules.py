#   This script is a child for DM Tools
#   This script defines the CraftingRules Child class
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
from json import load as jsonLoad
from random import choice as randchoice
# Load config
from ___Config import *
from __Tables import *

class CraftingRules:
    def __init__(self, master, crafting_bundle, bg=None):
        self.window = master
        self.crafting_data = crafting_bundle[0]
        self.random_patterns = crafting_bundle[1]
        self.random_words = crafting_bundle[2]
        self.canvas = tk.Canvas(self.window, width= WIN_W, height= WIN_H)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Create a dropdown to pick what information is show
        self.info_options = self.crafting_data["Options"]
        self.info_choice = tk.StringVar()
        self.info_choice.set(self.info_options[0])
        self.prev_info_choice = self.info_options[0]
        info_dropdown = tk.OptionMenu(self.window, self.info_choice, *self.info_options)
        info_dropdown.config(bg=SCROLL_TAN, fg=BLACK_BASE, font='Times 16 bold')
        info_dropdown["menu"].config(bg=SCROLL_TAN, fg=BLACK_BASE, font='Times 16 bold')
        self.canvas.create_window(B_DIST, B_DIST, anchor= tk.NW, window= info_dropdown)
        self.info_choice.trace("w", lambda var, index, mode: self.drawSelectedInfo())
        
        # Create a location to save crafting info objects
        self.display_objects = {}
        self.temp_display_objects = {}
        # Initialize every tab, bind their objects into a dictionary entry, then hide their objects
        for info_option in self.info_options:
            tempIdBucket = []
            tempOptionData = self.crafting_data[info_option]
            # Headers
            for header_key in tempOptionData["headers"]:
                tempHeaderData = tempOptionData["headers"][header_key]
                tempHeader = tk.Text(self.window, width= tempHeaderData["size"][0], height= tempHeaderData["size"][1], bg= SCROLL_TAN, fg= BLACK_BASE, font= 'Times 16 bold italic')
                tempHeader.insert(tk.END, tempHeaderData["header"])
                if not EDIT_MODE:
                    tempHeader.configure(state= 'disabled')
                tempIdBucket.append(self.canvas.create_window(tempHeaderData["position"][0], tempHeaderData["position"][1], anchor= tk.NW, window= tempHeader))
            # Text Bodies
            for text_key in tempOptionData["text"]:
                tempTextData = tempOptionData["text"][text_key]
                tempText = tk.Text(self.window, width= tempTextData["size"][0], height= tempTextData["size"][1], bg= SCROLL_TAN, fg= BLACK_BASE, font= 'Times 12')
                tempText.insert(tk.END, tempTextData["text"])
                if not EDIT_MODE:
                    tempText.configure(state = 'disabled')
                tempIdBucket.append(self.canvas.create_window(tempTextData["position"][0], tempTextData["position"][1], anchor= tk.NW, window= tempText))
            # Tables
            for table_key in tempOptionData["tables"]:
                tempTableData = tempOptionData["tables"][table_key]
                tempFrame = tk.Frame(self.window)
                if "text" in tempTableData:
                    tempTableTxt = tempTableData["text"]
                else:
                    tempTableTxt = False
                Table(tempFrame, tempTableData["items"], tempTableData["itemWidth"], tempTableTxt, table_key)
                tempIdBucket.append(self.canvas.create_window(tempTableData["position"][0], tempTableData["position"][1], anchor= tk.NW, window= tempFrame))
            # Random Generator Button Functionality
            if "random button" in tempOptionData:
                for button_key in tempOptionData["random button"]:
                    tempButtonData = tempOptionData["random button"][button_key]
                    tempButton = tk.Button(self.window, text=tempButtonData["text"], command=lambda: self.displayRandomContent(tempButtonData["display data"]), width= tempButtonData["size"][0], height= tempButtonData["size"][1], bg= DUNE_TAN, fg= BLACK_BASE, font= 'Times 12')
                    tempIdBucket.append(self.canvas.create_window(tempButtonData["position"][0], tempButtonData["position"][1], anchor= tk.NW, window= tempButton))
            if info_option != self.info_options[0]:
                for info_id in tempIdBucket:
                    self.canvas.itemconfig(info_id, state= 'hidden')
            self.display_objects[info_option] = tempIdBucket
            
        if "Quick Access Tables" in self.crafting_data:
            posW = (WIN_W - B_DIST)
            self.quickAccess_Windows = {}
            for quick_table in self.crafting_data["Quick Access Tables"]:
                QA_tableData = self.crafting_data["Quick Access Tables"][quick_table]
                self.quickAccess_Windows[quick_table] = self.createPopupTable(QA_tableData)
                QA_tableButton = tk.Button(self.window, text= QA_tableData["name"], command= self.quickAccess_Windows[quick_table].deiconify, width= QA_tableData["size"][0], height= QA_tableData["size"][1], bg= SCROLL_TAN, fg= BLACK_BASE, font= 'Times 16 bold')
                self.canvas.create_window(posW, B_DIST, anchor= tk.NE, window= QA_tableButton)
                posW -= QA_tableData["size"][0] * 14
        
        try:
            self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["craftRules"]["bg"]))
            self.canvas.create_image(0, 0, image= self.image, anchor= tk.NW)
        except:
            print("Crafting Rules Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["craftRules"]["bg"] +"\"")
             
    def drawSelectedInfo(self):
        old_option = self.prev_info_choice
        new_option = self.info_choice.get()
        if old_option == new_option: return
        # Hide any old objects, delete any temporary objects, then display any new objects
        for old_info_id in self.display_objects[old_option]:
            self.canvas.itemconfig(old_info_id, state= 'hidden')
        for temp_object_list in self.temp_display_objects:
            for temp_object in self.temp_display_objects[temp_object_list]:
                temp_object.destroy()
        for new_info_id in self.display_objects[new_option]:
            self.canvas.itemconfig(new_info_id, state= 'normal')
        # Remember the current choice
        self.prev_info_choice = new_option
    
    def displayRandomContent(self, display_data):
        posH = display_data["position"][1]
        # Destroy this button's temporary objects, if they already exist
        if display_data["name"] in self.temp_display_objects:
            for temp_object in self.temp_display_objects[display_data["name"]]:
                temp_object.destroy()
        self.temp_display_objects[display_data["name"]] = []
        for i in range(display_data["times"]):
            displayPattern = randchoice(self.random_patterns[display_data["patterns"]])
            displayArray = []
            for element in displayPattern:
                displayArray.append(randchoice(self.random_words[element]))
            # Using * as a key to remove unwanted join characters
            displayString = display_data["join"].join(displayArray).replace(display_data["join"] + "*", "")
            displayLabel = tk.Label(self.window, text= displayString, bg= DUNE_TAN, fg= BLACK_BASE, font= 'Times 12')
            self.temp_display_objects[display_data["name"]].append(displayLabel)
            self.canvas.create_window(display_data["position"][0], posH, window= displayLabel)
            posH += 26
    
    def createPopupTable(self, table_data):
        popup = tk.Toplevel(self.window, bg= DUNE_TAN)
        popup.title(table_data["name"])
        tempFrame = tk.Frame(popup)
        if "text" in table_data:
            tempTableText = table_data["text"]
        else:
            tempTableText = False
        temp_Table = Table(tempFrame, table_data["items"], table_data["itemWidth"], tempTableText, table_data["name"])
        tempFrame.pack()
        closeButton = tk.Button(popup, text= "Close", font= ('times', 12), command= popup.withdraw, bg= DARK_RED, fg= OFF_WHITE)
        closeButton.pack(pady= 5)
        popup.protocol("WM_DELETE_WINDOW", popup.withdraw)
        popup.attributes("-topmost", True)
        popup.withdraw()
        return popup 