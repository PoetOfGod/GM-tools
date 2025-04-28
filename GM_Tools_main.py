# The goal of this application is to be a multi-functional tool that can assist Game Masters
# Current Working Status of Each Application:
#   Scroll Generator - Refinement Stage                       Mid Application
#   Spell Lookup - Refinement Stage                           Mid Application
#   Initiative Tracker - Refinement Stage                     Light Application
#   Crafting Rules - Refinement Stage                         Light Application
#   Monster Lookup - Refinement Stage                         Heavy Application
#   Player Lookup - Refinement Stage                          Mid Application
#   Dice Roller - Prototyped, needs iterations                Light Application
#   Gear Lookup - Prototyped, needs iterations                Mid Application
#   Magic Item Lookup - Prototyped, needs iterations          Mid Application
#
#   Loot Generator - Not Started                              Light Application
#   NPC Generator - Not Started, Light Database Required      Mid Application
#   Encounter Builder - Not Started                           Mid Application

# Databases Required:
#   Spells - Done
#   Monsters - Refining
#   Classes/Subclasses - Working
#   Feats/Backgrounds/Races - Working
#   Crafting Rules - Working
#   Magic Items - Working
#   Gear - Working
#   Random Names/Content - Working
#   Extensive Meta Database/Meta Tags - TBD
#
# Import packages needed
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import re
from time import sleep
from pathlib import Path
# Load config
from ___Config import *
# Load parent scripts
from __Database import *
from __Tooltip import *
# Load child scripts
from _InitiativeTracker import *
from _MonsterLookup import *
from _SpellLookup import *
from _PlayerLookup import *
from _ScrollGenerator import *
from _CraftingRules import *
from _GearLookup import *
from _Magic_ItemLookup import *
from _DiceRoller import *
from _NoteTaker import *
# Import code for the Pyinstaller Splash Screen
import sys
if getattr(sys, 'frozen', False):
    import pyi_splash
    # Import code for a launch sound
    if APP_SOUNDS["launch"]:
        # Only include this input here for now
        from playsound import playsound
        playsound(bSP + APP_SOUNDS["launch"], block=False)

