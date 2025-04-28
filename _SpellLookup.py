#   This script is a child for GM Tools
#   This script defines the SpellLookup Child class
#
# Import required libraries
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import ImageTk, Image
from random import choice as randchoice, shuffle
# Load config
from ___Config import *
# Load parent scripts
from __Spells import *
from __Custom import CustomSpell
from __Lookup import *
from __Tooltip import *

class SpellLookup(Lookup, Spells, CustomSpell):
def __init__(self, master, spell_data):
Lookup.__init__(self, master)
Spells.__init__(self, spell_data)
self.canvas = tk.Canvas(self.window, width = WIN_W-18, height = WIN_H, scrollregion= (0, 0, WIN_W-10, WIN_H+218))

self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL)
self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
self.scrollbar.config(command=self.canvas.yview)
self.canvas.config(yscrollcommand=self.scrollbar.set)
self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

name_of_spell = tk.Label(self.window, text= "Name of Spell:", fg= BLACK_BASE, font= ('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
self.canvas.create_window(WIN_W//2-43, B_DIST+32, window= name_of_spell, anchor= tk.E)
self.spell_query = tk.Entry(self.window, width= 20, font= ('times', 16))
self.canvas.create_window(WIN_W//2-38, B_DIST+30, window= self.spell_query, anchor= tk.W)

self.attributes_var = tk.BooleanVar()
attribute_button = tk.Checkbutton(self.window, text= 'Search by Attributes', variable= self.attributes_var, onvalue= True, offvalue= False, bg= ORANGE, font= ('times', 12, 'bold'), borderwidth= 3, relief= 'raised')
self.canvas.create_window(B_DIST, B_DIST, window= attribute_button, anchor= tk.NW)
Tooltip(attribute_button, text="When this is enabled the search bar will attempt to match characteristics of the spell instead of the name\nYou can search by the following characteristics:\nLevel, School, Class, Style, and Source Book\nSeparate different characteristics with a \",\"\nSeparate different queries (only one of each will be returned, at random) with a \";\"")

# Create a popup prefilled with the current spell information, or an empty popup if there's no spell
CustomSpell.__init__(self, master)

self.spell_displays = []
for i in range(8):
    temp_label = tk.Text(self.window, bg= OFF_WHITE, fg= BLACK_BASE, font= ('times', 16), width= 80, height= 1)
    self.spell_displays.append(temp_label)
    
lookup_button = tk.Button(self.window, text='Lookup Spell', command= self.genSpellDesc, bg= DARK_RED, fg= OFF_WHITE, font= ('helvetica', 12, 'bold'))
self.canvas.create_window(WIN_W//2, B_DIST+75, window= lookup_button)

self.next_button = tk.Button(self.window, text='Next Spell', command= lambda: self.displayNextObject(self.genSpellDesc, True), bg= BLANK_GRAY, fg=BLACK_BASE, font= ('book antiqua', 12, 'italic', 'bold'))
self.canvas.create_window(WIN_W//2 +105, B_DIST+75, window= self.next_button)
self.prev_button = tk.Button(self.window, text='Previous', command= lambda: self.displayNextObject(self.genSpellDesc, False), bg= BLANK_GRAY, fg=BLACK_BASE, font=('book antiqua', 12, 'italic', 'bold'))
self.canvas.create_window(WIN_W//2 -100, B_DIST+75, window= self.prev_button)

self.canvas_bucket = [self.window, self.canvas, name_of_spell, self.spell_query, lookup_button, self.customize_button, attribute_button, self.next_button, self.prev_button]

for lookupObject in self.canvas_bucket:
    self.setKeyBinds(lookupObject, self.genSpellDesc)
for labelObject in self.spell_displays:
    self.setKeyBinds(labelObject, self.genSpellDesc)

try:
    self.image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["spellLook"]["bg"]))
    self.canvas.create_image(0, 0, image= self.image, anchor= tk.NW)
except:
    print("Spell Lookup Background failed to load")
    print("Store the image to use as the background at \""+ bIP + APP_IMAGES["spellLook"]["bg"] +"\"")

def genSpellDesc(self, found_Spell="", event=None):
self.resetSpellDisplay()
if found_Spell == "":
    spell_input = self.spell_query.get().strip().lower()
    if spell_input != "" or self.attributes_var.get():
        if ';' in spell_input:
            self.user_objects = []
            query_split = spell_input.split(';')
            for i in range(len(query_split)):
                search_result = self.searchSpells(query_split[i].lower().strip(), True)
                if search_result:
                    self.user_objects.append(randchoice(search_result))
                else:
                    self.user_objects.append("SNF102 Spell Not Found") # Return a nonsense query
        else:
            search_result = self.searchSpells(spell_input)
            if search_result:
                self.user_objects = sorted(self.searchSpells(spell_input))
            else:
                self.user_objects.append("SNF101 Spell Not Found") # Return a nonsense query
    else:
        all_spells = [spell for spell in self.spell_data]
        shuffle(all_spells)
        self.user_objects = all_spells
    self.user_objects_index = 0
    found_Spell = self.user_objects[self.user_objects_index]
self.updateNextButton()
if found_Spell in self.spell_data:
    pos1 = B_DIST+110
    infolines = self.getSpellInfo(self.spell_data[found_Spell])
    c_count = len(infolines[4]) + len(infolines[7])
    
    for i in range(8):
        pos1 = self.formatSpellText(infolines[i], i, pos1, c_count)
else:
    self.spell_displays[0].configure(width= 13, height= 1, font= ('times', 16))
    self.spell_displays[0].insert("end", "Spell Not Found")
    self.spell_displays[0].configure(state= 'disabled')
    self.canvas.create_window(WIN_W//2, B_DIST+120, window= self.spell_displays[0])

def resetSpellDisplay(self):
for spell_text in self.spell_displays:
    spell_text.configure(state= 'normal')
    spell_text.delete("1.0", "end")
    spell_text_id = self.canvas.create_window(WIN_W//2, B_DIST+120, window= spell_text)
    self.canvas.itemconfigure(spell_text_id, state= 'hidden')

def searchSpells(self, spell_input, inputList=False):
attributes = self.attributes_var.get()
all_spells = [spell for spell in self.spell_data]
shuffle(all_spells)
if attributes and spell_input != "":
    filter_Input = [filter_in.strip() for filter_in in spell_input.split(",")]
    filters = {"lvl" : [], "sch" : [], "cls" : [], "sty" : [], "src" : []}
    for this_filter in filter_Input:
        this_filter = this_filter.lower()
        cap_filter = this_filter.capitalize()
        title_filter = " ".join(word.capitalize() for word in this_filter.split())
        if this_filter in self.levels_txt:
            filters["lvl"].append(this_filter)
        if cap_filter in self.schools_dict:
            filters["sch"].append(self.schools_dict[cap_filter])
        elif cap_filter in self.schools_txt:
            filters["sch"].append(cap_filter)
        if this_filter in self.classes_txt:
            filters["cls"].append(this_filter)
        if title_filter in self.styles_txt:
            filters["sty"].append(title_filter)
        if title_filter in publishers_txt:
            for book_abr in publishers_dict[title_filter]:
                filters["src"].append(sources_dict[book_abr])
        if this_filter in sources_dict:
            filters["src"].append(sources_dict[this_filter])
        if this_filter in sources_txt:
            filters["src"].append(this_filter)

    found_spell_objs = self.filterSpells(self.spell_data, filters)
    return [spell for spell in found_spell_objs]
    
elif spell_input not in self.spell_data:
    clean_input = spell_input.replace(' ', '').replace('\'', '').replace('-', '')
    # Check if the Input matches part of a name of a spell
    found_spell_list = []
    for spell in all_spells:
        # Remove specific non-letter characters from both strings
        if (clean_input in spell.replace(' ', '').replace('\'', '').replace('-', '')):
            found_spell_list.append(spell)
    if found_spell_list:
        return found_spell_list

    # Run a more advanced search on each spell name to check if the error is due to spaces or a typo, also functions as a guess to what spell is being typed
    for spell in all_spells:
        # Remove specific non-letter characters from both strings
        if (len(spell_input) <= len(spell) + 1) and (self.spellcheck(clean_input, spell.replace(' ', '').replace('\'', '').replace('-', '')) <= 1):
            found_spell_list.append(spell)
    if found_spell_list:
        return found_spell_list
# Return both spells if a spell has the same name followed by " ii", unless the search input includes multiple spells
elif spell_input + " ii" in self.spell_data and not inputList:
    return [spell_input, spell_input + " ii"]
return [spell_input]

def formatSpellText(self, line, x, position, character_count):
if line != "":
# dynamic font sizing
    if x == 0:
        font_size = 20
    else:
        font_size = 16
    if character_count > 2000:
        font_size -= 4
    # Reset the font tags based on the desired font size
    self.spell_displays[x].configure(font=('times', font_size))
    self.spell_displays[x].tag_configure("bold", font="times " + str(font_size) + " bold")
    self.spell_displays[x].tag_configure("italic", font="times " + str(font_size) + " italic")
    self.spell_displays[x].tag_configure("clean", font="times " + str(font_size))
    mode = "clean"

    # Process the first line for each spell info label
    lineFeed = line[:100]
    line = line[100:]
    if len(lineFeed) - lineFeed.count('*') > 90:
            # Don't check the last character
            lastWordIndex = lineFeed.rfind(' ', 0, -2)
            line = lineFeed[lastWordIndex:] + line
            lineFeed = lineFeed[:lastWordIndex]
    if lineFeed.find('\n') != -1:
            # Handle new lines in the lineFeed
            newLineIndex = lineFeed.find('\n')
            line = lineFeed[newLineIndex+1:] + line
            lineFeed = lineFeed[:newLineIndex]
    max_line_length = len(lineFeed)
    big_lines = [lineFeed]
    numLines = 1
    bold_count = 0
    # Bold the name of the spell, but not the source
    if x == 0:
        line1Split = lineFeed.split(' (', 1)
        if len(line1Split) == 2:
            self.spell_displays[x].insert("end", line1Split[0], "bold")
            self.spell_displays[x].insert("end", " (" + line1Split[1])
        else:         
            self.spell_displays[x].insert("end", lineFeed)
    # Italicize the level, school, style, and ritual tag
    elif x == 1:
        self.spell_displays[x].insert("end", lineFeed, "italic")
    # Bold the Attribute Headers, such as Range: or Components:
    elif x < 7:
        lineExtraSplit = lineFeed.split(': ', 1)
        if len(lineExtraSplit) == 2:
            self.spell_displays[x].insert("end", lineExtraSplit[0], "bold")
            self.spell_displays[x].insert("end", ": " + lineExtraSplit[1])
        else:         
            self.spell_displays[x].insert("end", lineFeed)
    else:
        # Handling to add bold text if the first line contains the in-text bold flag
        while lineFeed.find('**') != -1:
            self.spell_displays[x].insert("end", lineFeed[:lineFeed.find('**')], mode)
            lineFeed = lineFeed[lineFeed.find('**')+2:]
            if mode == "clean": mode = "bold"
            else: 
                mode = "clean"
                bold_count += 1
        if lineFeed:
            self.spell_displays[x].insert("end", lineFeed, mode)
    # Go into a while loop once all variables have been initialized to handle multi-line boxes
    while line != "":
        lineFeed = line[:100]
        line = line[100:]
        if len(lineFeed) - lineFeed.count('*') > 90:
            # Don't check the last character
            lastWordIndex = lineFeed.rfind(' ', 0, -2)
            line = lineFeed[lastWordIndex:] + line
            lineFeed = lineFeed[:lastWordIndex]
        if lineFeed.find('\n') != -1:
            # Handle new lines in the lineFeed
            newLineIndex = lineFeed.find('\n')
            line = lineFeed[newLineIndex+1:] + line
            lineFeed = lineFeed[:newLineIndex]
        if len(lineFeed) - lineFeed.count('*') > max_line_length or len(lineFeed) > 90:
            # If this is a large line, add it to a list for length evaluation
            max_line_length = max(max_line_length, len(lineFeed))
            big_lines.append(lineFeed.replace('**', '*'))
        numLines += 1
        if lineFeed.startswith(' ') and not (lineFeed.startswith(' -') or lineFeed.startswith('  ')):
            lineFeed = lineFeed[1:]
        self.spell_displays[x].insert("end", "\n")
        while lineFeed.find('**') != -1:
            self.spell_displays[x].insert("end", lineFeed[:lineFeed.find('**')], mode)
            lineFeed = lineFeed[lineFeed.find('**')+2:]
            if mode == "clean": mode = "bold"
            else: 
                mode = "clean"
                bold_count += 1
        if lineFeed:
            self.spell_displays[x].insert("end", lineFeed, mode)
    # Bold lines slightly increase the vertical height
    if (bold_count > 5 and font_size > 12) or (bold_count > 10 and font_size <= 12): numLines += 1
    self.spell_displays[x].configure(height= numLines)
    # Find an estimation for the desired pixel width
    font_help = tkFont.Font(font=("times", font_size))
    # Special case for the name of the spell
    if x == 0:
        font_help_1 = tkFont.Font(font=("times", font_size, "bold"))
        winPixelWidth = font_help_1.measure(big_lines[0].split(" (")[0]) + font_help.measure(" (" + big_lines[0].split(" (")[1])
    elif x == 1:
        font_help_2 = tkFont.Font(font=("times", font_size, "italic"))
        winPixelWidth = font_help_2.measure(big_lines[0])
    else:
        # Use 6 spaces instead of /t for calculating line width
        for i in range(len(big_lines)):
            big_lines[i] = big_lines[i].replace('\t', '      ')
        winPixelWidth = font_help.measure(big_lines[0])
        for big_line in big_lines[1:]:
            winPixelWidth = max(font_help.measure(big_line), winPixelWidth)
    # Convert the pixel width into an estimated character width (denominator = 0.775*font_size - 2)
    char_width = -int((-winPixelWidth/((0.775*font_size)-2)))
    # Account for bold text in the first text boxes
    if x < 7:
        char_width += 1
    self.spell_displays[x].configure(width= char_width)

    self.spell_displays[x].configure(state= 'disabled')
    self.canvas.create_window(B_DIST, position, window=self.spell_displays[x], anchor= tk.NW)
    # Add an extra margin of error if displayed text width is too close to the estimated text width
    if self.spell_displays[x].winfo_reqwidth()-5 <= winPixelWidth:
        self.spell_displays[x].configure(width= char_width+2)
        self.canvas.create_window(B_DIST, position, window=self.spell_displays[x], anchor= tk.NW)
    # Get the height data in pixels once the text display has been calculated
    position += self.spell_displays[x].winfo_reqheight()
return position
