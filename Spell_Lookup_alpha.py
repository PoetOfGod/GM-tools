#   This script is a child for GM Tools, this is the functionality for the Spell Lookup
#
# Import required libraries
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image
from random import randint as randInt, shuffle
# Load child scripts
from Spell_Basics_alpha import *

# Global Variables to Act Like Macros
from GM_Basics_alpha import *

# Window Size Tracker to allow for dynamic window resizing
class Tracker:
    """ Toplevel windows resize event tracker. """

    def __init__(self, toplevel, win_dictionary):
        self.toplevel = toplevel
        self.win_dict = win_dictionary
        self.width, self.height = toplevel.winfo_width(), toplevel.winfo_height()
        self._func_id = None

    def bind_config(self):
        self._func_id = self.toplevel.bind("<Configure>", self.resize)

    def unbind_config(self):  # Untested.
        if self._func_id:
            self.toplevel.unbind("<Configure>", self._func_id)
            self._func_id = None

    def resize(self, event):
        if(event.widget == self.toplevel and (self.width != event.width or self.height != event.height)):
            update_display(event.height, event.width, self.win_dict)
            self.width, self.height = event.width, event.height

# Redraw components tied to the middle of the window
def update_display(win_Height, win_Width, win_Dict):
    global WIN_H, WIN_W
    WIN_H = win_Height
    WIN_W = win_Width
    win_Dict["canvas"].create_window(WIN_W//2-43, H_REF+32, window=win_Dict["name input"], anchor= tk.E)
    win_Dict["canvas"].create_window(WIN_W//2-38, H_REF+30, window=win_Dict["spell input"], anchor= tk.W)
    win_Dict["canvas"].create_window(WIN_W//2, H_REF+75, window=win_Dict["lookup button"])


# Initialize Labels and Buttons for the lookup window
def mapLookupWindow(master, spells):
    # Create a new window
    lookup_Win = master
    # Create a new canvas for this window, with a scrollbar
    canvas_2 = tk.Canvas(lookup_Win, width = WIN_W, height = WIN_H, scrollregion= (0, 0, WIN_W-10, WIN_H+400))
    scrollbar = tk.Scrollbar(lookup_Win, orient=tk.VERTICAL)
    scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
    scrollbar.config(command=canvas_2.yview)
    canvas_2.config(yscrollcommand=scrollbar.set)
    canvas_2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    
    spllNameInputTxt = tk.Label(lookup_Win, text="Name of Spell:", fg='black', font=('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
    canvas_2.create_window(WIN_W//2-43, H_REF+32, window=spllNameInputTxt, anchor= tk.E)
    spllNameInput = tk.Entry(lookup_Win, width= 20, font=('times', 16))
    canvas_2.create_window(WIN_W//2-38, H_REF+30, window=spllNameInput, anchor= tk.W)

    # Create labels to fill with the spell information
    spll_info_Labels = []
    for i in range(8):
        spllinfoLabel = tk.Text(lookup_Win, bg=OFF_WHITE, fg='black', font=('times', 16), width=80, height=1)
        spll_info_Labels.append(spllinfoLabel)
    
    # Returned object to be referenced globally
    lookup_Win_dict = {}
    lookup_Win_dict["window"] = lookup_Win
    lookup_Win_dict["canvas"] = canvas_2
    lookup_Win_dict["name input"] = spllNameInputTxt
    lookup_Win_dict["spell input"] = spllNameInput
    lookup_Win_dict["spell info"] = spll_info_Labels

    # Create an entry for user input
    lkup_btn = tk.Button(lookup_Win, text='Lookup Spell', command=lambda: spellDesc(lookup_Win_dict, spells), bg= DARK_RED, fg=OFF_WHITE, font=('helvetica', 12, 'bold'))
    canvas_2.create_window(WIN_W//2, H_REF+75, window=lkup_btn)
    lookup_Win_dict["lookup button"] = lkup_btn
    # Bind enter to the Lookup Spell
    lookup_Win_dict["canvas"].bind('<Return>', lambda event: spellDesc(lookup_Win_dict, spells))
    lookup_Win_dict["spell input"].bind('<Return>', lambda event: spellDesc(lookup_Win_dict, spells))

    tracker = Tracker(lookup_Win, lookup_Win_dict)
    tracker.bind_config()

    return lookup_Win_dict

# Reset the spell lookup info labels
def resetSpellInfo(lookupWin):
    for info_label in lookupWin["spell info"]:
        info_label.configure(state= 'normal')
        info_label.delete("1.0", "end")
        splinfo_id = lookupWin["canvas"].create_window(WIN_W//2, H_REF+120, window=info_label)
        lookupWin["canvas"].itemconfigure(splinfo_id, state='hidden')

def spellSearch(this_Spell_Input, spells):
    # The '#' Symbol will allow for a lookup based on attributes instead of the name
    all_spells = [spell for spell in spells]
    shuffle(all_spells)
    if "#" in this_Spell_Input:
        this_Spell_Input.replace('#', '')
        filter_Input = this_Spell_Input.split(",")
        filtersLen = len(filter_Input)
        lvlFilter = False
        schFilter = False
        clsFilter = False
        styFilter = False
        if "level:" in this_Spell_Input:
            for i in range(filtersLen):
                if "level:" in filter_Input[i]:
                    lvlFilter = filter_Input[i].split(':')[1].strip()
                    if lvlFilter not in levels_txt:
                        lvlFilter = False
        if "school:" in this_Spell_Input:
            for i in range(filtersLen):
                if "school:" in filter_Input[i]:
                    schFilter = filter_Input[i].split(':')[1].strip().capitalize()
                    if schFilter in schools_dict:
                        schFilter = schools_dict[schFilter]
                    if schFilter not in schools_txt:
                        schFilter = False
        if "class:" in this_Spell_Input:
            for i in range(filtersLen):
                if "class:" in filter_Input[i]:
                    clsFilter = filter_Input[i].split(':')[1].strip()
                    if clsFilter not in classes_txt:
                        clsFilter = False
        if "style:" in this_Spell_Input:
            for i in range(filtersLen):
                if "style:" in filter_Input[i]:
                    styFilter = filter_Input[i].split(':')[1].strip().capitalize()
                    if styFilter not in styles_txt:
                        styFilter = False

        filterSpells = []
        for spell in all_spells:
            if (not lvlFilter or spells[spell]["level"] == lvlFilter):
                if (not schFilter or spells[spell]["school"] == schFilter):
                    if (not styFilter or ("style" in spells[spell] and spells[spell]["style"] == styFilter)):
                        if (not clsFilter or clsFilter in spells[spell]["classes"]):
                            this_Spell_Input = spell
                            break
        
    elif this_Spell_Input not in spells:
        # Check if the Input matches part of a name of a spell
        spellNotFound = True
        for spell in all_spells:
            if (this_Spell_Input.replace(' ', '').replace('\'', '').replace('-', '') in spell.replace(' ', '').replace('\'', '').replace('-', '')):
                this_Spell_Input = spell
                spellNotFound = False
                break

        # Run a more advanced search on each spell name to check if the error is due to spaces or a typo, also functions as a guess to what spell is being typed
        if spellNotFound:
            for spell in all_spells:
                if (len(this_Spell_Input) <= len(spell) + 1) and (hamming(this_Spell_Input.replace(' ', '').replace('\'', '').replace('-', ''), spell.replace(' ', '').replace('\'', '').replace('-', '')) <= 1):
                    # Remove specific non ascii characters from both strings
                    this_Spell_Input = spell
                    break
    
    return this_Spell_Input

# Generate the spell description Labels based on the user input
def spellDesc(lookupWin, spells, event=None):
    resetSpellInfo(lookupWin)
    this_Spell_Input = lookupWin["spell input"].get().strip().lower()
    found_Spell = spellSearch(this_Spell_Input, spells)

    if found_Spell in spells:
        pos1 = H_REF+110
        infolines = getSpellInfo(found_Spell, spells)
        
        character_count = len(infolines[4]) + len(infolines[7])
        
        for i in range(8):
            if infolines[i] != "":
                if i == 0:
                    font_size = 20
                else:
                    font_size = 16
                if character_count > 2000:
                    font_size -= 4
                lookupWin["spell info"][i].configure(font=('times', font_size))
                lookupWin["spell info"][i].tag_configure("bold", font="times " + str(font_size) + " bold")
                lookupWin["spell info"][i].tag_configure("italic", font="times " + str(font_size) + " italic")
                lookupWin["spell info"][i].tag_configure("clean", font="times " + str(font_size))
                mode = "clean"

                lineFeed = infolines[i][:100]
                infolines[i] = infolines[i][100:]
                if len(lineFeed) > 90:
                    lastWordIndex = lineFeed.rfind(' ')
                    infolines[i] = lineFeed[lastWordIndex+1:] + infolines[i]
                    lineFeed = lineFeed[:lastWordIndex]
                max_line_length = len(lineFeed)
                big_lines = [lineFeed]
                numLines = 1
                bold_count = 0
                if i == 0:
                    line1Split = lineFeed.split('(', 1)
                    if len(line1Split) == 2:
                        lookupWin["spell info"][i].insert("end", line1Split[0], "bold")
                        lookupWin["spell info"][i].insert("end", "(" + line1Split[1])
                    else:         
                        lookupWin["spell info"][i].insert("end", lineFeed)
                elif i == 1:
                    lookupWin["spell info"][i].insert("end", lineFeed, "italic")
                elif i < 7:
                    lineExtraSplit = lineFeed.split(': ', 1)
                    if len(lineExtraSplit) == 2:
                        lookupWin["spell info"][i].insert("end", lineExtraSplit[0], "bold")
                        lookupWin["spell info"][i].insert("end", ": " + lineExtraSplit[1])
                    else:         
                        lookupWin["spell info"][i].insert("end", lineFeed)
                else:
                    while lineFeed.find('**') != -1:
                        lookupWin["spell info"][i].insert("end", lineFeed[:lineFeed.find('**')], mode)
                        lineFeed = lineFeed[lineFeed.find('**')+2:]
                        if mode == "clean": mode = "bold"
                        else: 
                            mode = "clean"
                            bold_count += 1
                    if lineFeed:
                        lookupWin["spell info"][i].insert("end", lineFeed, mode)
                while infolines[i] != "":
                    lineFeed = infolines[i][:100]
                    infolines[i] = infolines[i][100:]
                    # Need to be able to handle new lines in the lineFeed
                    # **Primal Infusion and Fusillade of Ice edge cases**
                    if len(lineFeed) > 90:
                        # Don't check the last character
                        lastWordIndex = lineFeed.rfind(' ', 0, -2)
                        infolines[i] = lineFeed[lastWordIndex:] + infolines[i]
                        lineFeed = lineFeed[:lastWordIndex]
                    if lineFeed.find('\n') != -1:
                        newLineIndex = lineFeed.find('\n')
                        infolines[i] = lineFeed[newLineIndex+1:] + infolines[i]
                        lineFeed = lineFeed[:newLineIndex]
                    if len(lineFeed) > max_line_length or len(lineFeed) > 90:
                        max_line_length = max(max_line_length, len(lineFeed))
                        big_lines.append(lineFeed)
                    numLines += 1
                    if lineFeed.startswith(' ') and not (lineFeed.startswith(' -') or lineFeed.startswith('  ')):
                        lineFeed = lineFeed[1:]
                    lookupWin["spell info"][i].insert("end", "\n")
                    while lineFeed.find('**') != -1:
                        lookupWin["spell info"][i].insert("end", lineFeed[:lineFeed.find('**')], mode)
                        lineFeed = lineFeed[lineFeed.find('**')+2:]
                        if mode == "clean": mode = "bold"
                        else: 
                            mode = "clean"
                            bold_count += 1
                    if lineFeed:
                        lookupWin["spell info"][i].insert("end", lineFeed, mode)
                if bold_count > 10: numLines += 1
                lookupWin["spell info"][i].configure(height= numLines)
                font_help = tkFont.Font(font=("times", font_size))
                winPixelWidth = font_help.measure(big_lines[0])
                for big_line in big_lines[1:]:
                    winPixelWidth = max(font_help.measure(big_line), winPixelWidth)
                if font_size == 20:
                    char_width = -int((-winPixelWidth/13.5))
                elif font_size == 16:
                    char_width = -int((-winPixelWidth/10.4))
                else:
                    char_width = -int((-winPixelWidth/7.3))
                if i < 7:
                    char_width += 1
                lookupWin["spell info"][i].configure(width= char_width)

                lookupWin["spell info"][i].configure(state= 'disabled')
                lookupWin["canvas"].create_window(H_REF, pos1, window=lookupWin["spell info"][i], anchor= tk.NW)
                lookupWin["window"].update()
                # Make sure all text is displayed
                if lookupWin["spell info"][i].winfo_width()-5 <= winPixelWidth:
                    lookupWin["spell info"][i].configure(width= char_width+2)
                    lookupWin["canvas"].create_window(H_REF, pos1, window=lookupWin["spell info"][i], anchor= tk.NW)
                    lookupWin["window"].update()
                pos1 += lookupWin["spell info"][i].winfo_height()
    else:
        lookupWin["spell info"][0].configure(width= 13, height= 1, font=('times', 16))
        lookupWin["spell info"][0].insert("end", "Spell Not Found")
        lookupWin["spell info"][0].configure(state= 'disabled')
        lookupWin["canvas"].create_window(WIN_W//2, H_REF+120, window=lookupWin["spell info"][0])

# Use a simple hamming distance calculation to evaluate the distance between the input and a potential key
def hamming(s1,s2):
    result=0
    for x,(i,j) in enumerate(zip(s1,s2)):
        if i!=j:
            result+=1
    return result

def scrollwheel(lookupWin, event):
    lookupWin["canvas"].yview_scroll(-1*(event.delta//120), "units")

def initializeSpellLookup(frame, spells):
    lookupWin = mapLookupWindow(frame, spells)
    lookupWin["canvas"].bind_all("<MouseWheel>", lambda event: scrollwheel(lookupWin, event))
    try:
        lookupWin["image"] = ImageTk.PhotoImage(Image.open("static\\Images\\spelllookup_bkgd.jpg"))
        lookupWin["image_id"] = lookupWin["canvas"].create_image(0, 0, image=lookupWin["image"], anchor=tk.NW)
    except:
        print("Spell Lookup Background failed to load")
        print("Store the image to use as the background at \"static\\Images\\spelllookup_bkgd.jpg\"")
    return lookupWin