#   This script is a child for DM Tools
#   This script defines the Database Parent class
#
# Import packages needed
from json import load
import sys
# Import Application wide-variables
from ___Config import *

class Database:
    def __init__(self):
        # Pull all required data into memory
        self.collectSpells()
        self.collectCrafting()
        self.collectRandom()
        self.collectMonsters()
        self.collectPlayers()
        self.collectGear()
        self.collectMagicItems()

    def collectSpells(self):
        # Retrieve Spell Data from multiple files
        self.spell_data = {}
        for item in SOURCE_INCLUDE:
            file_data = {}
            try:
                with open("data\\spell\\" + item + "_Spells.json", encoding='utf-8') as f:
                    # Import all spells
                    file_data = load(f)
            except:
                continue
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
            
    def collectCrafting(self):
        # Retrieve Crafting Data
        self.crafting_data = {}
        with open("data\\crafting.json") as f:
            self.crafting_data = load(f)
            
    def collectRandom(self):
        # Retrieve Random Data Words and Patterns
        self.random_words = {}
        self.random_patterns = {}
        with open("data/random/words.json") as f1:
            self.random_words = load(f1)
        with open("data/random/patterns.json") as f2:
            self.random_patterns = load(f2)
        
    def collectMonsters(self):
        # Retrieve Monster Data, attempt to handle duplicates
        self.monster_data = {}
        for item in SOURCE_INCLUDE:
            file_data = {}
            try:
                with open("data\\monster\\" + item + "_Monsters.json", encoding='utf-8') as f:
                    # Import all monsters
                    file_data = load(f)
            except:
                continue
            for monster in file_data:
                # Detect if there are duplicate monsters, important once 3rd party sources are added, but currently flags Multiverse Monsters
                if monster in self.monster_data:
                    # print(f"Duplicated Import with {monster}")
                    try:
                        # print("Monster Sources: ", end= "")
                        # print(self.monster_data[monster]["source"], end= ", ")
                        # print(file_data[monster]["source"])
                        self.monster_data[monster + ", old version"] = file_data[monster]
                        self.monster_data[monster + ", old version"]["name"] = file_data[monster]["name"] + ", Old Version"
                    except:
                        pass
                else:
                    self.monster_data[monster] = file_data[monster] 
    
    def collectPlayers(self):
        # Retrieve Player Data, and iteratively expand it for more convenient lookup
        self.player_data = {}
        for item in SOURCE_INCLUDE:
            file_data = {}
            try:
                with open("data\\player\\" + item + "_Players.json", encoding='utf-8') as f:
                    # Import all player data
                    file_data = load(f)
            except:
                continue
            for data in file_data:
                self.player_data[data] = file_data[data]
                # Create the subentries of the player data
                if "features" in file_data[data]:
                    for data_feature in file_data[data]["features"]:
                        if "exclude" in file_data[data]["features"]:
                            break
                        data_ref = data + " " + data_feature
                        file_reference = file_data[data]["features"][data_feature]
                        self.player_data[data_ref] = file_reference
                        # Have the subentries remember its parent feature
                        if "prefix" in file_reference:
                            self.player_data[data_ref]["prefix"] = file_data[data]["name"] + " " + file_reference["prefix"]
                        else:
                            self.player_data[data_ref]["prefix"] = file_data[data]["name"]
                        if "suffix" in file_data[data] or "feature_header" in file_data[data]:
                            if "suffix" in file_reference:
                                pass
                            elif "feature_header" in file_data[data]:
                                if file_data[data]["feature_header"].endswith("s"):
                                    self.player_data[data_ref]["suffix"] = file_data[data]["feature_header"][:-1]
                                else:
                                    self.player_data[data_ref]["suffix"] = file_data[data]["feature_header"]
                            else:
                                self.player_data[data_ref]["suffix"] = file_data[data]["suffix"]
                        # Create subentries of the subentries
                        if "features" in file_reference:
                            for nested_data_feature in file_reference["features"]:
                                if "exclude" in file_reference["features"]:
                                    break
                                nested_data_ref = data_ref + " " + nested_data_feature
                                self.player_data[nested_data_ref] = file_reference["features"][nested_data_feature]
                                if "prefix" in file_reference["features"][nested_data_feature]:
                                    self.player_data[nested_data_ref]["prefix"] = file_data[data]["name"] + " " + file_reference["features"][nested_data_feature]["prefix"]
                                else:
                                    self.player_data[nested_data_ref]["prefix"] = file_data[data]["name"]
                                if "suffix" in self.player_data[data_ref] or "feature_header" in file_reference:
                                    if "suffix" in file_reference["features"][nested_data_feature]:
                                        pass
                                    elif "feature_header" in file_reference:
                                        if file_reference["feature_header"].endswith("s"):
                                            self.player_data[nested_data_ref]["suffix"] = file_reference["feature_header"][:-1]
                                        else:
                                            playerdata[nested_data_ref]["suffix"] = file_reference["feature_header"]
                                    else:
                                        self.player_data[nested_data_ref]["suffix"] = self.player_data[data_ref]["suffix"]
                                        
    def collectGear(self):
        # Retrieve Gear Data, later combine with crafting recipes data
        self.gear_data = {}
        for item in SOURCE_INCLUDE:
            file_data = {}
            try:
                with open("data/gear/" + item + "_Gear.json", encoding='utf-8') as f:
                    # Import all gear data
                    file_data = load(f)
            except:
                continue
            for data in file_data:
                self.gear_data[data] = file_data[data]
        
        self.item_property_data = {}
        try:
            with open("data/gear/item_Properties.json", encoding='utf-8') as f2:
                self.item_property_data = load(f2)
        except:
            pass
    
    def collectMagicItems(self):
        # Retrieve Magic Item Data, later combine with crafting recipes data
        self.magic_item_data = {}
        for item in SOURCE_INCLUDE:
            file_data = {}
            try:
                with open("data/magic items/" + item + "_Magic_Items.json", encoding='utf-8') as f:
                    # Import all magic item data
                    file_data = load(f)
            except:
                continue
            for data in file_data:
                self.magic_item_data[data] = file_data[data]