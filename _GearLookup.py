#   This script is a child for DM Tools
#   This script defines the GearLookup Child class
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
from random import choice as randchoice, shuffle
# Load config
from ___Config import *
# Load parent scripts
from __Lookup import *
from __Tables import *
from __Tooltip import *

class GearLookup(Lookup):
    def __init__(self, master, gear_data, property_data):
        Lookup.__init__(self, master)
        
        self.gear_data = gear_data
        self.item_property_data = property_data
        self.canvas = tk.Canvas(self.window, width = WIN_W-18, height = WIN_H, bg=BLACK_BASE, scrollregion= (0, 0, WIN_W-10, WIN_H+800))
        
        self.scrollbar = tk.Scrollbar(self.window, orient= tk.VERTICAL)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.scrollbar.config(command= self.canvas.yview)
        self.canvas.config(yscrollcommand= self.scrollbar.set)
        self.canvas.pack(side= tk.LEFT, expand= True, fill= tk.BOTH)
        
        name_of_feature = tk.Label(self.window, text= "Gear Name:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W//2-43, B_DIST+32, window= name_of_feature, anchor= tk.E)
        self.feature_query = tk.Entry(self.window, width= 20, font= ('times', 16))
        self.canvas.create_window(WIN_W//2-38, B_DIST+30, window= self.feature_query, anchor= tk.W)
        
        # Extra bins to hold temporary objects
        self.gear_displays = []
        self.display_tables = []
        
        lookup_button = tk.Button(self.window, text= 'Lookup Gear Info', command= self.genGearDesc, bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W//2, B_DIST+75, window= lookup_button)
        
        # Create buttons to show "Next" and "Previous" Features
        self.next_button = tk.Button(self.window, text='Next Feature', command= lambda: self.displayNextObject(self.genGearDesc, True), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2+130, B_DIST+75, window= self.next_button)
        self.prev_button = tk.Button(self.window, text='Previous', command= lambda: self.displayNextObject(self.genGearDesc, False), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2-115, B_DIST+75, window= self.prev_button)
        
        for lookupObject in [self.window, self.canvas, name_of_feature, self.feature_query, lookup_button, self.next_button, self.prev_button]:
            self.setKeyBinds(lookupObject, self.genGearDesc)
            
        try:
            self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["grLook"]["bg"]))
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            self.canvas.create_image(MID_W, 900, image=self.image, anchor=tk.N)
        except:
            print("Gear Lookup Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["grLook"]["bg"] +"\"")
    
    def genGearDesc(self, found_Gear="", event=None):
        self.resetGearDisplay()
        if found_Gear == "":
            gear_input = self.feature_query.get().strip().lower()
            if gear_input != "":
                if ';' in gear_input:
                    self.user_objects = []
                    query_split = gear_input.split(';')
                    for i in range(len(query_split)):
                        self.user_objects.append(randchoice(self.searchGearData(query_split[i].lower().strip())))
                else:
                    self.user_objects = sorted(self.searchGearData(gear_input))
            else:
                all_geardata = [data for data in self.gear_data]
                shuffle(all_geardata)
                self.user_objects = all_geardata
            self.user_objects_index = 0
            found_Gear = self.user_objects[self.user_objects_index]
        self.updateNextButton()
        if found_Gear in self.gear_data:
            posH = B_DIST+110
            infolines = self.getGearInfo(self.gear_data[found_Gear])
            
            for i in range(len(infolines)):
                self.gear_displays.append(tk.Label(self.window, text= "", bg=OFF_WHITE, fg='black', font=('times', 12), wraplength=850, justify="left"))
                self.setKeyBinds(self.gear_displays[i], self.genGearDesc)
            for i in range(len(infolines)):
                if infolines[i][0] == "spacer":
                    posH += infolines[i][1]
                elif infolines[i][0] == "table":
                    temp_tblData = infolines[i][1]
                    temp_Frame = tk.Frame(self.window, bg=OFF_WHITE)
                    self.setKeyBinds(temp_Frame, self.genGearDesc)
                    default_vars = [False for x in range(6)]
                    var_keys = ["name", "dualLabel", "mode", "anchors", "wraplength", "text"]
                    for y in range(len(var_keys)):
                        if var_keys[y] in temp_tblData:
                            default_vars[y] = temp_tblData[var_keys[y]]
                            if y == 0:
                                posH += 5
                    SmartTable(temp_Frame, temp_tblData["items"], default_vars, lambda a: self.setKeyBinds(a, self.genGearDesc))
                    tableId = self.canvas.create_window(B_DIST, posH, anchor=tk.NW, window=temp_Frame)
                    self.window.update()
                    posH += temp_Frame.winfo_reqheight() + 5
                    self.display_tables.append(temp_Frame)
                else:
                    if infolines[i][0] == "header":
                        self.gear_displays[i].configure(font=("times", 16))
                    elif infolines[i][0] == "subheader":
                        self.gear_displays[i].configure(font=("times", 14))
                    elif infolines[i][0] == "core":
                        self.gear_displays[i].configure(font=("times", 14, "italic"))
                    self.gear_displays[i].configure(text=infolines[i][1])
                    if len(infolines[i]) == 3:
                        Tooltip(self.gear_displays[i], text= infolines[i][2])
                    self.canvas.create_window(B_DIST, posH, window= self.gear_displays[i], anchor= tk.NW)
                    posH += self.gear_displays[i].winfo_reqheight()
                    if infolines[i][0] in ["text"]:
                        posH += 5
        else:
            self.gear_displays.append(tk.Label(self.window, text="Gear Info Not Found", bg=OFF_WHITE, fg='black', font=('times', 16), wraplength=780, justify="left"))
            self.canvas.create_window(WIN_W//2, B_DIST+120, window=self.gear_displays[0])
        
    def resetGearDisplay(self):
        for display_object in self.gear_displays:
            display_object.destroy()
        for display_table in self.display_tables:
            display_table.destroy()
        self.gear_displays = []
        self.display_tables = []
    
    def getGearInfo(self, found_Gear, subheader=False):
        infolines = []
        headerString = ""
        # Create the header
        if "name" in found_Gear:
            headerString += found_Gear["name"]
        if "source" in found_Gear:
            # Needs header/subheader format
            headerString += " (" + found_Gear["source"][0] + ", " + str(found_Gear["source"][1]) + ")"
        if headerString:
            infolines.append(["header", headerString])
        # Handle the core information
        core_info = ""
        if "typeString" in found_Gear:
            core_info += found_Gear["typeString"]
        if "cost" in found_Gear:
            if core_info: core_info += ", "
            core_info += f"Cost: {found_Gear['cost']}"
        if "weight" in found_Gear:
            if core_info: core_info += ", "
            core_info += f"Weight: {found_Gear['weight']}"
        if core_info:
            infolines.append(["core", core_info])
        damage_ac = ""
        item_tooltip = ""
        if "damage" in found_Gear:
            damage_ac += found_Gear["damage"]
        elif "ac" in found_Gear:
            damage_ac += found_Gear["ac"]
        if "properties" in found_Gear:
            for item_property in found_Gear["properties"]:
                if damage_ac: damage_ac += ", "
                damage_ac += item_property
                # Create a tooltip for items based on properties
                if " (" in item_property:
                    item_property = item_property.split(" (")[0]
                item_property = item_property.lower()
                if item_property in self.item_property_data:
                    if item_tooltip: item_tooltip += "\n\n"
                    item_tooltip += self.item_property_data[item_property]
        if damage_ac:
            infolines.append(["spacer", 5])
            if item_tooltip:
                infolines.append(["subheader", damage_ac, item_tooltip])
            else:
                infolines.append(["subheader", damage_ac])
            infolines.append(["spacer", 5])
        # Text before the table or statblock
        if "description" in found_Gear:
            if not damage_ac:
                infolines.append(["subheader", found_Gear["description"]])
            else:
                infolines.append(["text", found_Gear["description"]])
        # Table
        if "table" in found_Gear:
            if isinstance(found_Gear["table"], dict):
                infolines.append(["table", found_Gear["table"]])
            elif isinstance(found_Gear["table"], list):
                for found_table in found_Gear["table"]:
                    infolines.append(["table", found_table])
        # Statblock
        if "statblock" in found_Gear:
            infolines.append(["spacer", 10])
            infolines.append(["subheader", found_Gear["statblock"]["name"]]),
            for entry in found_Gear["statblock"]["entries"]:
                infolines.append(["text", found_Gear["statblock"]["entries"][entry]])
            infolines.append(["spacer", 5])
        # Text after the table or statblock
        if "extra description" in found_Gear:
            if not damage_ac:
                infolines.append(["subheader", found_Gear["extra description"]])
            else:
                infolines.append(["text", found_Gear["extra description"]])

        return infolines
    
    def searchGearData(self, gear_input):
        all_geardata = [data for data in self.gear_data]
        if gear_input == "":
            shuffle(all_geardata)
            return all_geardata
        
        if gear_input in all_geardata:
            found_feature_list = [gear_input]
            all_geardata.remove(gear_input)
        else:
            found_feature_list = []

        # Prevent duplicate search results
        def prevent_dups(x, y):
            for a in x:
                if a in y: y.remove(a)
            return y
        
        # Remove characters that shouldn't impact the search
        def clean(s):
            return s.replace(' ', '').replace('\'', '').replace('-', '')
        
        clean_input = clean(gear_input)
        # Check if the Input matches part of a name of a data
        for data in all_geardata:
            if (clean_input in clean(data)):
                found_feature_list.append(data)
        all_geardata = prevent_dups(found_feature_list, all_geardata)
        
        # Run a more advanced search on each data name to check if the error is due to spaces or a typo, also functions as a guess to what data is being typed
        for data in all_geardata:
            # Remove specific non ascii characters from both strings while doing this check
            if (len(gear_input) <= len(data) + 1) and (self.spellcheck(clean_input, clean(data)) <= 1):
                found_feature_list.append(data)
        all_geardata = prevent_dups(found_feature_list, all_geardata)
        
        # If the input matches, or if nothing was found, return the original input as a list
        if found_feature_list:
            return found_feature_list
        else:
            return [gear_input]