#   This script is a child for GM Tools
#   This script defines the ScrollGenerator Child class
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
from random import choice as randchoice, randint as randInt
# Load config
from ___Config import *
# Load parent scripts
from __Spells import *
from __Tooltip import *

class ScrollGenerator(Spells):
    def __init__(self, master, spell_data):
        Spells.__init__(self, spell_data)
        self.window = master
        self.canvas = tk.Canvas(self.window, width = WIN_W, height = WIN_H, bg= RICH_BLUE)
        self.canvas.pack()
        # Create up to SCROLL_MAX labels to display generated scrolls
        self.scroll_labels = []
        self.scroll_tooltips = []
        for i in range(SCROLL_MAX):
            temp_label = tk.Label(self.window, text= "", bg= OFF_WHITE, fg= BLACK_BASE, font= ('times', 16))
            self.scroll_labels.append(temp_label)
            temp_tooltip = Tooltip(temp_label, text="")
            self.scroll_tooltips.append(temp_tooltip)
        
        # Create a checkbox to determine if duplicates should be generated
        self.duplicates = tk.BooleanVar()
        duplicates_Button = tk.Checkbutton(self.window, text= 'Duplicates', variable= self.duplicates, onvalue= True, offvalue= False, bg= BLANK_GRAY, font=('helvetica', 12, 'bold'), borderwidth= 3, relief='raised')
        self.canvas.create_window(43, 5, window= duplicates_Button, anchor= tk.NW)
        
        # Create a dropdown to control how spells are picked
        options = ["Default", "Uniform", "Linear (Decreasing)", "Exponential (Decreasing)", "Linear (Increasing)", "Exponential (Increasing)", "Custom"]
        self.weight_type = tk.StringVar()
        self.weight_type.set("Default")
        weights_dropdown = tk.OptionMenu(self.window, self.weight_type, *options)
        self.canvas.create_window(7, 40, window= weights_dropdown, anchor= tk.NW)
        self.weight_type.trace("w", lambda var, index, mode: self.selectCustomWeights())
        
        # Create trackable variables for the "Custom" weighting, and a popup window to adjust them
        self.customWeights = [0 for x in range(10)]
        self.customWeights_Window = tk.Toplevel(self.window)
        self.customWeights_Window.title("Custom Weights")
        self.customWeights_Sliders = []
        for i in range(10):
            tempLabel = tk.Label(self.customWeights_Window, text=self.levels_dict[str(i)], font=('helvetica', 10, 'bold'))
            tempLabel.pack()
            tempSlider = tk.Scale(self.customWeights_Window, from_= 0, to= 100, length= 300, orient= tk.HORIZONTAL)
            tempSlider.pack(padx= 7)
            self.customWeights_Sliders.append(tempSlider)
        for i in range(len(self.customWeights_Sliders)):
            def customWeights_lambda(x):
                return lambda event: self.setCustomWeight(x)
            self.customWeights_Sliders[i].config(command= customWeights_lambda(i))
        close_customWeights_Button = tk.Button(self.customWeights_Window, text= "Close", font= ('helvetica', 10), command= self.customWeights_Window.withdraw, bg= DARK_RED, fg= OFF_WHITE)
        close_customWeights_Button.pack(pady=5)
        self.customWeights_Window.protocol("WM_DELETE_WINDOW", self.customWeights_Window.withdraw)
        self.customWeights_Window.attributes("-topmost", True)
        self.customWeights_Window.withdraw()
        
        # Create an Input for the desired Number of Scrolls
        scrollNumberInput_Txt = tk.Label(self.window, text= "# of Scrolls:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(THRD_W-17, B_DIST+32, window=scrollNumberInput_Txt)
        self.scrollNumberInput = tk.Entry(self.window, width= 2, font= ('times', 16))
        self.canvas.create_window(THRD_W+53, B_DIST+30, window=self.scrollNumberInput)
        
        # Show "Click to Generate Scrolls"
        self.scroll_labels[0].config(text= "Click the Button Above\nto Generate Scrolls")
        self.canvas.create_window(THRD_W, B_DIST+180, window=self.scroll_labels[0])
        
        # Create filter checkboxes
        self.filter_dict = {}
        header_dict = {"lvl" : "Level:", "sch" : "School:", "cls" : "Class:", "sty" : "Styles:", "pub" : "Publishers:"}
        filter_types = {"lvl" : [self.levels_dict[lvl_key] for lvl_key in self.levels_txt], "sch" : self.schools_txt, "sty" : self.styles_txt, "cls" : [className.capitalize() for className in self.classes_txt], "pub" : publishers_txt}
        for filter_key in filter_types:
            self.filter_dict[filter_key + "_var"] = []
            self.filter_dict[filter_key + "_box"] = []
        for filter_key in filter_types:
            self.filter_dict[filter_key + "_header"] = tk.Label(self.window, text=header_dict[filter_key], bg= SCROLL_TAN, fg= BLACK_BASE, font= ('helvetica', 12, 'italic'), borderwidth= 2, relief= "raised")
            for filter_name in filter_types[filter_key]:
                temp_var = tk.IntVar()
                temp_box = tk.Checkbutton(self.window, text= filter_name, variable= temp_var, onvalue= True, offvalue= False, bg= SCROLL_TAN, font= ('helvetica', 10), borderwidth= 2, relief= "raised")
                if filter_key != "sty" or filter_name == "No Style":
                    temp_box.select()
                self.filter_dict[filter_key + "_var"].append(temp_var)
                self.filter_dict[filter_key + "_box"].append(temp_box)
        for filter_key in filter_types:
            def doubleClick_head_lambda(filter_key):
                return lambda event: self.doubleClick(self.filter_dict[filter_key + "_box"], "head")
            self.filter_dict[filter_key + "_header"].bind('<Double-1>', doubleClick_head_lambda(filter_key))
            for checkbox in self.filter_dict[filter_key + "_box"]:
                def doubleClick_body_lambda(filter_key):
                    return lambda event: self.doubleClick(self.filter_dict[filter_key + "_box"])
                checkbox.bind('<Double-1>', doubleClick_body_lambda(filter_key))
        
        # Draw the filter headers and checkboxes
        filter_Label = tk.Label(self.window, text= "Filters", bg= RICH_BLUE, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'), relief= 'raised')
        self.canvas.create_window(2*(THRD_W)+5, B_DIST, window= filter_Label, anchor= tk.NE)
        posW = 2*(THRD_W) + 25
        posH = B_DIST + 25
        posSave = 0
        for filter_key in filter_types:
            if filter_key == "sch": 
                posW = 2*(THRD_W) + 25
                posSave = posH
            self.canvas.create_window(posW, posH, window= self.filter_dict[filter_key + "_header"], anchor= tk.W)
            filter_boxes = self.filter_dict[filter_key + "_box"]
            for i in range(len(filter_boxes)):
                if filter_key == "lvl" and i == 5:
                    posW += 90
                    posH = B_DIST + 25
                posH += 25
                self.canvas.create_window(posW, posH, window = filter_boxes[i], anchor= tk.W)
            posH += 30
            if filter_key == "sty":
                posH = posSave
                posW += 120
        
        # Fetch the copy icon for the copy button
        try:
            self.copy_icon = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["scrollGen"]["copy_i"]).resize((23, 23), resample= 3))
            copy_button = tk.Button(self.window, command= self.copyScrolls, image= self.copy_icon)
        except:
            print("Scroll Generator Copy Icon failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["scrollGen"]["copy_i"] +"\"")
            copy_button = tk.Button(self.window, text= "^C", command= self.copyScrolls, height= 1, width= 2, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(22, 20, window=copy_button)
        
        generate_Scrolls_Button = tk.Button(self.window, text= 'Generate Scrolls', command= self.generateScrolls, bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(THRD_W, B_DIST+75, window=generate_Scrolls_Button)
        # Bind the Enter key to Scroll Generation
        self.canvas.bind('<Return>', self.generateScrolls)
        self.scrollNumberInput.bind('<Return>', self.generateScrolls)
        # Pressing Ctrl+C will copy any generated spells to the clipboard
        self.canvas.bind('<Control-c>', self.copyScrolls)
        self.scrollNumberInput.bind('<Control-c>', self.copyScrolls)
        
        try:
            self.generator_image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["scrollGen"]["bg"]))
            self.canvas.create_image(MID_W//2, MID_H, image= self.generator_image)
        except:
            print("Scroll Generator Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["scrollGen"]["bg"] +"\"")
        try:
            self.filter_image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["scrollGen"]["f_bg"]).resize((THRD_W+5, WIN_H), resample= 3))
            self.canvas.create_image(2*THRD_W, 0, image= self.filter_image, anchor= tk.NW)
        except:
            print("Scroll Filter Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["scrollGen"]["f_bg"] +"\"")
        self.canvas.create_rectangle(2*THRD_W, 0, 2*(THRD_W) +5, WIN_H, fill= RICH_BLUE)
        
    def generateScrolls(self, event=None):
        # Reset all scroll labels
        self.resetScrolls()
        # Filter the list of spells
        currentScrolls = self.getFilters(self.spell_data.copy())
        total_spells = len(currentScrolls)
        
        posW = THRD_W
        posH = B_DIST+100
        number = self.scrollNumberInput.get()
        allowDuplicates = self.duplicates.get()
        try:
            number = int(number)
            if (number > SCROLL_MAX):
                number = SCROLL_MAX
        # If input is invalid generate one scroll
        except:
            number = 1
        # Edge Case where total spells is less than number to be generated and allow duplicates is off
        if number > total_spells and not allowDuplicates:
            number = total_spells
        # If more than half SCROLL_MAX spells are being generated, create two columns of spells
        if(number > SCROLL_MAX//2):
            posW = MID_W//3
        for j in range(number):
            # If more than half SCROLL_MAX spells are being generated, shift to a new column halfway (rounding up)
            if(number > SCROLL_MAX//2 and j == -(number // -2)):
                posW = MID_W
                posH = B_DIST+100
            
            spellChosen = self.pickScroll(currentScrolls)
            if (not allowDuplicates):
                currentScrolls.pop(spellChosen.lower())
            
            # Place the generated scrolls
            posH += 30
            self.scroll_labels[j].configure(text= spellChosen)
            self.scroll_tooltips[j].text = ("\n".join(self.getSpellInfo(self.spell_data[spellChosen.lower()]))).replace('**', '').strip()
            self.canvas.create_window(posW, posH, window= self.scroll_labels[j])
        
    def resetScrolls(self):
        for i in range(SCROLL_MAX):
            self.scroll_labels[i].configure(text= "")
            temp_id = self.canvas.create_window(THRD_W, B_DIST+100, window=self.scroll_labels[i])
            self.canvas.itemconfigure(temp_id, state= 'hidden')
    
    def getFilters(self, current_Scrolls):
        mode = self.weight_type.get()
        # Filter based on the "Custom" scroll mode so later automation doesn't create an infinite loop
        # Redefine a more convenient filter_types
        filter_types = {"lvl" : self.levels_txt, "sch" : self.schools_txt, "sty" : self.styles_txt, "cls" : self.classes_txt, "pub" : publishers_txt}
        active_filter_vars = {}
        for filter_key in filter_types:
            active_filter_vars[filter_key] = [filter_var.get() for filter_var in self.filter_dict[filter_key + "_var"]]
        if all([active_filter_vars[key] == 1 for key in active_filter_vars]) and mode != "Custom":
            return current_Scrolls
        filters = {}
        for filter_key in filter_types:
            if filter_key == "pub":
                filters["src"] = []
            else:
                filters[filter_key] = []
            if not all(active_filter_vars[filter_key]) or (filter_key == "lvl" and mode == "Custom"):
                for i in range(len(filter_types[filter_key])):
                    if active_filter_vars[filter_key][i] == 1:
                        if filter_key == "pub":
                            for book_abr in publishers_dict[publishers_txt[i]]:
                                filters["src"].append(sources_dict[book_abr])
                        elif filter_key != "lvl" or (filter_key == "lvl" and mode != "Custom") or (filter_key == "lvl" and mode == "Custom" and self.customWeights[i] != 0):
                            filters[filter_key].append(filter_types[filter_key][i])
        return self.filterSpells(current_Scrolls, filters)
                            
    def pickScroll(self, current_Scrolls):
        # Choose a random scroll with support for various weighting styles
        mode = self.weight_type.get()
        if mode == 'Default':
            return randchoice([current_Scrolls[spell]["name"] for spell in current_Scrolls])
        leveled_Spells = [[] for i in range(10)]
        for spell in current_Scrolls:
            leveled_Spells[int(current_Scrolls[spell]["level"])].append(current_Scrolls[spell]["name"])
        current_weights = []
        weight_dict = {
            "Uniform" : lambda a: 1,
            "Linear (Decreasing)" : lambda a: 10-a,
            "Exponential (Decreasing)" : lambda a: (10-a)*(10-a),
            "Linear (Increasing)" : lambda a: a+1,
            "Exponential (Increasing)" : lambda a: (a+1)*(a+1)
        }
        if mode == "Custom":
            current_weights = self.customWeights.copy()
        elif mode in weight_dict:
            for i in range(10):
                current_weights.append(weight_dict[mode](i))
        else:
            return randchoice([current_Scrolls[spell]["name"] for spell in current_Scrolls])
        
        for i in range(9, -1, -1):
            if leveled_Spells[i] == []:
                del leveled_Spells[i]
                del current_weights[i]
        
        weightSum = sum(current_weights)
        if mode == "Custom" and weightSum > 0:
            if weightSum == 1:
                levelPick = 1
            else:
                levelPick = randInt(1, weightSum)
        else:
            levelPick = randInt(0, weightSum)
        postSum_weights = [sum(current_weights[:i+1]) for i in range(len(current_weights))]
        for i in range(len(postSum_weights)):
            if levelPick <= postSum_weights[i]:
                return randchoice(leveled_Spells[i])
        
        # If a failure occurs, just return a spell at random
        return randchoice([current_Scrolls[spell]["name"] for spell in current_Scrolls])

    def doubleClick(self, checkboxes, mode= "body"):
        # Double Click Functionality for ease of Filter Selection
        if mode == "body":
            for box in checkboxes:
                box.deselect()
        elif mode == "head":
            for box in checkboxes:
                box.select()
    
    def copyScrolls(self, event=None):
        scroll_names = []
        for i in range(SCROLL_MAX):
            try:
                if (self.scroll_labels[i]['text'] != ""): scroll_names.append(self.scroll_labels[i]['text'])
            except:
                print("Failure occured")
                break
        if (scroll_names != []):
            clipboard_txt = ("; ").join(scroll_names)
            self.window.clipboard_clear()
            self.window.clipboard_append(clipboard_txt)
            self.window.update()
    
    def setCustomWeight(self, i):
        self.customWeights[i] = self.customWeights_Sliders[i].get()
    
    def selectCustomWeights(self):
        if self.weight_type.get() == "Custom":
            # Show the popup for Custom weight scaling
            self.customWeights_Window.deiconify()
