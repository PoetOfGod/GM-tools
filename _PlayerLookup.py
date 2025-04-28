#   This script is a child for DM Tools
#   This script defines the PlayerLookup Child class
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

class PlayerLookup(Lookup):
    def __init__(self, master, player_data):
        Lookup.__init__(self, master)
        
        self.player_data = player_data
        self.canvas = tk.Canvas(self.window, width = WIN_W-18, height = WIN_H, scrollregion= (0, 0, WIN_W-10, WIN_H+3900))
        
        self.scrollbar = tk.Scrollbar(self.window, orient= tk.VERTICAL)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.scrollbar.config(command= self.canvas.yview)
        self.canvas.config(yscrollcommand= self.scrollbar.set)
        self.canvas.pack(side= tk.LEFT, expand= True, fill= tk.BOTH)
        
        name_of_feature = tk.Label(self.window, text= "Feature Name:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W//2-43, B_DIST+32, window= name_of_feature, anchor= tk.E)
        self.feature_query = tk.Entry(self.window, width= 20, font= ('times', 16))
        self.canvas.create_window(WIN_W//2-38, B_DIST+30, window= self.feature_query, anchor= tk.W)
        
        # Extra bins to hold temporary objects
        self.player_displays = []
        self.display_tables = []
        
        lookup_button = tk.Button(self.window, text= 'Lookup Player Info', command= self.genPlayerDesc, bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W//2, B_DIST+75, window= lookup_button)
        
        # Create buttons to show "Next" and "Previous" Features
        self.next_button = tk.Button(self.window, text='Next Feature', command= lambda: self.displayNextObject(self.genPlayerDesc, True), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2+135, B_DIST+75, window= self.next_button)
        self.prev_button = tk.Button(self.window, text='Previous', command= lambda: self.displayNextObject(self.genPlayerDesc, False), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2-120, B_DIST+75, window= self.prev_button)
        
        for lookupObject in [self.window, self.canvas, name_of_feature, self.feature_query, lookup_button, self.next_button, self.prev_button]:
            self.setKeyBinds(lookupObject, self.genPlayerDesc)
            
        try:
            # This is a really long application so display the image stacked on itself multiple times
            self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["plyLook"]["bg"]))
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.N)
            self.canvas.create_image(MID_W, 977, image=self.image, anchor=tk.N)
            self.canvas.create_image(0, 1954, image=self.image, anchor=tk.NW)
            self.canvas.create_image(MID_W, 2931, image=self.image, anchor=tk.N),
            self.canvas.create_image(0, 3908, image=self.image, anchor=tk.N)
        except:
            print("Player Lookup Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["plyLook"]["bg"] +"\"")
    
    def genPlayerDesc(self, found_Player="", event=None):
        self.resetPlayerDisplay()
        if found_Player == "":
            player_input = self.feature_query.get().strip().lower()
            if player_input != "":
                if ';' in player_input:
                    self.user_objects = []
                    query_split = player_input.split(';')
                    for i in range(len(query_split)):
                        self.user_objects.append(randchoice(self.searchPlayerData(query_split[i].lower().strip())))
                else:
                    self.user_objects = self.searchPlayerData(player_input)
            else:
                all_playerdata = [data for data in self.player_data]
                shuffle(all_playerdata)
                self.user_objects = all_playerdata
            self.user_objects_index = 0
            found_Player = self.user_objects[self.user_objects_index]
        self.updateNextButton()
        if found_Player in self.player_data:
            posH = B_DIST+110
            infolines = self.getPlayerInfo(self.player_data[found_Player])
            
            for i in range(len(infolines)):
                self.player_displays.append(tk.Label(self.window, text= "", bg=OFF_WHITE, fg='black', font=('times', 12), wraplength=850, justify="left"))
                self.setKeyBinds(self.player_displays[i], self.genPlayerDesc)
            for i in range(len(infolines)):
                if infolines[i][0] == "spacer":
                    posH += infolines[i][1]
                elif infolines[i][0] == "table":
                    temp_tblData = infolines[i][1]
                    temp_Frame = tk.Frame(self.window, bg=OFF_WHITE)
                    self.setKeyBinds(temp_Frame, self.genPlayerDesc)
                    default_vars = [False for x in range(6)]
                    var_keys = ["name", "dualLabel", "mode", "anchors", "wraplength", "text"]
                    for y in range(len(var_keys)):
                        if var_keys[y] in temp_tblData:
                            default_vars[y] = temp_tblData[var_keys[y]]
                            if y == 0:
                                posH += 5
                    SmartTable(temp_Frame, temp_tblData["items"], default_vars, lambda a: self.setKeyBinds(a, self.genPlayerDesc))
                    tableId = self.canvas.create_window(B_DIST, posH, anchor=tk.NW, window=temp_Frame)
                    self.window.update()
                    posH += temp_Frame.winfo_reqheight() + 5
                    self.display_tables.append(temp_Frame)
                else:
                    if infolines[i][0] == "header":
                        self.player_displays[i].configure(font=("times", 16))
                    elif infolines[i][0] == "subheader":
                        self.player_displays[i].configure(font=("times", 14))
                        if i > 0 and infolines[i-1][0] == "subheader":
                            posH += 5
                    elif infolines[i][0] == "suffix":
                        self.player_displays[i].configure(font=("times", 14, "italic"))
                    elif infolines[i][0] == "prereq":
                        self.player_displays[i].configure(font=("times", 12, "italic"))
                    self.player_displays[i].configure(text=infolines[i][1])
                    if infolines[i][0] != "prereq" or i < 0 or self.player_displays[i-1].winfo_reqwidth() <= 1:
                        self.canvas.create_window(B_DIST, posH, window= self.player_displays[i], anchor= tk.NW)
                        posH += self.player_displays[i].winfo_reqheight()
                    else:
                        self.canvas.create_window(B_DIST+self.player_displays[i-1].winfo_reqwidth(), posH, window=self.player_displays[i], anchor= tk.SW)
                    if infolines[i][0] in ["text", "suffix"]:
                        posH += 5
        else:
            self.player_displays.append(tk.Label(self.window, text="Player Info Not Found", bg=OFF_WHITE, fg='black', font=('times', 16), wraplength=780, justify="left"))
            self.canvas.create_window(WIN_W//2, B_DIST+120, window=self.player_displays[0])
        
    def resetPlayerDisplay(self):
        for display_object in self.player_displays:
            display_object.destroy()
        for display_table in self.display_tables:
            display_table.destroy()
        self.player_displays = []
        self.display_tables = []
    
    def getPlayerInfo(self, found_Player, master_source="", subheader=False):
        infolines = []
        headerString = ""
        # Create the header
        if "prefix" in found_Player and not subheader:
            headerString += found_Player["prefix"] + " "
        if "name" in found_Player:
            headerString += found_Player["name"]
        if "source" in found_Player and found_Player["source"][0] != master_source:
            master_source = found_Player["source"][0]
            # Needs header/subheader format
            headerString += " (" + master_source + ", " + str(found_Player["source"][1]) + ")"
        if headerString:
            if not subheader:
                infolines.append(["header", headerString])
            else:
                infolines.append(["subheader", headerString])
        # Handle the Suffix and Prereq
        suffixString = ""
        if "suffix" in found_Player and not subheader:
            suffixString += found_Player["suffix"]
            suffix_type = "suffix"
        if "prereq" in found_Player:
            if suffixString:
                suffixString += " " + found_Player["prereq"]
            elif not subheader:
                suffixString += found_Player["prereq"]
                suffix_type = "suffix"
            else:
                suffixString += found_Player["prereq"]
                suffix_type = "prereq"
        if suffixString:
            infolines.append([suffix_type, suffixString])
        # Text before the table or statblock
        if "text" in found_Player:
            if not subheader:
                infolines.append(["subheader", found_Player["text"]])
            else:
                infolines.append(["text", found_Player["text"]])
        # Table
        if "table" in found_Player:
            if isinstance(found_Player["table"], dict):
                infolines.append(["table", found_Player["table"]])
            elif isinstance(found_Player["table"], list):
                for found_table in found_Player["table"]:
                    infolines.append(["table", found_table])
        # Statblock
        if "statblock" in found_Player:
            infolines.append(["spacer", 10])
            infolines.append(["subheader", found_Player["statblock"]["name"]]),
            for entry in found_Player["statblock"]["entries"]:
                infolines.append(["text", found_Player["statblock"]["entries"][entry]])
            infolines.append(["spacer", 5])
        # Text after the table or statblock
        if "extra text" in found_Player:
            if not subheader:
                infolines.append(["subheader", found_Player["extra text"]])
            else:
                infolines.append(["text", found_Player["extra text"]])
        # Iterate through the features of the object
        if "features" in found_Player:
            if "feature_header" in found_Player:
                infolines.append(["header", found_Player["feature_header"]])
            for feature in found_Player["features"]:
                if feature == "exclude":
                    pass
                else:
                    for feature_line in self.getPlayerInfo(found_Player["features"][feature], master_source, True):
                        infolines.append(feature_line)
        return infolines
    
    def searchPlayerData(self, player_input):
        all_playerdata = [data for data in self.player_data]
        if player_input == "":
            shuffle(all_playerdata)
            return all_playerdata
        
        if player_input in all_playerdata:
            found_feature_list = [player_input]
            all_playerdata.remove(player_input)
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
        
        clean_input = clean(player_input)
        # Check if the Input matches part of a name of a data
        for data in all_playerdata:
            if (clean_input in clean(data)):
                found_feature_list.append(data)
        all_playerdata = prevent_dups(found_feature_list, all_playerdata)
                
        # Remove the Prefix (No spellcheck)
        for data in all_playerdata:
            if "prefix" in self.player_data[data]:
                short_data = data[len(self.player_data[data]["prefix"]):]
                if (clean_input in clean(short_data)):
                    found_feature_list.append(data)
        all_playerdata = prevent_dups(found_feature_list, all_playerdata)
        
        # Check the Suffix (No spellcheck)
        for data in all_playerdata:
            if "suffix" in self.player_data[data]:
                suffix_data = self.player_data[data]["suffix"].lower()
                if (clean_input in clean(suffix_data)):
                    found_feature_list.append(data)
        all_playerdata = prevent_dups(found_feature_list, all_playerdata)
        
        # Run a more advanced search on each data name to check if the error is due to spaces or a typo, also functions as a guess to what data is being typed
        for data in all_playerdata:
            # Remove specific non ascii characters from both strings while doing this check
            if (len(player_input) <= len(data) + 1) and (self.spellcheck(clean_input, clean(data)) <= 1):
                found_feature_list.append(data)
        all_playerdata = prevent_dups(found_feature_list, all_playerdata)
        
        # Remove the Prefix (Spellcheck)
        for data in all_playerdata:
            if "prefix" in self.player_data[data]:
                short_data = data[len(self.player_data[data]["prefix"]):]
                # Remove specific non ascii characters from both strings while doing this check
                if (len(player_input) <= len(short_data) + 1) and (self.spellcheck(clean_input, clean(short_data)) <= 1):
                    found_feature_list.append(data)
        all_playerdata = prevent_dups(found_feature_list, all_playerdata)
        
        # Check the Suffix (Spellcheck)
        for data in all_playerdata:
            if "suffix" in self.player_data[data]:
                suffix_data = self.player_data[data]["suffix"].lower()
                if (len(player_input) <= len(suffix_data) + 1) and (self.spellcheck(clean_input, clean(suffix_data)) <= 1):
                    found_feature_list.append(data)
        
        # If the input matches, or if nothing was found, return the original input as a list
        if found_feature_list:
            return found_feature_list
        else:
            return [player_input]