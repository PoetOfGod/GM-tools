#   This script is a child for DM Tools
#   This script defines the Magic_ItemLookup Child class
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

class Magic_ItemLookup(Lookup):
    def __init__(self, master, magic_item_data):
        Lookup.__init__(self, master)
        
        self.magic_item_data = magic_item_data
        self.canvas = tk.Canvas(self.window, width = WIN_W-18, height = WIN_H, bg=BLACK_BASE, scrollregion= (0, 0, WIN_W-10, WIN_H+2000))
        
        self.scrollbar = tk.Scrollbar(self.window, orient= tk.VERTICAL)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.scrollbar.config(command= self.canvas.yview)
        self.canvas.config(yscrollcommand= self.scrollbar.set)
        self.canvas.pack(side= tk.LEFT, expand= True, fill= tk.BOTH)
        
        name_of_feature = tk.Label(self.window, text= "Magic Item Name:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W//2-43, B_DIST+32, window= name_of_feature, anchor= tk.E)
        self.feature_query = tk.Entry(self.window, width= 20, font= ('times', 16))
        self.canvas.create_window(WIN_W//2-38, B_DIST+30, window= self.feature_query, anchor= tk.W)
        
        self.attributes_var = tk.BooleanVar()
        attribute_button = tk.Checkbutton(self.window, text= 'Search by Attributes', variable= self.attributes_var, onvalue= True, offvalue= False, bg= PURPLE_RED, font= ('times', 12, 'bold'), borderwidth= 3, relief= 'raised')
        self.canvas.create_window(B_DIST, B_DIST, window= attribute_button, anchor= tk.NW)
        Tooltip(attribute_button, text= "When this is enabled the search bar will attempt to match characteristics of the magic item instead of the name\nYou can search by the following characteristics:\nType, Rarity, Attunement, Class, Source\nYou can also attempt to search by:\nRelated Spells, or just text within the description with varied results\nSeparate different characteristics with a \",\"\nSeparate different queries (only one of each will be returned, at random) with a \";\"")
        
        # Extra bins to hold temporary objects
        self.magic_item_displays = []
        self.display_tables = []
        
        lookup_button = tk.Button(self.window, text= 'Lookup Magic Item Info', command= self.genMagicDesc, bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W//2, B_DIST+75, window= lookup_button)
        
        # Create buttons to show "Next" and "Previous" Features
        self.next_button = tk.Button(self.window, text='Next Feature', command= lambda: self.displayNextObject(self.genMagicDesc, True), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2+160, B_DIST+75, window= self.next_button)
        self.prev_button = tk.Button(self.window, text='Previous', command= lambda: self.displayNextObject(self.genMagicDesc, False), bg= BLANK_GRAY, fg= BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2-145, B_DIST+75, window= self.prev_button)
        
        for lookupObject in [self.window, self.canvas, name_of_feature, self.feature_query, lookup_button, self.next_button, self.prev_button]:
            self.setKeyBinds(lookupObject, self.genMagicDesc)
            
        try:
            self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["m_itmLook"]["bg"]))
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.N)
            self.canvas.create_image(0, 1181, image=self.image, anchor=tk.NW)
            self.canvas.create_image(MID_W, 2362, image=self.image, anchor=tk.N)
        except:
            print("Magic Item Lookup Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["m_itmLook"]["bg"] +"\"")
    
    def genMagicDesc(self, found_Magic="", event=None):
        self.resetMagicDisplay()
        if found_Magic == "":
            magic_input = self.feature_query.get().strip().lower()
            if magic_input != "" or self.attributes_var.get():
                if ';' in magic_input:
                    self.user_objects = []
                    query_split = magic_input.split(';')
                    for i in range(len(query_split)):
                        self.user_objects.append(randchoice(self.searchMagicData(query_split[i].lower().strip())))
                else:
                    self.user_objects = sorted(self.searchMagicData(magic_input))
            else:
                all_magicdata = [data for data in self.magic_item_data]
                shuffle(all_magicdata)
                self.user_objects = all_magicdata
            self.user_objects_index = 0
            found_Magic = self.user_objects[self.user_objects_index]
        self.updateNextButton()
        if found_Magic in self.magic_item_data:
            posH = B_DIST+110
            infolines = self.getMagicInfo(self.magic_item_data[found_Magic])
            
            for i in range(len(infolines)):
                self.magic_item_displays.append(tk.Label(self.window, text= "", bg=OFF_WHITE, fg='black', font=('times', 12), wraplength=850, justify="left"))
                self.setKeyBinds(self.magic_item_displays[i], self.genMagicDesc)
            for i in range(len(infolines)):
                if infolines[i][0] == "spacer":
                    posH += infolines[i][1]
                elif infolines[i][0] == "table":
                    temp_tblData = infolines[i][1]
                    temp_Frame = tk.Frame(self.window, bg=OFF_WHITE)
                    self.setKeyBinds(temp_Frame, self.genMagicDesc)
                    default_vars = [False for x in range(6)]
                    var_keys = ["name", "dualLabel", "mode", "anchors", "wraplength", "text"]
                    for y in range(len(var_keys)):
                        if var_keys[y] in temp_tblData:
                            default_vars[y] = temp_tblData[var_keys[y]]
                            if y == 0:
                                posH += 5
                    SmartTable(temp_Frame, temp_tblData["items"], default_vars, lambda a: self.setKeyBinds(a, self.genMagicDesc))
                    tableId = self.canvas.create_window(B_DIST, posH, anchor=tk.NW, window=temp_Frame)
                    self.window.update()
                    posH += temp_Frame.winfo_reqheight() + 5
                    self.display_tables.append(temp_Frame)
                else:
                    if infolines[i][0] == "header":
                        self.magic_item_displays[i].configure(font=("times", 16))
                    elif infolines[i][0] == "subheader":
                        self.magic_item_displays[i].configure(font=("times", 14))
                        if i > 0 and infolines[i-1][0] == "subheader":
                            posH += 5
                    elif infolines[i][0] == "core":
                        self.magic_item_displays[i].configure(font=("times", 14, "italic"))
                    self.magic_item_displays[i].configure(text=infolines[i][1])
                    self.canvas.create_window(B_DIST, posH, window= self.magic_item_displays[i], anchor= tk.NW)
                    posH += self.magic_item_displays[i].winfo_reqheight()
                    if infolines[i][0] in ["text"]:
                        posH += 5
        else:
            self.magic_item_displays.append(tk.Label(self.window, text="Magic Item Info Not Found", bg=OFF_WHITE, fg='black', font=('times', 16), wraplength=780, justify="left"))
            self.canvas.create_window(WIN_W//2, B_DIST+120, window=self.magic_item_displays[0])
        
    def resetMagicDisplay(self):
        for display_object in self.magic_item_displays:
            display_object.destroy()
        for display_table in self.display_tables:
            display_table.destroy()
        self.magic_item_displays = []
        self.display_tables = []
    
    def getMagicInfo(self, found_Magic, subheader=False):
        infolines = []
        headerString = ""
        # Create the header
        if "name" in found_Magic:
            headerString += found_Magic["name"]
        if "source" in found_Magic:
            # Needs header/subheader format
            headerString += " (" + found_Magic["source"][0] + ", " + str(found_Magic["source"][1]) + ")"
        if headerString:
            if not subheader:
                infolines.append(["header", headerString])
            else:
                infolines.append(["subheader", headerString])
        # Handle the core information
        core_info = ""
        if "typeString" in found_Magic:
            core_info += found_Magic["typeString"]
        if "rarity" in found_Magic:
            if core_info: core_info += ", "
            core_info += found_Magic["rarity"]
        if "attunement" in found_Magic:
            if isinstance(found_Magic["attunement"], str):
                core_info += f" ({found_Magic['attunement']})"
            else:
                core_info += " (requires attunement)"
        if core_info:
            # Change prereq tag to core
            infolines.append(["core", core_info])
        # Text before the table or statblock
        if "description" in found_Magic:
            if not subheader:
                infolines.append(["subheader", found_Magic["description"]])
            else:
                infolines.append(["text", found_Magic["description"]])
        # Table
        if "table" in found_Magic:
            if isinstance(found_Magic["table"], dict):
                infolines.append(["table", found_Magic["table"]])
            elif isinstance(found_Magic["table"], list):
                for found_table in found_Magic["table"]:
                    infolines.append(["table", found_table])
        # Statblock
        if "statblock" in found_Magic:
            infolines.append(["spacer", 10])
            infolines.append(["subheader", found_Magic["statblock"]["name"]]),
            for entry in found_Magic["statblock"]["entries"]:
                infolines.append(["text", found_Magic["statblock"]["entries"][entry]])
            infolines.append(["spacer", 5])
        # Text after the table or statblock
        if "extra description" in found_Magic:
            if not subheader:
                infolines.append(["subheader", found_Magic["extra description"]])
            else:
                infolines.append(["text", found_Magic["extra description"]])
        # Table after extra description
        if "extra table" in found_Magic:
            if isinstance(found_Magic["extra table"], dict):
                infolines.append(["table", found_Magic["extra table"]])
            elif isinstance(found_Magic["extra table"], list):
                for found_table in found_Magic["extra table"]:
                    infolines.append(["table", found_table])
        # Iterate through the features of the object
        if "features" in found_Magic:
            if "feature_header" in found_Magic:
                infolines.append(["header", found_Magic["feature_header"]])
            for feature in found_Magic["features"]:
                if feature == "exclude":
                    pass
                else:
                    for feature_line in self.getMagicInfo(found_Magic["features"][feature], True):
                        infolines.append(feature_line)
        return infolines
    
    def searchMagicData(self, magic_input):
        attributes = self.attributes_var.get()
        all_magicdata = [data for data in self.magic_item_data]
        shuffle(all_magicdata)
        if magic_input == "":
            return all_magicdata
        
        if attributes:
            filter_Input = set(filter_in.strip().lower() for filter_in in magic_input.split(","))
            # convert attunement
            if "attune" in filter_Input:
                filter_Input.remove("attune")
                filter_Input.add("attunement")
            # convert source abbreviations
            source_add = set()
            source_remove = set()
            for f_Input in filter_Input:
                if f_Input in sources_dict:
                    source_add.add(sources_dict[f_Input].lower())
                    source_remove.add(f_Input)
            for s_add in source_add:
                filter_Input.add(s_add)
            for s_remove in source_remove:
                filter_Input.remove(s_remove)
            found_magic_list = []
            
            priority_attributes = ["type", "subtype", "rarity", "attunement", "prereq"]
            temp_priority = {}
            priority_filters = {}
            for magic in all_magicdata:
                priority_clump = set()
                if "source" in self.magic_item_data[magic]:
                    priority_clump.add(self.magic_item_data[magic]["source"][0].lower())
                for priority in priority_attributes:
                    if priority in self.magic_item_data[magic]:
                        if priority == "attunement":
                            priority_clump.add("attunement")
                        elif priority in ["prereq", "subtype"]:
                            for iter_item in self.magic_item_data[magic][priority]:
                                priority_clump.add(iter_item.lower())
                        else:
                            priority_clump.add(self.magic_item_data[magic][priority].lower())
                temp_priority[magic] = priority_clump
                if filter_Input.issubset(priority_clump):
                    found_magic_list.append(magic)
                for f_Input in filter_Input:
                    if f_Input in priority_clump:
                        priority_filters[f_Input] = True
            if found_magic_list:
                return found_magic_list
            else:
                for magic in all_magicdata:
                    secondary_clump = ""
                    if "description" in self.magic_item_data[magic]:
                        secondary_clump += self.magic_item_data[magic]["description"]
                    if "extra description" in self.magic_item_data[magic]:
                        secondary_clump += self.magic_item_data[magic]["extra description"]
                    filter_check = []
                    for f_Input in filter_Input:
                        if f_Input in temp_priority[magic] or (f_Input in secondary_clump and f_Input not in priority_filters):
                            filter_check.append(True)
                        else:
                            filter_check.append(False)
                    if all(filter_check):
                        found_magic_list.append(magic)
                if found_magic_list:
                    return found_magic_list
            return [magic_input]
        
        if magic_input in all_magicdata:
            found_feature_list = [magic_input]
            all_magicdata.remove(magic_input)
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
        
        clean_input = clean(magic_input)
        # Check if the Input matches part of a name of a data
        for data in all_magicdata:
            if (clean_input in clean(data)):
                found_feature_list.append(data)
        all_magicdata = prevent_dups(found_feature_list, all_magicdata)
        
        # Run a more advanced search on each data name to check if the error is due to spaces or a typo, also functions as a guess to what data is being typed
        for data in all_magicdata:
            # Remove specific non ascii characters from both strings while doing this check
            if (len(magic_input) <= len(data) + 1) and (self.spellcheck(clean_input, clean(data)) <= 1):
                found_feature_list.append(data)
        all_magicdata = prevent_dups(found_feature_list, all_magicdata)
        
        # If the input matches, or if nothing was found, return the original input as a list
        if found_feature_list:
            return found_feature_list
        else:
            return [magic_input]