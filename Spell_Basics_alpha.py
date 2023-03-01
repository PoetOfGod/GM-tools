#   This script is a child for GM Tools, 
#   This script includes any shared functions for the Scroll Generator and Spell Lookup

# Declare global lists/dictionaries for schools, classes, and levels supported by the automation
styles_txt = ["No Style", "Alkemancy", "Angelic", "Apocalypse", "Blood", "Chaos", "Clockwork", "Dragon", "Elven Ritual", "Fiendish", "Illumination", "Labrinth", "Liminal", "Mythos", "Ring", "Shadow", "Temporal", "Void", "Winter"]
schools_txt = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Psionic", "Transmutation"]
schools_dict = {'Abjur': 'Abjuration', 'Conj': 'Conjuration', 'Div': 'Divination', 'Ench': 'Enchantment', 'Evoc': 'Evocation', 'Illus': 'Illusion', 'Necro': 'Necromancy', 'Trans': 'Transmutation', 'Psion': 'Psionic'}
classes_txt = ["bard", "cleric", "druid", "inventor", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
levels_txt = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
level_dict = {"0": "Cantrip", "1": "1st level", "2": "2nd level", "3": "3rd level", "4": "4th level", "5": "5th level", "6": "6th level", "7": "7th level", "8": "8th level", "9": "9th level"}

# This takes the information from the spell dictionary and creates a formatted list for display
def getSpellInfo(this_Spell_Name, spells):
    level_dict = {"0": "Cantrip", "1": "1st level", "2": "2nd level", "3": "3rd level", "4": "4th level", "5": "5th level", "6": "6th level", "7": "7th level", "8": "8th level", "9": "9th level"}
    this_Spell = spells[this_Spell_Name]
    infolines = []
    for i in range(8):
        empty_line = ""
        infolines.append(empty_line)
    j = 0
    infolines[j] = this_Spell["name"]
    if "source" in this_Spell:
        infolines[j] += "  ("
        infolines[j] += this_Spell["source"][0]
        infolines[j] += ", "
        infolines[j] += this_Spell["source"][1]
        infolines[j] += ")"
    j += 1
    if "level" in this_Spell or "school" in this_Spell or "style" in this_Spell:
        if "level" in this_Spell:
            infolines[j] += level_dict[this_Spell["level"]]
            infolines[j] += " "
        if "school" in this_Spell:
            infolines[j] += this_Spell["school"]
        if "style" in this_Spell:
            infolines[j] += " [" + this_Spell["style"] + "]"
        if "ritual" in this_Spell:
            infolines[1] += " (Ritual)"
        j += 1
    if "time" in this_Spell:
        infolines[j] += "Casting Time: "
        infolines[j] += this_Spell["time"]
        j += 1
    if "range" in this_Spell:
        infolines[j] += "Range: "
        infolines[j] += this_Spell["range"]
        j += 1
    if "components" in this_Spell:
        infolines[j] += "Components: "
        infolines[j] += this_Spell["components"]
        if "materials" in this_Spell:
            infolines[j] += " ("
            infolines[j] += this_Spell["materials"]
            infolines[j] += ")"
        j += 1
    if "duration" in this_Spell:
        infolines[j] += "Duration: "
        infolines[j] += this_Spell["duration"]
        j += 1
    if "classes" in this_Spell:
        infolines[j] += "Classes: "
        for className in this_Spell["classes"]:
            infolines[j] += className.capitalize()
            infolines[j] += ", "
        infolines[j] = infolines[6][:-2]
        j += 1
    if "description" in this_Spell:
        infolines[j] += this_Spell["description"]
    return infolines