#   This script is a child for GM Tools, this is the functionality for the Scroll Generator
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
from random import choice as randchoice, randint as randInt
# Load child scripts
from Spell_Basics_alpha import *

# Global Variables to Act Like Macros
from GM_Basics_alpha import *
# Maximum number of scrolls to be generated at once
SCROLL_MAX = 40

# Tooltip Class to allow for more Spell Information
# Code modified from https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 500   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 28
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left', background=OFF_WHITE, relief='solid', borderwidth=1, wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

# Create up to SCROLL_MAX labels to display generated scrolls
def getScrLabels(numLabels, generatorWin):
    scrLabels = []
    scrTooltips = []
    for i in range(numLabels):
        scrLabel = tk.Label(generatorWin, text= "", bg=OFF_WHITE, fg='black', font=('times', 16))
        scrLabels.append(scrLabel)
        scrTooltip = CreateToolTip(scrLabel, text="")
        scrTooltips.append(scrTooltip)
    return scrLabels, scrTooltips

# Hide all scroll labels
def resetScrolls(genWin):
    genWin["canvas"].itemconfigure(genWin["startLabel"], state='hidden')
    for i in range(SCROLL_MAX):
        genWin["labels"][i].configure(text="")
        scr_id = genWin["canvas"].create_window(THRD_W, H_REF+100, window=genWin["labels"][i])
        genWin["canvas"].itemconfigure(scr_id, state='hidden')

