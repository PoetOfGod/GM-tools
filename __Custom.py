#   This script is a child for DM Tools
#   This script defines the CustomMonster and CustomSpell Parent classes
#   These classes are dependent on running within their child environments
#   They are aggregated here solely for readability
#
# Import required libraries
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from random import choice as randchoice, shuffle
from re import findall
from json import load
import sys
# Load config
from ___Config import *
from __Tooltip import *

class CustomMonster:
    def __init__(self, master):
        self.setProfile()
        self.customize_button = tk.Button(self.window, text='Customize', command= self.enableCustomize, bg= BLUE_PURPLE, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(B_DIST, B_DIST+33, window= self.customize_button, anchor= tk.NW)
        Tooltip(self.customize_button, text="Opens the Create a Custom Monster window\nThe monster currently displayed will be automatically ported into the Custom Monster window to use as a base\nIf no monster is displayed, all fields will initially be empty\nCustom Monsters will be saved across multiple sessions, and can be referenced immediately")
        self.createCustomPopup()
    
    def setProfile(self, profile=DEFAULT_PROFILE, startup=True):
        self.current_profile = profile
        if not startup:
            self.unloadCustom()
        self.loadCustom()
    
    def loadCustom(self):
        with open(f"dynamic/profiles/{self.current_profile}/customMonsters.json", encoding='utf-8') as f:
            self.custom_monster_data = {}
            # Import custom monsters
            file_data = load(f)
            for monster in file_data:
                if not getattr(sys, 'frozen', False):
                    if monster in self.monster_data:
                        print(f"Duplicated Import with {monster}")
                        try:
                            print("Monster Sources: ", end= "")
                            print(self.monster_data[monster]["source"], end= ", ")
                            print(file_data[monster]["source"])
                        except:
                            pass
                self.monster_data[monster] = file_data[monster]
                self.custom_monster_data[monster] = file_data[monster]
    
    def unloadCustom(self):
        for custom_monster in self.custom_monster_data:
            if custom_monster in self.monster_data:
                del self.monster_data[custom_monster]
    
    def enableCustomize(self):
        self.customPopup.deiconify()
        # Autofill the customPopup fields with the current spell, if possible
        if len(self.user_objects) == 0:
            return
        current_monster = self.user_objects[self.user_objects_index]
        if current_monster not in self.monster_data:
            return
        cfb = self.customFieldBuckets
        if cfb[0]["get"](cfb[0]["content"]) != "":
            if not messagebox.askyesno(title=f"Overwrite the Current Custom Monster?", message=f"Warning: There is a monster in the Customize Dialogue.\n   The Current Custom Monster " + cfb[0]["get"](cfb[0]["content"]) + " will be lost if you have not saved it.", parent= self.customPopup):
                return
        self.clearCustom()
        fields = ["name", "cr", "size", "type", "subtype", "acString", "alignment", "hp", "speed", "str", "dex", "con", "int", "wis", "cha", "saves", "skills", "senses", "languages", "resist", "immune", "vulnerable", "conditionImmune", "traits", "spellcasting", "spells", "actions", "bonus", "reactions", "legendary", "mythic"]
        for i in range(len(cfb)):
            if fields[i] == "name" and self.monster_data[current_monster]["name"].endswith("  (Custom)"):
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster][fields[i]][:-10])
                continue
            if fields[i] in ["str", "dex", "con", "int", "wis", "cha"]:
                if "scores" not in self.monster_data[current_monster]:
                    continue
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster]["scores"][fields[i]])
                continue
            if fields[i] not in self.monster_data[current_monster]:
                continue
            if fields[i] == "hp":
                current_monster_hp = str(self.monster_data[current_monster]["hp"])
                if "hpFormula" in self.monster_data[current_monster]:
                    current_monster_hp += " (" + self.monster_data[current_monster]["hpFormula"] + ")"
                cfb[i]["insert"](cfb[i]["content"], current_monster_hp)
            elif fields[i] == "spells":
                current_monster_spells = ", ".join([spellName.title() for spellName in self.monster_data[current_monster]["spells"]])
                cfb[i]["insert"](cfb[i]["content"], current_monster_spells)
            else:
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster][fields[i]])
    
    def createCustomPopup(self):
        popupColor = BLANK_GRAY
        # Refactor
        self.customPopup = tk.Toplevel(self.window)
        self.customPopup.configure(bg=popupColor)
        self.customPopup.title("Create a Custom Monster")
        self.customCanvas = tk.Canvas(self.customPopup, width = WIN_W, height = WIN_H, bg= popupColor)
        self.customCanvas.pack()
        self.customMenu = tk.Menu(self.customPopup)
        self.customPopup.config(menu= self.customMenu)
        self.customMenu.add_command(label="Save", command=self.saveCustom)
        self.customMenu.add_command(label="Clear", command=self.clearCustom)
        self.customMenu.add_command(label="Delete", command=self.deleteCustom)
        self.customMenu.add_command(label="Exit", command=self.customPopup.withdraw)
        if not MONSTER_CUSTOM_DROPDOWNS:
            monster_sizes = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
            mon_size_def = "Medium"
            monster_types = ["Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead"]
            mon_type_def = "Humanoid"
        else:
            monster_sizes = MONSTER_CUSTOM_SIZE_DROPDOWN
            mon_size_def = MONSTER_CUSTOM_SIZE_DEFAULT
            monster_types = MONSTER_CUSTOM_TYPE_DROPDOWN
            mon_type_def = MONSTER_CUSTOM_TYPE_DEFAULT
        # Position variables for easier consistent formatting
        LFactor = 27
        WFactor = 155
        custom_fields = [
            {"label" : "Name:",                 "type" : "Entry", "len" : 40, "x" : WFactor, "y" : B_DIST-10},
            {"label" : "Challenge Rating:",     "type" : "Entry", "len" : 5, "x" : WFactor+455, "y" : B_DIST-10},
            {"label" : "Size:",                 "type" : "Dropdown", "list" : monster_sizes, "default" : mon_size_def, "x" : WFactor, "y" : B_DIST+LFactor-10},
            {"label" : "Type:",                 "type" : "Dropdown", "list" : monster_types, "default" : mon_type_def, "x" : WFactor+160, "y" : B_DIST+LFactor-10},
            {"label" : "Subtype:",              "type" : "Entry", "len" : 20, "x" : WFactor+345, "y" : B_DIST+LFactor-10},
            {"label" : "Armor Class:",          "type" : "Entry", "len" : 35, "x" : WFactor, "y" : B_DIST+LFactor*2},
            {"label" : "Alignment:",            "type" : "Entry", "len" : 20, "x" : WFactor+370, "y" : B_DIST+LFactor*2},
            {"label" : "Hit Points",            "type" : "Entry", "len" : 20, "x" : WFactor, "y" : B_DIST+LFactor*3},
            {"label" : "Speed:",                "type" : "Entry", "len" : 40, "x" : WFactor+205, "y" : B_DIST+LFactor*3},
            {"label" : "Strength:",             "type" : "Entry", "len" : 4, "x" : WFactor, "y" : B_DIST+LFactor*4},
            {"label" : "Dexterity:",            "type" : "Entry", "len" : 4, "x" : WFactor+110, "y" : B_DIST+LFactor*4},
            {"label" : "Constitution:",         "type" : "Entry", "len" : 4, "x" : WFactor+240, "y" : B_DIST+LFactor*4},
            {"label" : "Intelligence:",         "type" : "Entry", "len" : 4, "x" : WFactor+370, "y" : B_DIST+LFactor*4},
            {"label" : "Wisdom:",               "type" : "Entry", "len" : 4, "x" : WFactor+470, "y" : B_DIST+LFactor*4},
            {"label" : "Charisma:",             "type" : "Entry", "len" : 4, "x" : WFactor+580, "y" : B_DIST+LFactor*4},
            {"label" : "Saves:",                "type" : "Entry", "len" : 40, "x" : WFactor, "y" : B_DIST+LFactor*5},
            {"label" : "Skills:",               "type" : "Entry", "len" : 40, "x" : WFactor+380, "y" : B_DIST+LFactor*5},
            {"label" : "Senses:",               "type" : "Entry", "len" : 45, "x" : WFactor, "y" : B_DIST+LFactor*6},
            {"label" : "Languages:",            "type" : "Entry", "len" : 30, "x" : WFactor+455, "y" : B_DIST+LFactor*6},
            {"label" : "Resistance:",           "type" : "Entry", "len" : 90, "x" : WFactor, "y" : B_DIST+LFactor*7},
            {"label" : "Immune:",               "type" : "Entry", "len" : 40, "x" : WFactor, "y" : B_DIST+LFactor*8},
            {"label" : "Vulnerable:",           "type" : "Entry", "len" : 39, "x" : WFactor+410, "y" : B_DIST+LFactor*8},
            {"label" : "Condition Immunities:", "type" : "Entry", "len" : 90, "x" : WFactor, "y" : B_DIST+LFactor*9},
            {"label" : "Traits:",               "type" : "Text", "w" : 90, "h" : 5, "x" : WFactor, "y" : B_DIST+LFactor*10},
            {"label" : "Spellcasting:",         "type" : "Text", "w" : 90, "h" : 3, "x" : WFactor, "y" : B_DIST+LFactor*14-5},
            {"label" : "Spells:",               "type" : "Text", "w" : 90, "h" : 1, "x" : WFactor, "y" : B_DIST+LFactor*16},
            {"label" : "Actions",               "type" : "Text", "w" : 90, "h" : 5, "x" : WFactor, "y" : B_DIST+LFactor*17},
            {"label" : "Bonus Actions",         "type" : "Text", "w" : 90, "h" : 3, "x" : WFactor, "y" : B_DIST+LFactor*21-5},
            {"label" : "Reactions",             "type" : "Text", "w" : 90, "h" : 3, "x" : WFactor, "y" : B_DIST+LFactor*23+5},
            {"label" : "Legendary Actions",     "type" : "Text", "w" : 90, "h" : 6, "x" : WFactor, "y" : B_DIST+LFactor*25+15},
            {"label" : "Mythic Actions",        "type" : "Text", "w" : 90, "h" : 4, "x" : WFactor, "y" : B_DIST+LFactor*30+3}
        ]
        def expand_custom_text(widget, index):
            expanded_height= 33
            if widget.expanded:
                # Widget is already expanded, shrink widget and unhide any hidden fields
                widget.configure(height= widget.height)
                self.customFieldBuckets[index]["contentID"] = self.customCanvas.create_window(widget.xy[0], widget.xy[1], window= widget, anchor= tk.NW)
                widget.expanded = False
                for i in range(23, 31):
                    if i != index:
                        self.customFieldBuckets[i]["expand"].configure(state= 'normal')
                        self.customCanvas.itemconfigure(self.customFieldBuckets[i]["contentID"], state= 'normal')
                        self.customCanvas.itemconfigure(self.cFB_Labels[i], state= 'normal')
            else:
                for i in range(23, 31):
                    if i != index:
                        self.customFieldBuckets[i]["expand"].configure(state= 'disabled')
                        self.customCanvas.itemconfigure(self.customFieldBuckets[i]["contentID"], state= 'hidden')
                        self.customCanvas.itemconfigure(self.cFB_Labels[i], state= 'hidden')
                widget.configure(height= expanded_height)
                self.customFieldBuckets[index]["contentID"] = self.customCanvas.create_window(WFactor, B_DIST+LFactor*10, window= widget, anchor= tk.NW)
                widget.expanded = True
        self.customFieldBuckets = []
        self.cFB_Labels = []
        for i in range(len(custom_fields)):
            field_name = tk.Label(self.customCanvas, text=custom_fields[i]["label"], bg=popupColor, fg=BLACK_BASE, font='Times 12 bold', anchor='ne')
            cFB_LabelID = self.customCanvas.create_window(custom_fields[i]["x"], custom_fields[i]["y"], window= field_name, anchor= tk.NE)
            self.cFB_Labels.append(cFB_LabelID)
            modeToggle = custom_fields[i]["type"]
            if modeToggle == "Entry":
                field_content = tk.Entry(self.customCanvas, width=custom_fields[i]["len"], font='Times 12')
                self.customCanvas.create_window(custom_fields[i]["x"], custom_fields[i]["y"], window= field_content, anchor= tk.NW)
                self.customFieldBuckets.append({"content" : field_content, "get" : lambda a: a.get().strip(), "insert" : lambda a, b: a.insert(0, b), "delete" : lambda a: a.delete(0, tk.END)})
            elif modeToggle == "Dropdown":
                field_content = tk.StringVar()
                field_content.set(custom_fields[i]["default"])
                field_menu = tk.OptionMenu(self.customCanvas, field_content, *custom_fields[i]["list"])
                field_menu.config(bg=popupColor, fg=BLACK_BASE, font='Times 12')
                field_menu["menu"].config(bg=popupColor, fg=BLACK_BASE, font='Times 12')
                self.customCanvas.create_window(custom_fields[i]["x"], custom_fields[i]["y"], window= field_menu, anchor= tk.NW)
                # Homogenize the required functions so that the fields can be referenced iteratively later on
                self.customFieldBuckets.append({"content" : field_content, "get" : lambda a: a.get(), "insert" : lambda a, b: a.set(b), "delete" : lambda a, c: a.set(c), "default" : custom_fields[i]["default"]})
            elif modeToggle == "Text":
                field_content = tk.Text(self.customCanvas, bg= OFF_WHITE, fg= BLACK_BASE, font= ('times', 12), width= custom_fields[i]["w"], height= custom_fields[i]["h"], wrap= tk.WORD)
                field_content.expanded = False
                field_content.height = custom_fields[i]["h"]
                field_content.xy = [custom_fields[i]["x"], custom_fields[i]["y"]]
                fc_ID = self.customCanvas.create_window(custom_fields[i]["x"], custom_fields[i]["y"], window= field_content, anchor= tk.NW)
                
                field_expand = tk.Button(self.customCanvas, text= '+', bg= popupColor, fg= BLACK_BASE, font= ('Arial', 8), borderwidth= 3, relief= 'raised')
                self.customCanvas.create_window(WFactor+730, custom_fields[i]["y"], window=field_expand, anchor= tk.NW)
                
                # Homogenize the required functions so that the fields can be referenced iteratively later on
                self.customFieldBuckets.append({"content" : field_content, "get" : lambda a: a.get(1.0, tk.END).strip(), "insert" : lambda a, b: a.insert(1.0, b), "delete" : lambda a: a.delete(1.0, tk.END), "expand" : field_expand, "contentID" : fc_ID})
        # Manually assign the text expansion since it doesn't want to be integrated using a loop
        # Refactor once I figure out why it is so annoying about this
        cfb = self.customFieldBuckets
        cfb[23]["expand"].configure(command= lambda: expand_custom_text(cfb[23]["content"], 23))
        cfb[24]["expand"].configure(command= lambda: expand_custom_text(cfb[24]["content"], 24))
        cfb[25]["expand"].configure(command= lambda: expand_custom_text(cfb[25]["content"], 25))
        cfb[26]["expand"].configure(command= lambda: expand_custom_text(cfb[26]["content"], 26))
        cfb[27]["expand"].configure(command= lambda: expand_custom_text(cfb[27]["content"], 27))
        cfb[28]["expand"].configure(command= lambda: expand_custom_text(cfb[28]["content"], 28))
        cfb[29]["expand"].configure(command= lambda: expand_custom_text(cfb[29]["content"], 29))
        cfb[30]["expand"].configure(command= lambda: expand_custom_text(cfb[30]["content"], 30))
        self.customPopup.protocol("WM_DELETE_WINDOW", self.customPopup.withdraw)
        self.customPopup.attributes("-topmost", True)
        self.customPopup.withdraw()
    
    def enableCustomize(self):
        self.customPopup.deiconify()
        # Autofill the customPopup fields with the current spell, if possible
        if len(self.user_objects) == 0:
            return
        current_monster = self.user_objects[self.user_objects_index]
        if current_monster not in self.monster_data:
            return
        cfb = self.customFieldBuckets
        if cfb[0]["get"](cfb[0]["content"]) != "":
            if not messagebox.askyesno(title=f"Overwrite the Current Custom Monster?", message=f"Warning: There is a monster in the Customize Dialogue.\n   The Current Custom Monster " + cfb[0]["get"](cfb[0]["content"]) + " will be lost if you have not saved it.", parent= self.customPopup):
                return
        self.clearCustom()
        fields = ["name", "cr", "size", "type", "subtype", "acString", "alignment", "hp", "speed", "str", "dex", "con", "int", "wis", "cha", "saves", "skills", "senses", "languages", "resist", "immune", "vulnerable", "conditionImmune", "traits", "spellcasting", "spells", "actions", "bonus", "reactions", "legendary", "mythic"]
        for i in range(len(cfb)):
            if fields[i] == "name" and self.monster_data[current_monster]["name"].endswith("  (Custom)"):
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster][fields[i]][:-10])
                continue
            if fields[i] in ["str", "dex", "con", "int", "wis", "cha"]:
                if "scores" not in self.monster_data[current_monster]:
                    continue
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster]["scores"][fields[i]])
                continue
            if fields[i] not in self.monster_data[current_monster]:
                continue
            if fields[i] == "hp":
                current_monster_hp = str(self.monster_data[current_monster]["hp"])
                if "hpFormula" in self.monster_data[current_monster]:
                    current_monster_hp += " (" + self.monster_data[current_monster]["hpFormula"] + ")"
                cfb[i]["insert"](cfb[i]["content"], current_monster_hp)
            elif fields[i] == "spells":
                current_monster_spells = ", ".join([spellName.title() for spellName in self.monster_data[current_monster]["spells"]])
                cfb[i]["insert"](cfb[i]["content"], current_monster_spells)
            else:
                cfb[i]["insert"](cfb[i]["content"], self.monster_data[current_monster][fields[i]])
    
    def saveCustom(self):
        # Refactor
        cfb = self.customFieldBuckets
        new_monster_object = {}
        if cfb[0]["get"](cfb[0]["content"]) != "":
            new_monster_object["name"] = cfb[0]["get"](cfb[0]["content"]) + "  (Custom)"
        else:
            messagebox.showerror(title="Save Failed", message="Failed to Save:\nThis custom monster needs a name", parent= self.customPopup)
            return
        sI = 1
        listToIndex = ["cr", "size", "type", "subtype", "acString", "alignment", "hp", "speed", "str", "dex", "con", "int", "wis", "cha", "saves", "skills", "senses", "languages", "resist", "immune", "vulnerable", "conditionImmune", "traits", "spellcasting", "spells", "actions", "bonus", "reactions", "legendary", "mythic"]
        for abc in listToIndex:
            if abc == "spells":
                new_monster_object[abc] = sorted([class_name for class_name in cfb[sI]["get"](cfb[sI]["content"]).lower().split(", ")]) # Doesn't currently check that the spell is real
            elif cfb[sI]["get"](cfb[sI]["content"]) != "":
                if abc == "acString":
                    try:
                        new_monster_object["acString"] = cfb[sI]["get"](cfb[sI]["content"])
                        new_monster_object["ac"] = max(map(int, findall('\d+', cfb[sI]["get"](cfb[sI]["content"]))))
                    except:
                        messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " has an invalid value for Armor Class", parent= self.customPopup)
                        return
                elif abc == "hp":
                    if len(cfb[sI]["get"](cfb[sI]["content"]).strip().split(" (")) == 2:
                        new_monster_hp = cfb[sI]["get"](cfb[sI]["content"]).strip().split(" (")
                        try:
                            new_monster_object[abc] = int(new_monster_hp[0])
                            new_monster_object["hpFormula"] = new_monster_hp[1].replace(")", "")
                        except:
                            messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " has an invalid value for Hit Points", parent= self.customPopup)
                            return
                    else:
                        try:
                            new_monster_object[abc] = int(cfb[sI]["get"](cfb[sI]["content"]).strip())
                        except:
                            messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " has an invalid value for Hit Points", parent= self.customPopup)
                            return
                elif abc in ["str", "dex", "con", "int", "wis", "cha"]:
                    if "scores" not in new_monster_object:
                        new_monster_object["scores"] = {}
                    try:
                        new_monster_object["scores"][abc] = int(cfb[sI]["get"](cfb[sI]["content"]).strip())
                    except:
                        messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " has an invalid value for an ability score (" + abc.capitalize() + ")", parent= self.customPopup)
                        return
                else:
                    new_monster_object[abc] = cfb[sI]["get"](cfb[sI]["content"])
            elif abc == "acString":
                messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " needs an armor class", parent= self.customPopup)
                return
            elif abc == "hp":
                messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " needs hit points", parent= self.customPopup)
                return
            elif abc == "cr":
                messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_monster_object["name"] + " needs a challenge rating", parent= self.customPopup)
                return
            sI += 1
        # Check if the custom monster already existed with an image path
        if new_monster_object["name"].lower() in self.custom_monster_data and "hasFluffImages" in self.custom_monster_data[new_monster_object["name"].lower()]:
            new_monster_object["hasFluffImages"] = self.custom_monster_data[new_monster_object["name"].lower()]["hasFluffImages"]
        self.monster_data[new_monster_object["name"].lower()] = new_monster_object
        self.custom_monster_data[new_monster_object["name"].lower()] = new_monster_object
        self.save()
    
    def clearCustom(self):
        cfb = self.customFieldBuckets
        for i in range(len(cfb)):
            if "default" in cfb[i]:
                cfb[i]["delete"](cfb[i]["content"], cfb[i]["default"])
            else:
                cfb[i]["delete"](cfb[i]["content"])
    
    def deleteCustom(self):
        cfb = self.customFieldBuckets
        if cfb[0]["get"](cfb[0]["content"]) != "":
            object_name = (cfb[0]["get"](cfb[0]["content"]) + "  (Custom)").lower()
        else: return
        if object_name not in self.custom_monster_data: return
        if not messagebox.askyesno(title=f"Permanently Delete this Custom monster?", message=f"Warning: This will permanently delete this custom monster.\n   The Current Custom Monster " + cfb[0]["get"](cfb[0]["content"]) + " will be completely lost.", parent= self.customPopup):
            return
        if object_name in self.monster_data:
            del(self.monster_data[object_name])
        if object_name in self.custom_monster_data:
            del(self.custom_monster_data[object_name])
            self.save()
        self.clearCustom()
    
    def save(self):
        try:
            with open(f"dynamic/profiles/{self.current_profile}/customMonsters.json", "w+", encoding='utf-8') as fSave:
                json_custom_monsters = json.dumps(self.custom_monster_data, indent=4)
                fSave.write(json_custom_monsters)
        except:
            print("The custom monsters from this session failed to save.")