class DM_Tools(Database):
    def __init__(self, master):
        Database.__init__(self)
        # Create an instance of tkinter window, using a ttk Notebook for the ability to use Tabs
        self.master = master
        self.master.title('Game Master\'s Tools')
        self.appNotebook = ttk.Notebook(self.master)
        self.home_window = ttk.Frame(self.appNotebook)
        self.appNotebook.add(self.home_window, text= "Home")
        
        # Create the main window canvas
        self.canvas = tk.Canvas(self.home_window, width = WIN_W, height = WIN_H, bg= RICH_BLUE)
        self.canvas.pack()
        
        # Put the background on the canvas
        try:
            self.background_file = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["home"]["bg"]).resize((1920, 1080), resample= 3))
            self.background_image = self.canvas.create_image(MID_W, MID_H, image= self.background_file)
        except:
            print("DM Tools Home Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["home"]["bg"] +"\"")
            
        # Create the tabs for each module from classes defined in the child scripts
        self.createModules()
        # Setup buttons and objects that need cross-module functions to work
        self.crossModules()
        
        # Create the entry and labels for Profile Swapping
        change_profile_label = tk.Label(self.home_window, text= "Change Profile:", fg= BLACK_BASE, font= ('times', 18, 'bold'), bg= SCROLL_TAN, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(B_DIST, B_DIST, anchor=tk.NW, window= change_profile_label)
        self.current_profile = DEFAULT_PROFILE
        self.profile_label = tk.Label(self.home_window, text= self.current_profile.title(), fg= BLACK_BASE, font= ('times', 18), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
        self.canvas.create_window(WIN_W - (B_DIST*2), B_DIST, anchor=tk.NE, window= self.profile_label)
        self.profile_entry = tk.Entry(self.home_window, width= 20, font= ('times', 18))
        self.canvas.create_window(B_DIST, B_DIST+40, anchor=tk.NW, window= self.profile_entry)
        self.profile_entry.bind("<Return>", self.profileSwap)
        
        # Final Setup before launching
        self.appNotebook.pack(expand= 1, fill= "both")
        self.master.protocol("WM_DELETE_WINDOW", self.safeExit)
    
    # Launch the child scripts and bind each to its own Notebook frame
    def createModules(self):
        # Initiative Tracker
        initiative_tracker_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(initiative_tracker_frame, text= "Initiative Tracker")
        self.initiative_tracker = InitiativeTracker(initiative_tracker_frame)
        # Monster Lookup
        monster_lookup_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(monster_lookup_frame, text= "Monster Lookup")
        self.monster_lookup = MonsterLookup(monster_lookup_frame, self.monster_data)
        # Spell Lookup
        spell_lookup_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(spell_lookup_frame, text= "Spell Lookup")
        self.spell_lookup = SpellLookup(spell_lookup_frame, self.spell_data)
        # Player Lookup
        player_lookup_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(player_lookup_frame, text= "Player Lookup")
        self.player_lookup = PlayerLookup(player_lookup_frame, self.player_data)
        # Equipment Lookup
        gear_lookup_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(gear_lookup_frame, text= "Gear Lookup")
        self.gear_lookup = GearLookup(gear_lookup_frame, self.gear_data, self.item_property_data)
        # Magic Item Lookup
        magic_item_lookup_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(magic_item_lookup_frame, text= "Magic Item Lookup")
        self.magic_item_lookup = Magic_ItemLookup(magic_item_lookup_frame, self.magic_item_data)
        # Scroll Generator
        scroll_generator_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(scroll_generator_frame, text= "Scroll Generator")
        self.scroll_generator = ScrollGenerator(scroll_generator_frame, self.spell_data)
        # Loot Generator
        # NPC Generator
        # Crafting Rules
        crafting_rules_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(crafting_rules_frame, text= "Crafting Rules")
        self.crafting_rules = CraftingRules(crafting_rules_frame, [self.crafting_data, self.random_patterns, self.random_words])
        # Dice Roller
        dice_roller_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(dice_roller_frame, text= "Dice Roller")
        self.dice_roller = DiceRoller(dice_roller_frame)
        # Note Taker
        note_taker_frame = ttk.Frame(self.appNotebook)
        self.appNotebook.add(note_taker_frame, text= "Note Taker")
        self.note_taker = NoteTaker(note_taker_frame)
        # Encounter Builder
        # Soundscape
        self.appNotebook.pack(expand= 1, fill= "both")
    
    # Homepage function to change dynamic data profiles
    def profileSwap(self, event=None):
        # Tasks - Check if the profile folder exists, if it doesn't then ask if it should create one
        profileQuery = self.profile_entry.get().lower()
        # An empty entry should revert it to using the default profile
        if not profileQuery:
            self.refreshDynamicApps()
            self.current_profile = DEFAULT_PROFILE
            self.profile_label.configure(text= self.current_profile.title())
            return
        pQPath = Path("dynamic/profiles/" + profileQuery)
        # Only allow the profileQuery to contain alphanumerical characters
        allowed_chars = set("1234567890 qwertyuiopasdfghjklzxcvbnm")
        if set(profileQuery) <= allowed_chars:
            pass
        else:
            messagebox.showerror(title="Invalid Profile Characters", message="This profile is invalid, please input a different profile name.")
            return
        pQTest = pQPath.exists()
        if not pQTest:
            if not messagebox.askyesno(title=f"Create a new profile?", message=f"The profile named \"{profileQuery}\" does not exist.\nWould you like to create a new profile with the name \"{profileQuery}\"?"):
                return
            # Create a new profile folder
            else:
                pQPath.mkdir(parents=True, exist_ok=True)
                Path("dynamic/profiles/" + profileQuery + "/custom_monster_img").mkdir(parents=True, exist_ok=True)
                newP_dict = {"customMonsters.json" : r"{}", "customSpells.json" : r"{}", "initTracker.json" : r'{"initiative" : []}', "noteTaker.txt" : ""}
                for newP_file in newP_dict:
                    with open(f"dynamic/profiles/{profileQuery}/{newP_file}", "w+", encoding='utf-8') as d_f:
                        d_f.write(newP_dict[newP_file])
        
        self.refreshDynamicApps(profileQuery)
        self.current_profile = profileQuery
        self.profile_label.configure(text= self.current_profile.title())
    
    def refreshDynamicApps(self, profile=DEFAULT_PROFILE):
        # Save and then clear initiativeTracker and noteTaker
        self.initiative_tracker.save(self.current_profile)
        self.initiative_tracker.clear_entries(True)
        self.note_taker.save(self.current_profile)
        self.note_taker.clear()
        # Load initiativeTracker and noteTaker
        self.initiative_tracker.load(profile)
        self.note_taker.load(profile)
        # Remove the current custom monsters, then import any new ones
        self.monster_lookup.setProfile(profile, False)
        self.spell_lookup.setProfile(profile, False)
    
    # Functions that rely on multiple modules for implementation, usually involve "communication" across the Notebook
    def crossModules(self):
        self.monster_lookup.addMontoInit_Button.config(command = self.addMonstertoInitiative)
        self.monster_lookup.lookupMonSpells_Button.config(command = self.lookupMonsterSpells)
        self.initiative_tracker.lookup_monster_button.config(command = self.lookupMonsterfromInit)
        
    def addMonstertoInitiative(self):
        if not self.monster_lookup.user_objects or self.monster_lookup.user_objects[self.monster_lookup.user_objects_index] not in self.monster_data: return
        currentMonster = self.monster_data[self.monster_lookup.user_objects[self.monster_lookup.user_objects_index]]
        if currentMonster:
            if currentMonster["name"].endswith("  (Custom)"):
                entry_name = currentMonster["name"][:-10]
            elif currentMonster["name"].endswith(", Old Version"):
                entry_name = currentMonster["name"][:-13]
            else:
                entry_name = currentMonster["name"]
            if self.monster_lookup.addMontoInit_InitToggle.get():
                try:
                    score_mod = (currentMonster["scores"]["dex"]-10) // 2
                except:
                    score_mod = 0
                entry_init = self.dice_roller.parseDieString("d20", mode="num") + score_mod
            else:
                entry_init = 0
            if self.monster_lookup.addMontoInit_HPToggle.get():
                try:
                    entry_health = self.dice_roller.parseDieString(currentMonster["hpFormula"], mode="num")
                except:
                    try:
                        entry_health = currentMonster["hp"]
                    except:
                        entry_health = 0
            else:
                try:
                    entry_health = currentMonster["hp"]
                except:
                    entry_health = 0
            try:
                entry_ac = currentMonster["ac"]
            except:
                entry_ac = 0
            entry = (entry_init, entry_name, entry_health, entry_health, 0, entry_ac, "", True)
            self.initiative_tracker.add_entry(entry)
    
    def lookupMonsterSpells(self):
        if not self.monster_lookup.user_objects or self.monster_lookup.user_objects[self.monster_lookup.user_objects_index] not in self.monster_data: return
        currentMonster = self.monster_data[self.monster_lookup.user_objects[self.monster_lookup.user_objects_index]]
        if currentMonster and currentMonster["spells"]:
            self.appNotebook.select(3)
            self.spell_lookup.spell_query.delete(0, tk.END)
            self.spell_lookup.spell_query.insert(tk.END, "; ".join(currentMonster["spells"]))
            self.spell_lookup.genSpellDesc()

    def lookupMonsterfromInit(self):
        # Get monster name from selected entry in initiative tracker
        if self.initiative_tracker.selected_index != None and self.initiative_tracker.entries:
            selected_monster_name = self.initiative_tracker.entries[self.initiative_tracker.selected_index][1]
        # Clean up monster name (removing spaces, numbers at the front or end)
            selected_monster_name = re.sub(r'\d+$', '', selected_monster_name)
        # Change active window to monster lookup
            self.appNotebook.select(2)
        # Lookup the monster in the monster lookup
            self.monster_lookup.monster_query.delete(0, tk.END)
            self.monster_lookup.monster_query.insert(tk.END, selected_monster_name)
            self.monster_lookup.genMonsterDesc()
    
    # Executive Functions that govern application-wide behaviors
    def safeExit(self):
        # Save the contents of modules that store "dynamic" data
        self.initiative_tracker.save(self.current_profile)
        self.note_taker.save(self.current_profile)
        self.master.destroy()
    
    def autosave(self):
        self.initiative_tracker.save(self.current_profile)
        self.note_taker.save(self.current_profile)
        # Save every 10 minutes
        self.master.after(600000, self.autosave)
    
    def refresh_rate(self, e):
        if e.widget == self.master:
            sleep(0.001)

    def run(self):
        self.master.after_idle(self.autosave)
        self.master.after_idle(lambda: self.master.bind("<Configure>", self.refresh_rate))
        self.master.mainloop()
          
if __name__ == '__main__':
    app = DM_Tools(tk.Tk())
    # Close the PyiInstaller Splash Screen before mainloop is called
    if getattr(sys, 'frozen', False):
        pyi_splash.close()
    app.run()
