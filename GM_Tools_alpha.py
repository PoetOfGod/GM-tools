# Import packages needed
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from os import listdir
from json import load as jsonLoad
# Load child scripts
import Spell_Lookup_alpha as splLkp
import Scroll_Generator_alpha as scrGen
import Initiative_Tracker_alpha as initTrack

# Collect Global Variables
from GM_Basics_alpha import *
# Declare global dictionaries for applications to be included in this application
apps_dict = {
    "Scroll Generator": True, 
    "Spell Lookup": True, 
    "Equipment Lookup": False, 
    "Crafting Rules": False, 
    "Monster Lookup": False, 
    "Player Lookup": False,
    "Loot Generator": False, 
    "Name Generator": False, 
    "Magic Item Lookup": False, 
    "Initiative": True, 
    "Dice Roller": False, 
    "Encounter Builder": False
    }

# Collect the data for all working applications
def collectDatabases():
    master_database = {}
    if apps_dict["Scroll Generator"] or apps_dict["Spell Lookup"]:
        master_database["spell data"] = collectSpells()
    if apps_dict["Equipment Lookup"]:
        master_database["equip data"] = collectEquip()
    if apps_dict["Monster Lookup"]:
        master_database["monster data"] = collectMonsters()
    if apps_dict["Player Lookup"]:
        master_database["player data"] = collectPlayerData()
    if apps_dict["Name Generator"]:
        master_database["name data"] = collectNames()
    if apps_dict["Magic Item Lookup"]:
        master_database["magic item data"] = collectMagicItems()
    return master_database

# Database collection handling
def collectSpells():
    # Retrieve Spell Data from specific JSON Files
    spells = {}
    DBs = listdir(r"Databases")
    spellCount_dict = {}
    for item in DBs:
        if item.endswith("_Spells.json"):
            with open("Databases\\" + item, encoding='utf-8') as f:
                # Import all spells
                file_data = jsonLoad(f)
                tempspellCount = 0
                for spell in file_data:
                    spells[spell] = file_data[spell]
                    tempspellCount += 1
                spellCount_dict[item] = tempspellCount
    
    # Retrieve Modifier Data from specific .txt files
    mods = {}
    Mds = listdir(r"Databases\Modifiers")
    # Collect Modifiers
    for item in Mds:
        if item.endswith("Mods.txt"):
            with open("Databases\\Modifiers\\" + item, "r") as f:
                modDump = f.readlines()
                for mod in modDump:
                    modAttri = mod.split('; ')
                    mods[modAttri[0]] = {}
                    for attribute in modAttri[1:]:
                        operators = attribute.split(': ')
                        if operators[1].__contains__(','):
                            operators[1] = operators[1].strip('\n').split(', ')
                        else:
                            operators[1] = operators[1].strip('\n')
                        mods[modAttri[0]] = {
                            operators[0] : operators[1]
                        }
    # Apply Modifiers
    for spell_name in mods:
        spell_name_lower = spell_name.lower()
        if spell_name_lower in spells:
            for operation in mods[spell_name]:
                theChange = mods[spell_name][operation]
                if operation == "level_change":
                    spells[spell_name_lower]["level"] = theChange
                elif operation == "school_change":
                    spells[spell_name_lower]["school"] = theChange
                elif operation == "class_add":
                    if isinstance(theChange, list):
                        for new_class in theChange:
                            spells[spell_name_lower]["classes"].append(new_class)
                    else:
                        spells[spell_name_lower]["classes"].append(theChange)
                    spells[spell_name_lower]["classes"] = sorted(spells[spell_name_lower]["classes"])
                elif operation == "class_change":
                    spells[spell_name_lower]["classes"] = theChange
    # Return the modified spells dictionary
    return spells

def collectEquip():
    pass

def collectMonsters():
    pass

def collectPlayerData():
    pass

def collectNames():
    pass

def collectMagicItems():
    pass

