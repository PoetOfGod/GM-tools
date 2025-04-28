#   This script is a child for GM Tools 
#   This script defines the Spells Parent class
#
class Spells:
    def __init__(self, spell_data):
        self.spell_data = spell_data
        self.styles_txt = ["No Style", "Alkemancy", "Angelic", "Apocalypse", "Blood", "Chaos", "Clockwork", "Dragon", "Elven Ritual", "Fiendish", "Illumination", "Labrinth", "Liminal", "Mythos", "Ring", "Shadow", "Temporal", "Void", "Winter"]
        self.schools_txt = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Psionic", "Transmutation"]
        self.schools_dict = {'Abjur': 'Abjuration', 'Conj': 'Conjuration', 'Div': 'Divination', 'Ench': 'Enchantment', 'Evoc': 'Evocation', 'Illus': 'Illusion', 'Necro': 'Necromancy', 'Trans': 'Transmutation', 'Psion': 'Psionic'}
        self.levels_txt = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.levels_dict = {"0": "Cantrip", "1": "1st level", "2": "2nd level", "3": "3rd level", "4": "4th level", "5": "5th level", "6": "6th level", "7": "7th level", "8": "8th level", "9": "9th level"}
        self.scores_txt = ["", "Strength", "Dexterity", "Consitution", "Intelligence", "Wisdom", "Charisma"]
        self.classes_txt = self.getSpellClasses()
        
    def getSpellClasses(self):
        class_set = set()
        for spell in self.spell_data:
            for class_name in self.spell_data[spell]["classes"]:
                if class_name:
                    class_set.add(class_name)
        classestxt = []
        for c in class_set:
            classestxt.append(c)
        return sorted(classestxt)
    
    # This takes the information from the spell dictionary and creates a formatted list for display
    def getSpellInfo(self, spell_object):
        infolines = []
        for i in range(8):
            empty_line = ""
            infolines.append(empty_line)
        j = 0
        infolines[j] = spell_object["name"]
        if "source" in spell_object:
            infolines[j] += "  ("
            infolines[j] += spell_object["source"][0]
            infolines[j] += ", "
            infolines[j] += spell_object["source"][1]
            infolines[j] += ")"
        j += 1
        if "level" in spell_object or "school" in spell_object or "style" in spell_object:
            if "level" in spell_object:
                infolines[j] += self.levels_dict[spell_object["level"]]
                infolines[j] += " "
            if "school" in spell_object:
                infolines[j] += spell_object["school"]
            if "style" in spell_object:
                infolines[j] += " [" + spell_object["style"] + "]"
            if "ritual" in spell_object:
                infolines[1] += " (Ritual)"
            j += 1
        if "time" in spell_object:
            infolines[j] += "Casting Time: "
            infolines[j] += spell_object["time"]
            j += 1
        if "range" in spell_object:
            infolines[j] += "Range: "
            infolines[j] += spell_object["range"]
            j += 1
        if "components" in spell_object:
            infolines[j] += "Components: "
            infolines[j] += spell_object["components"]
            if "materials" in spell_object:
                infolines[j] += " ("
                infolines[j] += spell_object["materials"]
                infolines[j] += ")"
            j += 1
        if "duration" in spell_object:
            infolines[j] += "Duration: "
            infolines[j] += spell_object["duration"]
            j += 1
        if "classes" in spell_object:
            infolines[j] += "Classes: "
            for className in spell_object["classes"]:
                infolines[j] += className.capitalize()
                infolines[j] += ", "
            infolines[j] = infolines[6][:-2]
            j += 1
        if "description" in spell_object:
            infolines[j] += spell_object["description"]
        return infolines
    
    # Filter the spells based on their attributes
    def filterSpells(self, current_spells, filters):
        found_spells = {}
        for spell in current_spells:
            if (not filters["src"] or ("source" in current_spells[spell] and current_spells[spell]["source"][0] in filters["src"])):
                if (not filters["lvl"] or current_spells[spell]["level"] in filters["lvl"]):
                    if (not filters["sch"] or current_spells[spell]["school"] in filters["sch"]):
                        if (not filters["sty"] or ("No Style" in filters["sty"] and "style" not in current_spells[spell]) or ("style" in current_spells[spell] and current_spells[spell]["style"] in filters["sty"])):
                            if (not filters["cls"] or any(clss in current_spells[spell]["classes"] for clss in filters["cls"])):
                                found_spells[spell] = current_spells[spell]
        return found_spells