class CustomSpell:
    def __init__(self, master):
        self.setProfile()
        self.customize_button = tk.Button(self.window, text='Customize', command= self.enableCustomize, bg= BLUE_PURPLE, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
        self.canvas.create_window(B_DIST, B_DIST+35, window= self.customize_button, anchor= tk.NW)
        Tooltip(self.customize_button, text="Opens the Create a Custom Spell window\nThe spell currently displayed will be automatically ported into the Custom Spell window to use as a base\nIf no spell is displayed, all fields will initially be empty\nCustom Spells will be saved across multiple sessions, and can be referenced immediately")
        self.createCustomPopup()
    
    def setProfile(self, profile=DEFAULT_PROFILE, startup=True):
        self.current_profile = profile
        if not startup:
            self.unloadCustom()
        self.loadCustom()
    
    def loadCustom(self):
        with open(f"dynamic/profiles/{self.current_profile}/customSpells.json", encoding='utf-8') as f:
            self.custom_spell_data = {}
            # Import custom spells
            file_data = load(f)
            for spell in file_data:
                # Check for duplicated spell names, ignored if the application is frozen
                if not getattr(sys, 'frozen', False):
                    if spell in self.spell_data:
                        print(f"Duplicated Import with {spell}")
                        try:
                            print("Spell Sources: ", end= "")
                            print(self.spell_data[spell]["source"], end= ", ")
                            print(file_data[spell]["source"])
                        except:
                            pass
                self.spell_data[spell] = file_data[spell]
                self.custom_spell_data[spell] = file_data[spell]
    
    def unloadCustom(self):
        for custom_spell in self.custom_spell_data:
            if custom_spell in self.spell_data:
                del self.spell_data[custom_spell]
    
    def createCustomPopup(self):
        popupColor = BLANK_GRAY
        # Refactor
        self.customPopup = tk.Toplevel(self.window)
        self.customPopup.configure(bg=popupColor)
        self.customPopup.title("Create a Custom Spell")
        self.customMenu = tk.Menu(self.customPopup)
        self.customPopup.config(menu= self.customMenu)
        self.customMenu.add_command(label="Save", command=self.saveCustom)
        self.customMenu.add_command(label="Clear", command=self.clearCustom)
        self.customMenu.add_command(label="Delete", command=self.deleteCustom)
        self.customMenu.add_command(label="Exit", command=self.customPopup.withdraw)
        custom_fields = [
            ["Name:", ["Entry"], "Required"], 
            ["Level:", ["Dropdown", self.levels_txt], "Required"],
            ["School:", ["Dropdown", self.schools_txt], ""],
            ["Style:", ["Dropdown", self.styles_txt], ""],
            ["Casting Time:", ["Entry"], ""],
            ["Ritual:", ["Checkbox"], "Optional"],
            ["Range:", ["Entry"], ""],
            ["Components:", ["Entry"], ""],
            ["Materials:", ["Text", [40, 2]], "Optional"],
            ["Duration:", ["Entry"], ""],
            ["Classes:", ["Text", [40, 2]], "Separate with \", \""],
            ["Save:", ["Dropdown", self.scores_txt], "Optional"],
            ["Description:", ["Text", [80, 20]], "Required\nUse ** for Bold"]
        ]
        self.customFieldBuckets = []
        for i in range(len(custom_fields)):
            field_name = tk.Label(self.customPopup, text=custom_fields[i][0], bg=popupColor, fg=BLACK_BASE, font='Times 12 bold', anchor='ne')
            field_name.grid(row=i, column=0, sticky="nsew")
            modeToggle = custom_fields[i][1][0]
            if modeToggle == "Entry":
                field_content = tk.Entry(self.customPopup, width=40, font='Times 12')
                field_content.grid(row=i, column=1, sticky="nw")
                self.customFieldBuckets.append([field_content, lambda a: a.get().strip(), lambda a, b: a.insert(0, b), lambda a: a.delete(0, tk.END)])
            elif modeToggle == "Dropdown":
                field_content = tk.StringVar()
                field_content.set(custom_fields[i][1][1][0])
                field_menu = tk.OptionMenu(self.customPopup, field_content, *custom_fields[i][1][1])
                field_menu.config(bg=popupColor, fg=BLACK_BASE, font='Times 12')
                field_menu["menu"].config(bg=popupColor, fg=BLACK_BASE, font='Times 12')
                field_menu.grid(row=i, column=1, sticky="nw")
                self.customFieldBuckets.append([field_content, lambda a: a.get(), lambda a, b: a.set(b), lambda a, c: a.set(c), custom_fields[i][1][1][0]])
            elif modeToggle == "Checkbox":
                field_content = tk.BooleanVar()
                field_box = tk.Checkbutton(self.customPopup, variable=field_content, onvalue=True, offvalue=False, bg=popupColor)
                field_box.grid(row=i, column=1, sticky="nw")
                self.customFieldBuckets.append([field_content, lambda a: True if a.get() else "", lambda a, b: a.set(b), lambda a: a.set(False)])
            elif modeToggle == "Text":
                field_content = tk.Text(self.customPopup, bg= OFF_WHITE, fg= BLACK_BASE, font= ('times', 12), width= custom_fields[i][1][1][0], height= custom_fields[i][1][1][1], wrap= tk.WORD)
                field_content.grid(row=i, column=1, sticky="nw")
                self.customFieldBuckets.append([field_content, lambda a: a.get(1.0, tk.END).strip(), lambda a, b: a.insert(1.0, b), lambda a: a.delete(1.0, tk.END)])
            if custom_fields[i][2] != "":
                field_extra = tk.Label(self.customPopup, text=custom_fields[i][2], bg=popupColor, fg=BLACK_BASE, font='Times 12 italic', anchor='nw')
                field_extra.grid(row=i, column=2, sticky="nsew")
        self.customPopup.protocol("WM_DELETE_WINDOW", self.customPopup.withdraw)
        self.customPopup.attributes("-topmost", True)
        self.customPopup.withdraw()
    
    def enableCustomize(self):
        self.customPopup.deiconify()
        # Autofill the customPopup fields with the current spell, if possible
        if len(self.user_objects) == 0:
            return
        current_spell = self.user_objects[self.user_objects_index]
        if current_spell not in self.spell_data:
            return
        cfb = self.customFieldBuckets
        if cfb[0][1](cfb[0][0]) != "":
            if not messagebox.askyesno(title=f"Overwrite the Current Custom Spell?", message=f"Warning: There is a spell in the Customize Dialogue.\n   The Current Custom Spell " + cfb[0][1](cfb[0][0]) + " will be lost if you have not saved it.", parent= self.customPopup):
                return
        self.clearCustom()
        fields = ["name", "level", "school", "style", "time", "ritual", "range", "components", "materials", "duration", "classes", "save", "description"]
        for i in range(len(cfb)):
            if fields[i] == "name" and self.spell_data[current_spell]["name"].endswith("  (Custom)"):
                cfb[i][2](cfb[i][0], self.spell_data[current_spell][fields[i]][:-10])
                continue
            if fields[i] not in self.spell_data[current_spell]:
                continue
            if fields[i] == "classes":
                current_spell_classes = ", ".join([className.capitalize() for className in self.spell_data[current_spell]["classes"]])
                cfb[i][2](cfb[i][0], current_spell_classes)
            else:
                cfb[i][2](cfb[i][0], self.spell_data[current_spell][fields[i]])
    
    def saveCustom(self):
        # Refactor
        cfb = self.customFieldBuckets
        new_spell_object = {}
        if cfb[0][1](cfb[0][0]) != "":
            new_spell_object["name"] = cfb[0][1](cfb[0][0]) + "  (Custom)"
        else:
            messagebox.showerror(title="Save Failed", message="Failed to Save:\nThis custom spell needs a name", parent= self.customPopup)
            return
        new_spell_object["level"] = cfb[1][1](cfb[1][0])
        new_spell_object["school"] = cfb[2][1](cfb[2][0])
        if cfb[3][1](cfb[3][0]) != "No Style":
            new_spell_object["style"] = cfb[3][1](cfb[3][0])
        sI = 4
        listToIndex = ["time", "ritual", "range", "components", "materials", "duration", "classes", "save", "description"]
        for abc in listToIndex:
            if abc == "classes":
                new_spell_object[abc] = sorted([class_name for class_name in cfb[sI][1](cfb[sI][0]).lower().split(", ") if class_name in self.classes_txt])
            elif cfb[sI][1](cfb[sI][0]) != "":
                new_spell_object[abc] = cfb[sI][1](cfb[sI][0])
            elif abc == "description":
                messagebox.showerror(title="Save Failed", message="Failed to Save:\n" + new_spell_object["name"] + " needs a description", parent= self.customPopup)
                return
            sI += 1
        self.spell_data[new_spell_object["name"].lower()] = new_spell_object
        self.custom_spell_data[new_spell_object["name"].lower()] = new_spell_object
        self.save()
    
    def clearCustom(self):
        cfb = self.customFieldBuckets
        for i in range(len(cfb)):
            if len(cfb[i]) == 4:
                cfb[i][3](cfb[i][0])
            elif len(cfb[i]) == 5:
                cfb[i][3](cfb[i][0], cfb[i][4])
    
    def deleteCustom(self):
        cfb = self.customFieldBuckets
        if cfb[0][1](cfb[0][0]) != "":
            object_name = (cfb[0][1](cfb[0][0]) + "  (Custom)").lower()
        else: return
        if object_name not in self.custom_spell_data: return
        if not messagebox.askyesno(title=f"Permanently Delete this Custom spell?", message=f"Warning: This will permanently delete this custom spell.\n   The Current Custom Spell " + cfb[0][1](cfb[0][0]) + " will be completely lost.", parent= self.customPopup):
            return
        if object_name in self.spell_data:
            del(self.spell_data[object_name])
        if object_name in self.custom_spell_data:
            del(self.custom_spell_data[object_name])
            self.save()
        self.clearCustom()
    
    def save(self):
        try:
            with open(f"dynamic/profiles/{self.current_profile}/customSpells.json", "w+", encoding='utf-8') as fSave:
                json_custom_spells = json.dumps(self.custom_spell_data, indent=4)
                fSave.write(json_custom_spells)
        except:
            print("The custom spells from this session failed to save.")