# Create the tabs for all applications
def createAppTabs(tabControl):
    srcGenerator = launch_Scroll_Generator(tabControl)
    splLookup = launch_Spell_Lookup(tabControl)
    launch_Equipment_Lookup(tabControl)
    crftRules = launch_Crafting_Rules(tabControl)
    launch_Monster_Lookup(tabControl)
    launch_Loot_Generator(tabControl)
    launch_Name_Generator(tabControl)
    initTracker = launch_Initiative_Tracker(tabControl)
    launch_Dice_Roller(tabControl)
    launch_Encounter_Builder(tabControl)
    return srcGenerator, splLookup, crftRules, initTracker

# Application Launchers (Tied to Tabs)
def launch_Scroll_Generator(tabControl, event=None):
    srcGeneratorFrame = ttk.Frame(tabControl)
    tabControl.add(srcGeneratorFrame, text= "Scroll Generator")
    srcGenerator = scrGen.initializeScrollGenerator(srcGeneratorFrame, masterDB["spell data"])
    tabControl.pack(expand = 1, fill ="both")
    return srcGenerator

def launch_Spell_Lookup(tabControl, event=None):
    splLookupFrame = ttk.Frame(tabControl)
    tabControl.add(splLookupFrame, text= "Spell Lookup")
    splLookup = splLkp.initializeSpellLookup(splLookupFrame, masterDB["spell data"])
    tabControl.pack(expand = 1, fill ="both")
    return splLookup

def launch_Equipment_Lookup(tabControl, event=None):
    pass

def launch_Crafting_Rules(tabControl, event=None):
    pass

def launch_Monster_Lookup(tabControl, event=None):
    pass

def launch_Player_Lookup(tabControl, event=None):
    pass

def launch_Loot_Generator(tabControl, event=None):
    pass

def launch_Name_Generator(tabControl, event=None):
    pass

def launch_Initiative_Tracker(tabControl, event=None):
    initTrackerFrame = ttk.Frame(tabControl)
    tabControl.add(initTrackerFrame, text= "Initiative Tracker")
    initTracker = initTrack.initializeInitiativeTracker(initTrackerFrame)
    tabControl.pack(expand = 1, fill ="both")
    return initTracker

def launch_Dice_Roller(tabControl, event=None):
    pass

def launch_Magic_Item_Lookup(tabControl, event=None):
    pass

def launch_Encounter_Builder(tabControl, event=None):
    pass

# Use this function to save data when the program closes 
# Does not currently work if the computer is shut down while program is running
def safeExit(master, initTracker):
    # Save the contents of the initiative tracker (See child script)
    initTrack.initTrackerSave(initTracker)
    master.destroy()

if __name__ == '__main__':
    # Create an instance of tkinter window, using a ttk Notebook for the ability to use Tabs
    master = tk.Tk()
    master.title('Game Master\'s Tools')
    masterTabControl = ttk.Notebook(master)
    masterTab = ttk.Frame(masterTabControl)

    masterTabControl.add(masterTab, text= "Home")
    
    # Create the main window canvas, this will contain buttons that initialize the other applications
    master_canvas = tk.Canvas(masterTab, width = WIN_W, height = WIN_H, bg= RICH_BLUE)
    master_canvas.pack()

    # Put the background on the canvas
    try:
        master_bg_file = ImageTk.PhotoImage(Image.open("static\\Images\\gmhome_bkgd.jpg").resize((1920, 1080), resample= 3))
        master_background_image = master_canvas.create_image(MID_W, MID_H, image=master_bg_file)
    except:
        print("GM Tools Home Background failed to load")
        print("Store the image to use as the background at \"static\\Images\\gmhome_bkgd.jpg\"")

    # Pull all of the data from the files into a memory
    masterDB = collectDatabases()

    # Create the tabs for each application
    # These return dictionary objects to prevent Python from garbage-collecting any images or important information from child scripts
    srcGenObjs, splLookObjs, crftRuleObjs, initTracker = createAppTabs(masterTabControl)
    
    masterTabControl.pack(expand = 1, fill ="both")
    master.protocol("WM_DELETE_WINDOW", lambda: safeExit(master, initTracker))
    master.mainloop()