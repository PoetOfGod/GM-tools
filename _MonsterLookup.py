#   This script is a child for DM Tools
#   This script defines the MonsterLookup Child class
#
# Import required libraries
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from random import choice as randchoice, shuffle
from re import findall
# Load config
from ___Config import *
# Load parent scripts
from __Lookup import *
from __Custom import CustomMonster
from __ImageDisplay import *
from __Tooltip import *

class MonsterLookup(Lookup, CustomMonster):
    def __init__(self, master, monster_data):
        Lookup.__init__(self, master)
        self.monster_data = monster_data
        self.canvas = tk.Canvas(self.window, width = WIN_W-18, height = WIN_H, scrollregion= (0, 0, WIN_W-10, WIN_H+1600))
        
        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        name_of_monster = tk.Label(self.window, text= "Name of Monster:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W//2-43, B_DIST+32, window= name_of_monster, anchor= tk.E)
        self.monster_query = tk.Entry(self.window, width= 20, font= ('times', 16))
        self.canvas.create_window(WIN_W//2-38, B_DIST+30, window= self.monster_query, anchor= tk.W)
        
        self.attributes_var = tk.BooleanVar()
        attribute_button = tk.Checkbutton(self.window, text= 'Search by Attributes', variable= self.attributes_var, onvalue= True, offvalue= False, bg= ORANGE, font= ('times', 12, 'bold'), borderwidth= 3, relief= 'raised')
        self.canvas.create_window(B_DIST, B_DIST, window= attribute_button, anchor= tk.NW)
        Tooltip(attribute_button, text= "When this is enabled the search bar will attempt to match characteristics of the monster instead of the name\nYou can search by the following characteristics:\nSize, Type, Subtype, Alignment, and Challenge Rating\nYou can also attempt to search by:\nSpeed, Senses, Languages, Traits, Actions, Bonus Actions, Reactions, Legendary Actions, and Mythic Actions, with varied results\nSeparate different characteristics with a \",\"\nSeparate different queries (only one of each will be returned, at random) with a \";\"")
        
        # Create a popup prefilled with the current monster information, or an empty popup if there's no monster
        CustomMonster.__init__(self, master)
        
        # Create a button to display the current monster image
        if MONSTER_IMAGES:
            self.show_image_button = tk.Button(self.window, text='Show Image', bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'), state='disabled')
            self.canvas.create_window(B_DIST, B_DIST+70, window= self.show_image_button, anchor= tk.NW)
            Tooltip(self.show_image_button, text= "Opens a separate window with an image of the monster currently displayed\nIf this button is greyed out then no image is available")
        
        # Create the "Add to Initiative" button, the command will be changed later by DM_Tools_main
        self.addMontoInit_Button = tk.Button(self.window, text= 'Add to Initiative', bg= MUDDY_ORANGE, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W-(B_DIST*2), B_DIST, anchor= tk.NE, window= self.addMontoInit_Button)
        Tooltip(self.addMontoInit_Button, text= "Sends the currently displayed monster to the Initiative Tracker\nThe Name, Health, and Armor Class will fill automatically")
        
        # Create a toggle to roll for the monster's initiative when adding to initiative
        self.addMontoInit_InitToggle = tk.BooleanVar()
        InitToggle_box = tk.Checkbutton(self.window, text= 'Roll Init', variable= self.addMontoInit_InitToggle, onvalue= True, offvalue= False, bg= ORANGE, font= ('times', 12, 'bold'), borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W-(B_DIST*2), B_DIST+36, window= InitToggle_box, anchor= tk.NE)
        
        # Create a toggle to roll for the monster's health when adding to initiative
        self.addMontoInit_HPToggle = tk.BooleanVar()
        HPToggle_box = tk.Checkbutton(self.window, text= 'Roll HP', variable= self.addMontoInit_HPToggle, onvalue= True, offvalue= False, bg= ORANGE, font= ('times', 12, 'bold'), borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W-(B_DIST*2 + 90), B_DIST+36, window= HPToggle_box, anchor= tk.NE)
        
        # Create the "Lookup Spells" button, the command will be changed later by DM_Tools_main
        self.lookupMonSpells_Button = tk.Button(self.window, text= 'Lookup Spells', bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W-(B_DIST*2), B_DIST+70, anchor= tk.NE, window= self.lookupMonSpells_Button)
        Tooltip(self.lookupMonSpells_Button, text= "Sends any spells referenced by the monster to the Spell Lookup\nIf no spells are referenced then nothing will occur")
        
        # Create labels to fill with the monster information
        self.monster_displays = []
        for i in range(35):
            temp_label = tk.Label(self.window, text= "", bg= SCROLL_TAN, fg= BLACK_BASE, font= ('times', 16), wraplength= 850, justify= "left")
            self.monster_displays.append(temp_label)
        
        self.display_dividers = []
        
        lookup_button = tk.Button(self.window, text= 'Lookup Monster', command= self.genMonsterDesc, bg= BLUE_PURPLE, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(WIN_W//2, B_DIST+75, window= lookup_button)
        
        # Create buttons to show "Next" and "Previous" Monsters
        self.next_button = tk.Button(self.window, text='Next Monster', command= lambda: self.displayNextObject(self.genMonsterDesc, True), bg= BLANK_GRAY, fg=BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2 +130, B_DIST+75, window= self.next_button)
        self.prev_button = tk.Button(self.window, text='Previous', command= lambda: self.displayNextObject(self.genMonsterDesc, False), bg= BLANK_GRAY, fg=BLACK_BASE, font=('book antiqua', 12, 'italic', 'bold'))
        self.canvas.create_window(WIN_W//2 -115, B_DIST+75, window= self.prev_button)
        
        for lookupObject in [self.window, self.canvas, name_of_monster, self.monster_query, lookup_button, self.next_button, self.prev_button]:
            self.setKeyBinds(lookupObject, self.genMonsterDesc)
        for labelObject in self.monster_displays:
            self.setKeyBinds(labelObject, self.genMonsterDesc)
        
        try:
            self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["monLook"]["bg"]))
            self.canvas.create_image(0, 0, image= self.image, anchor= tk.N)
            self.canvas.create_image(0, 1320, image= self.image, anchor= tk.NW)
        except:
            print("Monster Lookup Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["monLook"]["bg"] +"\"")
    
    def genMonsterDesc(self, found_Monster="", event=None):
        self.resetMonsterDisplay()
        if found_Monster == "":
            monster_input = self.monster_query.get().strip().lower()
            if monster_input == "" and self.attributes_var.get():
                self.user_objects = sorted(self.searchMonsters(monster_input))
                self.user_objects_index = 0
            elif monster_input != "":
                if ';' in monster_input:
                    self.user_objects = []
                    query_split = monster_input.split(';')
                    for i in range(len(query_split)):
                        self.user_objects.append(randchoice(self.searchMonsters(query_split[i].lower().strip(), True)))
                        self.user_objects_index = 0
                else:
                    check_existing = self.searchMonsters(monster_input)
                    user_intersection = [monster for monster in check_existing if monster in self.user_objects]
                    if user_intersection:
                        intersection_index = self.user_objects.index(user_intersection[0])
                        self.user_objects_index = intersection_index
                    else:
                        shuffle(check_existing)
                        self.user_objects = check_existing
                        self.user_objects_index = 0
            else:
                all_monsters = [monster for monster in self.monster_data]
                shuffle(all_monsters)
                self.user_objects = all_monsters
                self.user_objects_index = 0
            found_Monster = self.user_objects[self.user_objects_index]
        self.updateNextButton()
        if found_Monster in self.monster_data:
            posH = B_DIST+110
            infolines = self.getMonsterInfo(self.monster_data[found_Monster])
            for i in range(len(infolines)):
                if infolines[i] == "##Insert Divider##":
                    ##Insert Divider##
                    posH += 5
                    divider = self.canvas.create_rectangle(B_DIST, posH, B_DIST+600, posH+5, fill= BRIGHT_RED)
                    self.display_dividers.append(divider)
                    posH += 10
                elif infolines[i] != "":
                    self.monster_displays[i].configure(text=infolines[i])
                    self.canvas.create_window(B_DIST, posH, window= self.monster_displays[i], anchor= tk.NW)
                    posH += self.monster_displays[i].winfo_reqheight()
            if MONSTER_IMAGES:
                the_Monster = self.monster_data[found_Monster]
                if "hasFluffImages" in the_Monster:
                    if the_Monster["name"].endswith("  (Custom)"):
                        self.show_image_button.config(state= 'normal', command= lambda: self.show_monster_image(the_Monster["name"], "Custom"))
                    elif "source" in the_Monster:
                        self.show_image_button.config(state= 'normal', command= lambda: self.show_monster_image(the_Monster["name"], the_Monster["source"][0], the_Monster["hasFluffImages"]))
                else:
                    self.show_image_button.config(state='disabled')
        else:
            self.monster_displays[0].configure(text="Monster Not Found")
            self.canvas.create_window(WIN_W//2, B_DIST+120, window= self.monster_displays[0])
            if MONSTER_IMAGES:
                self.show_image_button.config(state='disabled')
    
    def resetMonsterDisplay(self):
        for monster_label in self.monster_displays:
            monster_label.configure(text="")
            monster_label_id = self.canvas.create_window(WIN_W//2, B_DIST+120, window= monster_label)
            self.canvas.itemconfigure(monster_label_id, state='hidden')
        for divider in self.display_dividers:
            self.canvas.delete(divider)
    
    def searchMonsters(self, monster_input, inputList=False):
        attributes = self.attributes_var.get()
        all_monsters = [monster for monster in self.monster_data]
        shuffle(all_monsters)
        if attributes and monster_input != "":
            filter_Input = set(filter_in.strip().lower() for filter_in in monster_input.split(","))
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
            found_monster_list = []
            
            priority_attributes = ["size", "type", "subtype", "alignment", "cr"]
            temp_priority = {}
            priority_filters = {}
            for monster in all_monsters:
                priority_clump = set()
                if "source" in self.monster_data[monster]:
                    priority_clump.add(self.monster_data[monster]["source"][0].lower())
                for priority in priority_attributes:
                    if priority in self.monster_data[monster]:
                        priority_clump.add(self.monster_data[monster][priority].lower())
                temp_priority[monster] = priority_clump
                if filter_Input.issubset(priority_clump):
                    found_monster_list.append(monster)
                for f_Input in filter_Input:
                    if f_Input in priority_clump:
                        priority_filters[f_Input] = True
            if found_monster_list:
                return found_monster_list
            else:
                secondary_attributes = ["speed", "senses", "languages", "traits", "actions", "bonus", "reactions", "legendary", "mythic"]
                for monster in all_monsters:
                    secondary_clump = ""
                    for secondary in secondary_attributes:
                        if secondary in self.monster_data[monster]:
                            secondary_clump += self.monster_data[monster][secondary].lower()
                    filter_check = []
                    for f_Input in filter_Input:
                        if f_Input in temp_priority[monster] or (f_Input in secondary_clump and f_Input not in priority_filters):
                            filter_check.append(True)
                        else:
                            filter_check.append(False)
                    if all(filter_check):
                        found_monster_list.append(monster)
                if found_monster_list:
                    return found_monster_list
                 
        elif monster_input not in self.monster_data:
            clean_input = monster_input.replace(' ', '').replace('\'', '').replace('-', '')
            # Check if the Input matches part of a name of a monster
            found_monster_list = []
            for monster in all_monsters:
                if (clean_input in monster.replace(' ', '').replace('\'', '').replace('-', '')):
                    found_monster_list.append(monster)
            if found_monster_list:
                return found_monster_list

            # Run a more advanced search on each monster name to check if the error is due to spaces or a typo, also functions as a guess to what monster is being typed
            for monster in all_monsters:
                if (len(monster_input) <= len(monster) + 1) and (self.spellcheck(clean_input, monster.replace(' ', '').replace('\'', '').replace('-', '')) <= 1):
                    # Remove specific non ascii characters from both strings
                    found_monster_list.append(monster)
            if found_monster_list:
                return found_monster_list
        # Return both spells if a spell has the same name followed by ", old version", unless the search input includes multiple monsters
        elif monster_input + ", old version" in self.monster_data and not inputList:
            return [monster_input, monster_input + ", old version"]
        # If the input matches, or if nothing was found, return the original input as a list
        return [monster_input]
    
    def getMonsterInfo(self, monster_object):
        infolines = ["" for i in range(35)]
        j = 0
        infolines[j] = monster_object["name"]
        def fA(a):
            return True if a in monster_object else False
        if "source" in monster_object:
            infolines[j] += "  ("
            infolines[j] += monster_object["source"][0]
            infolines[j] += ", "
            infolines[j] += monster_object["source"][1]
            infolines[j] += ")"
        j += 1
        if [c for c in filter(fA, ["size", "type", "subtype", "alignment"])]:
            if "size" in monster_object:
                infolines[j] += monster_object["size"] + " "
            if "type" in monster_object:
                infolines[j] += monster_object["type"]
            if "subtype" in monster_object:
                infolines[j] += " (" + monster_object["subtype"] + ")"
            if "alignment" in monster_object:
                if infolines[j]:
                    infolines[j] += ", "
                infolines[j] += monster_object["alignment"]
            j += 1
        infolines[j] = "##Insert Divider##"
        j += 1
        if [c for c in filter(fA, ["acString", "hp", "speed"])]:
            if "acString" in monster_object:
                infolines[j] += "Armor Class: " + monster_object["acString"]
                j += 1
            if "hp" in monster_object:
                infolines[j] += "Hit Points: " + str(monster_object["hp"])
                if "hpFormula" in monster_object:
                    infolines[j] += " (" + monster_object["hpFormula"] + ")"
                j += 1
            if "speed" in monster_object:
                infolines[j] += "Speed: " + monster_object["speed"]
                j += 1
            infolines[j] = "##Insert Divider##"
            j += 1
        if "scores" in monster_object:
            infolines[j] += "  STR\t  DEX\t  CON\t  INT\t  WIS\t  CHA\n"
            for score in monster_object["scores"]:
                score_mod = (monster_object["scores"][score]-10) // 2
                if score_mod >= 0:
                    score_mod = "+" + str(score_mod)
                else:
                    score_mod = str(score_mod)
                infolines[j] += str(monster_object["scores"][score]) + " (" + score_mod + ")\t"
            j += 1
            infolines[j] = "##Insert Divider##"
            j += 1
        if [c for c in filter(fA, ["saves", "skills", "senses", "resist", "vulnerable", "immune", "conditionImmune", "languages", "cr"])]:
            if "saves" in monster_object:
                infolines[j] += "Saves: " + monster_object["saves"]
                j += 1
            if "skills" in monster_object:
                infolines[j] += "Skills: " + monster_object["skills"]
                j += 1
            if "senses" in monster_object:
                infolines[j] += "Senses: " + monster_object["senses"]
                j += 1
            if "resist" in monster_object:
                infolines[j] += "Damage Resistances: " + monster_object["resist"]
                j += 1
            if "vulnerable" in monster_object:
                infolines[j] += "Damage Vulnerabilities: " + monster_object["vulnerable"]
                j += 1
            if "immune" in monster_object:
                infolines[j] += "Damage Immunities: " + monster_object["immune"]
                j += 1
            if "conditionImmune" in monster_object:
                infolines[j] += "Condition Immunities: " + monster_object["conditionImmune"]
                j += 1
            if "languages" in monster_object:
                infolines[j] += "Languages: " + monster_object["languages"]
                j += 1
            if "cr" in monster_object:
                infolines[j] += "Challenge Rating: " + monster_object["cr"]
                j += 1
            infolines[j] = "##Insert Divider##"
            j += 1
        if [c for c in filter(fA, ["traits", "spellcasting"])]:
            if "traits" in monster_object:
                infolines[j] += monster_object["traits"]
                j += 1
            if "spellcasting" in monster_object:
                infolines[j] += monster_object["spellcasting"]
                j += 1
            if [c for c in filter(fA, ["actions", "bonus", "reactions", "legendary", "mythic"])]:
                infolines[j] = "##Insert Divider##"
                j += 1
        if "actions" in monster_object:
            infolines[j] = "Actions______________________________________"
            j += 1
            infolines[j] = monster_object["actions"]
            j += 1
            if [c for c in filter(fA, ["bonus", "reactions", "legendary", "mythic"])]:
                infolines[j] = "##Insert Divider##"
                j += 1
        if "bonus" in monster_object:
            infolines[j] = "Bonus Actions________________________________"
            j += 1
            infolines[j] = monster_object["bonus"]
            j += 1
            if [c for c in filter(fA, ["reactions", "legendary", "mythic"])]:
                infolines[j] = "##Insert Divider##"
                j += 1
        if "reactions" in monster_object:
            infolines[j] = "Reactions_____________________________________"
            j += 1
            infolines[j] = monster_object["reactions"]
            j += 1
            if [c for c in filter(fA, ["legendary", "mythic"])]:
                infolines[j] = "##Insert Divider##"
                j += 1
        if "legendary" in monster_object:
            infolines[j] = "Legendary Actions____________________________"
            j += 1
            infolines[j] = monster_object["legendary"]
            j += 1
            if "mythic" in monster_object:
                infolines[j] = "##Insert Divider##"
                j += 1
        if "mythic" in monster_object:
            infolines[j] = "Mythic Legendary Actions_____________________"
            j += 1
            infolines[j] = monster_object["mythic"]
        return infolines
            
    def show_monster_image(self, name, source, path_ext=""):
        # Load the image
        if name.endswith(", Old Version"):
            name = name[:-13]
        # Load custom monster images from the dynamic folder
        if name.endswith("  (Custom)"):
            name = name[:-10]
            image_path = f"dynamic/profiles/{self.current_profile}/custom_monster_img/" + name + ".webp"
        else:
            image_path = "data/monster/monster_img/" + path_ext + ".webp"
        try:
            original_image = Image.open(image_path)
        except:
            self.show_image_button.config(state='disabled')
            return
        geometry = f"{original_image.width+17}x{original_image.height+17}"
        popup = ImageWindow(tk.Toplevel(self.window), path=image_path, winSize=geometry, title=name)