# Generation Function
def scrollGen(generatorWin, scrolls, event=None):
    # Reset all scroll labels
    resetScrolls(generatorWin)
    # Filter the list of spells
    cur_scrolls = filterScrolls(generatorWin, scrolls)
    total_spells = len(cur_scrolls)

    randTracker = []
    pos1 = THRD_W
    pos2 = H_REF+100
    number = generatorWin["numInput"].get()
    allowDuplicates = generatorWin["duplicates"].get()
    try:
        number = int(number)
        if(number > SCROLL_MAX):
            number = SCROLL_MAX
    # If input is invalid generate one scroll
    except:
        number = 1
    # Edge Case where total spells is less than number to be generated and allow duplicates is off
    if number > total_spells and not allowDuplicates:
        number = total_spells
    # If more than half SCROLL_MAX spells are being generated, create two columns of spells
    if(number > SCROLL_MAX//2):
        pos1 = MID_W//3
    for j in range(number):
        # If more than half SCROLL_MAX spells are being generated, shift to a new column halfway (rounding up)
        if(number > SCROLL_MAX//2 and j == -(number // -2)):
            pos1 = MID_W
            pos2 = H_REF+100
        
        spellChosen = pickRandScroll(generatorWin, cur_scrolls)
        # If a duplicate is picked, reroll until a new spell is found
        if (not allowDuplicates):
            while spellChosen in randTracker:
                spellChosen = pickRandScroll(generatorWin, cur_scrolls)
            randTracker.append(spellChosen)
        
        # Place the generated scrolls
        pos2 += 30
        generatorWin["labels"][j].configure(text=spellChosen)
        generatorWin["tooltips"][j].text = ("\n".join(getSpellInfo(spellChosen.lower(), scrolls))).replace('**', '').strip()
        generatorWin["canvas"].create_window(pos1, pos2, window=generatorWin["labels"][j])

# Return a list of scrolls that match the filters selected
def filterScrolls(generatorWin, cur_scrolls):
    levelVars = generatorWin["lvlFilters"]
    schoolVars = generatorWin["schFilters"]
    classVars = generatorWin["clssFilters"]
    styleVars = generatorWin["styFilters"]
    levels, schools, classes, styles = [], [], [], []

    for level in levelVars:
        levels.append(level.get())
    for school in schoolVars:
        schools.append(school.get())
    for class_var in classVars:
        classes.append(class_var.get())
    for style_var in styleVars:
        styles.append(style_var.get())
    # Don't filter if all checkboxes are selected
    if all(levels) and all(schools) and all(classes) and all(styles):
        return cur_scrolls
    
    new_scrolls, class_sort, school_sort, style_sort = {}, {}, {}, {}
    for i in range(len(classes_txt)):
        if classes[i] == 1:
            class_sort[classes_txt[i]] = classes[i]
    for i in range(len(schools_txt)):
        if schools[i] == 1:
            school_sort[schools_txt[i]] = schools[i]
    for i in range(len(styles_txt)):
        if styles[i] == 1:
            style_sort[styles_txt[i]] = styles[i]

    # If any column has all options selected, don't filter with that data
    for spell in cur_scrolls:
        if (all(levels) or levels[int(cur_scrolls[spell]["level"])] == 1) and (all(schools) or cur_scrolls[spell]["school"] in school_sort):
            if (all(styles) or ((not ("style" in cur_scrolls[spell])) and ("No Style" in style_sort)) or (("style" in cur_scrolls[spell]) and (cur_scrolls[spell]["style"] in style_sort))):
                for class_name in cur_scrolls[spell]["classes"]:
                    if (all(classes) or (class_name in class_sort)):
                        new_scrolls[spell] = cur_scrolls[spell]
                        break
    return new_scrolls

# Choose a random scroll with support for various weighting styles
def pickRandScroll(generatorWin, cur_scrolls):
    mode = generatorWin["dChoice"].get()
    if mode == 'Default':
        return randchoice(list(cur_scrolls[spell]["name"] for spell in cur_scrolls))
    lvldSpellLists = getLvlSpells(cur_scrolls)
    weights = []
    if mode == 'Uniform':
        for i in range(10):
            weights.append(1)
    elif mode == 'Linear (Decreasing)':
        for i in range(10):
            weights.append(10 - i)
    elif mode == 'Exponential (Decreasing)':
        for i in range(10):
            weights.append((10 - i)*(10 - i))
    elif mode == 'Linear (Increasing)':
        for i in range(10):
            weights.append(i+1)
    elif mode == 'Exponential (Increasing)':
        for i in range(10):
            weights.append((i+1)*(i+1))
    else:
        return randchoice(list(cur_scrolls))
    
    for i in range(9, -1, -1):
        if lvldSpellLists[i] == []:
            del lvldSpellLists[i]
            del weights[i]
    weightsum = sum(weights)
    levelPick = randInt(0, weightsum)
    ps_weights = [sum(weights[ : i + 1]) for i in range(len(weights))]
    for i in range(len(ps_weights)):
        if levelPick <= ps_weights[i]:
            return randchoice(lvldSpellLists[i])
    
    # If a failure occurs, just return a spell at random
    return randchoice(list(cur_scrolls[spell]["name"] for spell in cur_scrolls))

# Put spells in buckets depending on their level
def getLvlSpells(cur_scrolls):
    lvld_SpellLists = []
    for i in range(10):
        lvld_SpellLists.append([])
    for spell in cur_scrolls:
        lvld_SpellLists[int(cur_scrolls[spell]["level"])].append(cur_scrolls[spell]["name"])
    return lvld_SpellLists

# Initialize a host of checkboxes as Filters
def filterInitialize(generatorWin):
    filter_headers = []
    for header_txt in ["Level:", "School:", "Class:", "Styles:"]:
        filter_headers.append(tk.Label(generatorWin, text=header_txt, bg=SCROLL_TAN, fg='black', font=('helvetica', 12, 'italic'), borderwidth=2, relief="raised"))

    # Create checkboxes for Level Filters
    level_boxes, level_vars = [], []
    for i in range(0, 10):
        inc_level = tk.IntVar()
        level_vars.append(inc_level)
        level_text = level_dict[str(i)]
        level_box = tk.Checkbutton(generatorWin, text= level_text, variable=level_vars[i], onvalue= True, offvalue= False, bg=SCROLL_TAN, font=('helvetica', 10), borderwidth=2, relief="raised")
        level_box.select()
        level_boxes.append(level_box)
    
    # Create checkboxes for School Filters
    school_vars, school_boxes = [], []
    for school in schools_txt:
        school_var = tk.IntVar()
        school_box = tk.Checkbutton(generatorWin, text= school, variable= school_var, onvalue= True, offvalue= False, bg=SCROLL_TAN, font=('helvetica', 10), borderwidth=2, relief="raised")
        school_box.select()
        school_vars.append(school_var)
        school_boxes.append(school_box)

    # Create checkboxes for Class Filters
    class_vars, class_boxes = [], []
    for className in classes_txt:
        class_var = tk.IntVar()
        class_box = tk.Checkbutton(generatorWin, text= className.capitalize(), variable= class_var, onvalue= True, offvalue= False, bg=SCROLL_TAN, font=('helvetica', 10), borderwidth=2, relief="raised")
        class_box.select()
        class_vars.append(class_var)
        class_boxes.append(class_box)

    # Create checkbox for Style Filter
    style_vars, style_boxes = [], []
    for style in styles_txt:
        style_var = tk.IntVar()
        style_box = tk.Checkbutton(generatorWin, text= style, variable= style_var, onvalue= True, offvalue= False, bg=SCROLL_TAN, font=('helvetica', 10), borderwidth=2, relief="raised")
        if style == "No Style":
            style_box.select()
        style_vars.append(style_var)
        style_boxes.append(style_box)

    return filter_headers, level_boxes, level_vars, school_boxes, school_vars, class_boxes, class_vars, style_boxes, style_vars

# Expand the window and draw the filter objects on the canvas
def mapfilterOptions(genWin_dict):
    generatorWin, canvas_1 = genWin_dict["window"], genWin_dict["canvas"]
    # Create Objects for the Filter Logic
    filterHeaders, levelBoxes, levelVars, schoolBoxes, schoolVars, classBoxes, classVars, styleBoxes, styleVars = filterInitialize(generatorWin)
    # Bind doubleclick on any checkbox to clear all relevant checkboxes
    for ck_box in levelBoxes:
        ck_box.bind('<Double-1>', lambda event : dbClick_Box(levelBoxes, "body"))
    for ck_box in schoolBoxes:
        ck_box.bind('<Double-1>', lambda event : dbClick_Box(schoolBoxes, "body"))
    for ck_box in classBoxes:
        ck_box.bind('<Double-1>', lambda event : dbClick_Box(classBoxes, "body"))
    for ck_box in styleBoxes:
        ck_box.bind('<Double-1>', lambda event : dbClick_Box(styleBoxes, "body"))
    # Bind doubleclick on the filter headers to select all relevant checkboxes
    filterHeaders[0].bind('<Double-1>', lambda event : dbClick_Box(levelBoxes, "head"))
    filterHeaders[1].bind('<Double-1>', lambda event : dbClick_Box(schoolBoxes, "head"))
    filterHeaders[2].bind('<Double-1>', lambda event : dbClick_Box(classBoxes, "head"))
    filterHeaders[3].bind('<Double-1>', lambda event : dbClick_Box(styleBoxes, "head"))

    flt_lbl = tk.Label(generatorWin, text= "Filters", bg= RICH_BLUE, fg= OFF_WHITE, font=('helvetica', 12, 'bold'), relief= 'raised')
    flt_lbl_id = canvas_1.create_window(2*(THRD_W) +5, H_REF, window= flt_lbl, anchor= tk.NE)

    # Sort by Level, School, and Class
    pos1 = 2*(THRD_W) + 25
    pos2 = H_REF + 25
    
    # Level Checkboxes
    canvas_1.create_window(pos1, pos2, window= filterHeaders[0], anchor= tk.W)
    for i in range(10):
        if (i == 5):
            pos2 = H_REF + 25
            pos1 = pos1 + 90
        pos2 = pos2 + 25
        canvas_1.create_window(pos1, pos2, window= levelBoxes[i], anchor= tk.W)

    # School & Class Checkboxes
    pos1 = 2*(THRD_W) + 25
    pos2 = pos2 + 30
    canvas_1.create_window(pos1, pos2, window= filterHeaders[1], anchor= tk.W)
    canvas_1.create_window(pos1 + 120, pos2, window= filterHeaders[2], anchor= tk.W)
    for i in range(9):
        pos2 = pos2 + 25
        canvas_1.create_window(pos1, pos2, window= schoolBoxes[i], anchor= tk.W)
        canvas_1.create_window(pos1 + 120, pos2, window= classBoxes[i], anchor= tk.W)

    # Style Checkboxes
    pos2 = pos2 + 30
    canvas_1.create_window(pos1, pos2, window= filterHeaders[3], anchor= tk.W)
    for i in range(9):
        pos2 = pos2 + 25
        canvas_1.create_window(pos1, pos2, window= styleBoxes[i], anchor= tk.W)
        canvas_1.create_window(pos1 + 120, pos2, window= styleBoxes[i+10], anchor= tk.W)
    pos2 = pos2 + 25
    canvas_1.create_window(pos1, pos2, window= styleBoxes[9], anchor= tk.W)
    
    return levelVars, schoolVars, classVars, styleVars

# Functionality for the copy button (and Ctrl + C) to put the names of all generated spells on the user's clipboard
def copyScrolls(generatorWin, event=None):
    raw_text = []
    for i in range(SCROLL_MAX):
        try:
            scrTxt = generatorWin["labels"][i]['text']
            if(scrTxt != ""):
                raw_text.append(scrTxt)
        except:
            break
    if (raw_text != []):
        clip_text = (", ").join(raw_text)
        generatorWin["window"].clipboard_clear()
        generatorWin["window"].clipboard_append(clip_text)
        generatorWin["window"].update()

# Double Click Functionality for ease of Filter Selection
def dbClick_Box(typeBoxes, mode= "body"):
    if mode == "body":
        for box in typeBoxes:
            box.deselect()
    elif mode == "head":
        for box in typeBoxes:
            box.select()

def mapGeneratorWindow(master, scrolls):
    # Returned object to be referenced globally
    genWin_dict = {}
    # Create a new window
    genWin_dict["window"] = master
    # Create a new canvas for this window
    genWin_dict["canvas"] = tk.Canvas(genWin_dict["window"], width = WIN_W, height = WIN_H, bg= RICH_BLUE)
    genWin_dict["canvas"].pack()
    genWin_dict["labels"], genWin_dict["tooltips"] = getScrLabels(SCROLL_MAX, genWin_dict["window"])
    
    # Create a checkbox to determine duplicate logic
    duplicates_check = tk.BooleanVar()
    dup_box = tk.Checkbutton(genWin_dict["window"], text= 'Duplicates', variable=duplicates_check, onvalue= True, offvalue= False, bg= BLANK_GRAY, font=('helvetica', 12, 'bold'), borderwidth= 3, relief='raised')
    genWin_dict["canvas"].create_window(43, 5, window=dup_box, anchor= tk.NW)
    genWin_dict["duplicates"] = duplicates_check

    # Create a dropdown to control how spells are picked
    options = ["Default", "Uniform", "Linear (Decreasing)", "Exponential (Decreasing)", "Linear (Increasing)", "Exponential (Increasing)"]
    d_choice = tk.StringVar()
    d_choice.set("Default")
    d_drop = tk.OptionMenu(genWin_dict["window"], d_choice, *options)
    genWin_dict["canvas"].create_window(7, 40, window=d_drop, anchor= tk.NW)
    genWin_dict["dChoice"] = d_choice

    # Create Input for Number of Scrolls
    scrNumInputTxt = tk.Label(genWin_dict["window"], text="# of Scrolls:", fg='black', font=('times', 14, 'bold italic'), bg= OFF_WHITE, borderwidth= 3, relief= 'raised')
    genWin_dict["canvas"].create_window((THRD_W) - 17, H_REF+32, window=scrNumInputTxt)
    scrNumInput = tk.Entry(genWin_dict["window"], width= 2, font=('times', 16))
    genWin_dict["canvas"].create_window((THRD_W) + 53, H_REF+30, window=scrNumInput)
    genWin_dict["numInput"] = scrNumInput
    
    # Show "Click to Generate Scrolls"
    startUp_Label = tk.Label(genWin_dict["window"], text= "Click the Button Above\nto Generate Scrolls", bg=OFF_WHITE, fg= DARK_RED, font=('times', 16), borderwidth= 3, relief= 'groove')
    genWin_dict["startLabel"] = genWin_dict["canvas"].create_window(THRD_W, H_REF+180, window=startUp_Label)

    # Create and place the filter objects
    genWin_dict["lvlFilters"], genWin_dict["schFilters"], genWin_dict["clssFilters"], genWin_dict["styFilters"] = mapfilterOptions(genWin_dict)

    # Fetch the copy icon for the copy button
    try:
        big_cp_img = Image.open("static\\Images\\Copy.ico")
        genWin_dict["copyImage"] = ImageTk.PhotoImage(big_cp_img.resize((23, 23), resample= 3))
        button3 = tk.Button(genWin_dict["window"], command=lambda: copyScrolls(genWin_dict), image=genWin_dict["copyImage"])
    except:
        print("Scroll Generator Copy Icon failed to load")
        print("Store the image to use as the background at \"static\\Images\\Copy.ico\"")
        button3 = tk.Button(genWin_dict["window"], text= "^C", command=lambda: copyScrolls(genWin_dict), height= 1, width= 2, font=('helvetica', 12, 'bold'))
    genWin_dict["canvas"].create_window(22, 20, window=button3)


    button1 = tk.Button(genWin_dict["window"], text='Generate Scrolls', command=lambda: scrollGen(genWin_dict, scrolls), bg= DARK_RED, fg=OFF_WHITE, font=('helvetica', 12, 'bold'))
    genWin_dict["canvas"].create_window(THRD_W, H_REF+75, window=button1)
    # The Enter key will Generate Scrolls
    genWin_dict["canvas"].bind('<Return>', lambda event: scrollGen(genWin_dict, scrolls))
    genWin_dict["numInput"].bind('<Return>', lambda event: scrollGen(genWin_dict, scrolls))
    # Pressing Ctrl+C will copy any generated spells to the clipboard
    genWin_dict["canvas"].bind('<Control-c>', lambda event: copyScrolls(genWin_dict))
    genWin_dict["numInput"].bind('<Control-c>', lambda event: copyScrolls(genWin_dict))
    return genWin_dict

def initializeScrollGenerator(master, scrolls):
    generatorWin = mapGeneratorWindow(master, scrolls)
    try:
        generatorWin["image"] = ImageTk.PhotoImage(Image.open("static\\Images\\scrollgen_bkgd.jpg"))
        generatorWin["image_id"] = generatorWin["canvas"].create_image(2*(THRD_W), MID_H, image=generatorWin["image"])
    except:
        print("Scroll Generator Background failed to load")
        print("Store the image to use as the background at \"static\\Images\\scrollgen_bkgd.jpg\"")
    try:
        big_scrRack_img = Image.open("static\\Images\\scrollfilter_bkgd.jpg")
        generatorWin["filterImage"] = scrRack_img = ImageTk.PhotoImage(big_scrRack_img.resize(((THRD_W) +5, 2*(THRD_H) +100), resample= 3))
        generatorWin["filterImage_id"] = generatorWin["canvas"].create_image(2*(THRD_W), 0, image=scrRack_img, anchor= tk.NW)
    except:
        print("Scroll Filter Background failed to load")
        print("Store the image to use as the background at \"static\\Images\\scrollfilter_bkgd.jpg\"")
    generatorWin["filterBorderSide"] = generatorWin["canvas"].create_rectangle(2*(THRD_W), 0, 2*(THRD_W) +5, 2*(THRD_H) +100, fill=RICH_BLUE)
    generatorWin["filterBorderBottom"] = generatorWin["canvas"].create_rectangle(2*(THRD_W), 2*(THRD_H) +100, WIN_W, 2*(THRD_H) +105, fill=RICH_BLUE)
    return generatorWin