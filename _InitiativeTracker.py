#   This script is a child for GM Tools
#   This script defines the InitiativeTracker Child class
#
# Import required libraries
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
import json
# Load config
from ___Config import *
from __Tooltip import *

class InitiativeTracker:
    def __init__(self, master):
        self.window = master
        self.canvas = tk.Canvas(self.window, width = WIN_W, height = WIN_H)
        self.canvas.pack()
        try:
            self.background_image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["initTrack"]["bg"]))
            self.canvas.create_image(0, 0, image= self.background_image, anchor= tk.NW)
        except:
            print("Initiative Tracker Background failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["initTrack"]["bg"] +"\"")
        # Fetch the arrow for the arrow tracker
        try:
            self.arrow_image = ImageTk.PhotoImage(Image.open(bIP + APP_IMAGES["initTrack"]["arrow"]).resize((41, 12), resample= 3))
        except:
            print("Initiative Tracker Arrow Image failed to load")
            print("Store the image to use as the background at \""+ bIP + APP_IMAGES["initTrack"]["arrow"] +"\"")
            self.arrow_image = False
        
        self.font = "courier 14 bold"
        # Variables for formatting
        self.def_pix_H = 30
        self.cur_pix_H = B_DIST
        self.def_pix_W = 125
        self.cur_pix_W = B_DIST

        # Entries
        initiative_label = tk.Label(self.window, text="Initiative", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=initiative_label)
        self.cur_pix_W += self.def_pix_W
        self.initiative_entry = tk.Entry(self.window, width=4, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.initiative_entry)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W = B_DIST

        current_health_label = tk.Label(self.window, text="Current HP", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=current_health_label)
        self.cur_pix_W += self.def_pix_W
        self.current_health_entry = tk.Entry(self.window, width=4, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.current_health_entry)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W = B_DIST

        max_health_label = tk.Label(self.window, text="Max HP", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=max_health_label)
        self.cur_pix_W += self.def_pix_W
        self.max_health_entry = tk.Entry(self.window, width=4, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.max_health_entry)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W = B_DIST

        temp_health_label = tk.Label(self.window, text="Temp HP", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=temp_health_label)
        self.cur_pix_W += self.def_pix_W
        self.temp_health_entry = tk.Entry(self.window, width=4, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.temp_health_entry)
        self.cur_pix_H = B_DIST
        self.cur_pix_W += 60
        self.def_pix_W = 80

        name_label = tk.Label(self.window, text="Name", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=name_label)
        self.cur_pix_W += self.def_pix_W
        self.name_entry = tk.Entry(self.window, width=12, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.name_entry)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= self.def_pix_W

        armor_class_label = tk.Label(self.window, text="AC", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=armor_class_label)
        self.cur_pix_W += self.def_pix_W
        self.armor_class_entry = tk.Entry(self.window, width=4, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.armor_class_entry)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= self.def_pix_W

        enemy_highlight_label = tk.Label(self.window, text="Enemy?", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=enemy_highlight_label)
        self.cur_pix_W += self.def_pix_W
        self.enemy_highlight_var = tk.BooleanVar()
        self.enemy_highlight_box = tk.Checkbutton(self.window, variable=self.enemy_highlight_var, onvalue=True, offvalue=False, bg=MUDDY_RED)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.enemy_highlight_box)
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= self.def_pix_W

        extra_label = tk.Label(self.window, text="Extra", font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=extra_label)
        self.cur_pix_W += self.def_pix_W
        self.extra_entry = tk.Entry(self.window, width=35, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.extra_entry)
        self.cur_pix_H = B_DIST
        self.cur_pix_W += 150
        self.def_pix_H = 45

        # Buttons
        self.add_button = tk.Button(self.window, text="Add", command=self.add_entry, font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.add_button)
        self.cur_pix_W += 65

        self.update_button = tk.Button(self.window, text="Update", command=self.update_entry, font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.update_button)
        
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= 65

        self.clear_button = tk.Button(self.window, text="Clear Inputs", command=self.clear_inputs, font=self.font, bg=SCROLL_TAN)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.clear_button)
        Tooltip(self.clear_button, text="Clear the input boxes and deselect the current entry")
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_H = B_DIST
        self.cur_pix_W += (self.def_pix_W * 2)

        self.move_up_button = tk.Button(self.window, text="Up", command=self.move_entry_up, font=self.font, bg=RICH_BLUE)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.move_up_button)
        Tooltip(self.move_up_button, text="Force the selected creature up in the initiative\nOnly use this if multiple initiatives are the same (Hotkey: Up Arrow)")
        self.cur_pix_W += 45

        self.move_down_button = tk.Button(self.window, text="Down", command=self.move_entry_down, font=self.font, bg=RICH_BLUE)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.move_down_button)
        Tooltip(self.move_down_button, text="Force the selected creature down in the initiative\nOnly use this if multiple initiatives are the same (Hotkey: Down Arrow)")
        self.cur_pix_W += 80

        self.heal_button = tk.Button(self.window, text="Full Heal All", bg=BRIGHT_GREEN, command=self.heal_all, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.heal_button)
        Tooltip(self.heal_button, text="Sets all creature's Current HP equal to their Max HP")
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= 125

        self.next_turn_button = tk.Button(self.window, text="Next Turn", bg=BLACK_BASE, fg=OFF_WHITE, command=self.next_turn, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.next_turn_button)
        Tooltip(self.next_turn_button, text="Progress the Initiative arrow (Hotkey: Right and Left Arrow)")
        self.cur_pix_W += 125

        self.delete_button = tk.Button(self.window, text="Delete", bg=BRIGHT_RED, command=self.delete_entry, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.delete_button)
        Tooltip(self.delete_button, text="Permanently deletes the selected creature (Hotkey: Delete)")
        self.cur_pix_W += 90

        self.clear_entry_button = tk.Button(self.window, text="Clear List", bg=BRIGHT_RED, command=self.clear_entries, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.clear_entry_button)
        Tooltip(self.clear_entry_button, text="Permanently deletes all creatures in the initiative")
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W -= 90

        self.lookup_monster_button = tk.Button(self.window, text="Lookup Monster", bg=PURPLE_RED, fg=OFF_WHITE, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.lookup_monster_button)
        Tooltip(self.lookup_monster_button, text="Lookup this monster in the Monster Lookup")
        self.cur_pix_H += self.def_pix_H
        self.cur_pix_W = B_DIST + (self.def_pix_W // 2)

        # Listbox
        self.entry_list = tk.Listbox(self.window, height=36, width=80, font=self.font)
        self.canvas.create_window(self.cur_pix_W, self.cur_pix_H, anchor=tk.NW, window=self.entry_list)
        self.entry_list.bind("<<ListboxSelect>>", self.select_entry)
        self.bind_window("<Return>", self.enter_entry)
        self.bind_window("<Escape>", self.clear_inputs)
        self.bind_window("<Delete>", self.delete_entry)
        self.bind_window("<Right>", self.next_turn)
        self.bind_window("<Left>", lambda event: self.next_turn(event, True))
        self.selected_index = None

        # Entry list
        self.entries = []

        if self.arrow_image:
            # Arrow starting position is 155, move 23 to align with list box
            self.arrow_image_id = self.canvas.create_image(10, 155, anchor=tk.NW, image=self.arrow_image)
            self.arrow_position = 0
            self.arrow_adj = 23

        self.load()
    
    def bind_window(self, keybind, command):
        # Class function to use instead of bind_all
        self.canvas.bind(keybind, command)
        self.initiative_entry.bind(keybind, command)
        self.current_health_entry.bind(keybind, command)
        self.max_health_entry.bind(keybind, command)
        self.temp_health_entry.bind(keybind, command)
        self.name_entry.bind(keybind, command)
        self.armor_class_entry.bind(keybind, command)
        self.enemy_highlight_box.bind(keybind, command)
        self.extra_entry.bind(keybind, command)
        self.entry_list.bind(keybind, command)
            
    def add_entry(self, entry = None):
        if not entry:
            initiative = self.initiative_entry.get()
            name = self.name_entry.get()
            current_health = self.current_health_entry.get()
            max_health = self.max_health_entry.get()
            temp_health = self.temp_health_entry.get()
            armor_class = self.armor_class_entry.get()
            enemy_tag = self.enemy_highlight_var.get()
            extra = self.extra_entry.get()
            
            if initiative.isnumeric():
                initiative = int(initiative)
            else:
                return

            if current_health.isnumeric():
                current_health = int(current_health)
            else:
                current_health = 0

            if max_health.isnumeric():
                max_health = int(max_health)
            else:
                max_health = 0
            
            if temp_health.isnumeric():
                temp_health = int(temp_health)
            else:
                temp_health = 0
            
            if armor_class.isnumeric():
                armor_class = int(armor_class)
            else:
                armor_class = 0

            entry = (initiative, name, current_health, max_health, temp_health, armor_class, extra, enemy_tag)
        self.entries.append(entry)
        self.entry_list.insert(tk.END, self.format_entry(entry))
        self.entry_list_sort()

        self.clear_inputs()

    def update_entry(self):
        if self.selected_index is not None:
            initiative = self.initiative_entry.get()
            name = self.name_entry.get()
            current_health = self.current_health_entry.get()
            max_health = self.max_health_entry.get()
            temp_health = self.temp_health_entry.get()
            armor_class = self.armor_class_entry.get()
            enemy_tag = self.enemy_highlight_var.get()
            extra = self.extra_entry.get()

            if initiative.isnumeric():
                initiative = int(initiative)
            else:
                initiative = self.entries[self.selected_index][0]
            
            if temp_health.isnumeric():
                temp_health = int(temp_health)
            elif temp_health == "":
                temp_health = 0
            else:
                temp_health = self.entries[self.selected_index][4]

            math_flag = False
            if current_health.isnumeric():
                current_health = int(current_health)
            elif current_health.startswith("+"):
                cur_health_math = int(eval(current_health))
                current_health = self.entries[self.selected_index][2] + cur_health_math
            elif current_health.startswith("-"):
                cur_health_math = -int(eval(current_health))
                if temp_health > 0:
                    if temp_health >= cur_health_math:
                        temp_health = temp_health - cur_health_math
                        cur_health_math = 0
                    else:
                        cur_health_math -= temp_health
                        temp_health = 0
                current_health = self.entries[self.selected_index][2] - cur_health_math
                math_flag = True
            else:
                current_health = self.entries[self.selected_index][2]

            if max_health.isnumeric():
                max_health = int(max_health)
                # Make current health sticky to max health
                if current_health == self.entries[self.selected_index][3]:
                    current_health = max_health
            else:
                max_health = self.entries[self.selected_index][3]

            # Current Health should never be over Max Health
            if current_health > max_health:
                current_health = max_health

            if current_health < 0 or (current_health == 0 and math_flag):
                    if -current_health >= max_health:
                        messagebox.showerror(title="Fatality", message=name + " has died from massive damage.")
                        if "Bleeding Out" in extra:
                            if "; Bleeding Out" in extra:
                                extra = extra.replace("; Bleeding Out", "")
                            else:
                                extra = extra.replace("Bleeding Out", "")
                        if extra:
                            extra += "; "
                        extra += "DEAD"
                    else:
                        if extra:
                            extra += "; "
                        extra += "Bleeding Out"
                    current_health = 0
            elif current_health > 0:
                if "Bleeding Out" in extra:
                    if "; Bleeding Out" in extra:
                        extra = extra.replace("; Bleeding Out", "")
                    else:
                        extra = extra.replace("Bleeding Out", "")
                if "DEAD" in extra:
                    if "; DEAD" in extra:
                        extra = extra.replace("; DEAD", "")
                    else:
                        extra = extra.replace("DEAD", "")
            
            if armor_class.isnumeric():
                armor_class = int(armor_class)
            else:
                armor_class = self.entries[self.selected_index][5]
        
            entry = (initiative, name, current_health, max_health, temp_health, armor_class, extra, enemy_tag)
            self.entries[self.selected_index] = entry
            self.entry_list.delete(self.selected_index)
            self.entry_list.insert(self.selected_index, self.format_entry(entry))
            self.entry_list_sort()

            self.clear_inputs()

    def clear_inputs(self, event=None):
        self.initiative_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.current_health_entry.delete(0, tk.END)
        self.max_health_entry.delete(0, tk.END)
        self.temp_health_entry.delete(0, tk.END)
        self.armor_class_entry.delete(0, tk.END)
        self.extra_entry.delete(0, tk.END)
        self.enemy_highlight_box.deselect()
        self.entry_list.selection_clear(0, tk.END)
        self.selected_index = None

    def delete_entry(self, event=None):
        if self.selected_index is not None:
            if messagebox.askyesno(title=f"Delete {self.entries[self.selected_index][1]}?", message=f"Are you sure you want to delete {self.entries[self.selected_index][1]}?"):
                self.entry_list.delete(self.selected_index)
                del self.entries[self.selected_index]
                self.selected_index = None
                if self.arrow_image and self.arrow_position >= len(self.entries):
                    reset_move = self.arrow_position * - self.arrow_adj
                    self.canvas.move(self.arrow_image_id, 0, reset_move)
                    self.arrow_position = 0

    def clear_entries(self, bypass= False):
        if bypass or messagebox.askyesno(title=f"Clear all creatures?", message=f"Are you sure you want to delete all creatures in the initiative?"):
            self.entry_list.delete(0, tk.END)
            self.entries = []
            self.selected_index = None
            if self.arrow_image:
                reset_move = self.arrow_position * - self.arrow_adj
                self.canvas.move(self.arrow_image_id, 0, reset_move)
                self.arrow_position = 0

    def enter_entry(self, event):
        if self.selected_index is not None:
            self.update_entry()
        else:
            self.add_entry()

    def select_entry(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection:
            index = selection[0]
            self.selected_index = index
            entry = self.entries[index]
            self.initiative_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.current_health_entry.delete(0, tk.END)
            self.max_health_entry.delete(0, tk.END)
            self.temp_health_entry.delete(0, tk.END)
            self.armor_class_entry.delete(0, tk.END)
            self.extra_entry.delete(0, tk.END)
            self.initiative_entry.insert(0, entry[0])
            self.name_entry.insert(0, entry[1])
            # The current health is the most likely thing to get overwritten
            # self.current_health_entry.insert(0, entry[2])
            self.max_health_entry.insert(0, entry[3])
            self.temp_health_entry.insert(0, entry[4])
            self.armor_class_entry.insert(0, entry[5])
            self.extra_entry.insert(0, entry[6])
            if entry[7]:
                self.enemy_highlight_box.select()
            else:
                self.enemy_highlight_box.deselect()

    def entry_list_sort(self):
        if self.arrow_image and self.arrow_position < len(self.entries):
            bind_arrow_entry = self.entries[self.arrow_position]
        else:
            bind_arrow_entry = False
        self.entries.sort(reverse=True, key=lambda x: x[0])
        self.entry_list.delete(0, tk.END)
        for entry in self.entries:
            self.entry_list.insert(tk.END, self.format_entry(entry))
            if entry[7]:
                self.entry_list.itemconfig(tk.END, bg=BRIGHT_RED)
        if bind_arrow_entry:
            new_position = self.entries.index(bind_arrow_entry)
            reset_move = (new_position - self.arrow_position) * self.arrow_adj
            self.canvas.move(self.arrow_image_id, 0, reset_move)
            self.arrow_position = new_position

    def format_entry(self, entry):
        initiative, name, current_health, max_health, temp_health, armor_class, extra, tag = entry
        health_str = f"{current_health}/{max_health}"
        if temp_health > 0:
            health_str = f"{temp_health}+{health_str}"
        return f"{initiative:<4} {name:<15} HP: {health_str:<10} AC: {armor_class:>2}, {extra}"
    
    def heal_all(self):
        if len(self.entries) > 0:
            if messagebox.askyesno(title=f"Heal all creatures?", message=f"Are you sure you want to heal all creatures in the initiative?"):
                self.entry_list.delete(0, tk.END)
                for i in range(len(self.entries)):
                    initiative, name, current_health, max_health, temp_health, armor_class, extra, tag = self.entries[i]
                    if "Bleeding Out" in extra:
                        if "; Bleeding Out" in extra:
                            extra = extra.replace("; Bleeding Out", "")
                        else:
                            extra = extra.replace("Bleeding Out", "")
                    if "DEAD" in extra:
                        if "; DEAD" in extra:
                            extra = extra.replace("; DEAD", "")
                        else:
                            extra = extra.replace("DEAD", "")
                    entry = (initiative, name, max_health, max_health, temp_health, armor_class, extra, tag)
                    self.entries[i] = entry
                    self.entry_list.insert(tk.END, self.format_entry(entry))
                    if entry[7]:
                        self.entry_list.itemconfig(tk.END, bg=BRIGHT_RED)

    def move_entry_up(self):
        if len(self.entries) > 1 and self.selected_index is not None and self.selected_index != 0:
            self.entries[self.selected_index], self.entries[self.selected_index - 1] = self.entries[self.selected_index - 1], self.entries[self.selected_index]
            if self.arrow_image and self.selected_index == self.arrow_position:
                self.canvas.move(self.arrow_image_id, 0, -self.arrow_adj)
                self.arrow_position -= 1
            self.entry_list.delete(0, tk.END)
            for entry in self.entries:
                self.entry_list.insert(tk.END, self.format_entry(entry))
                if entry[7]:
                    self.entry_list.itemconfig(tk.END, bg=BRIGHT_RED)
            self.selected_index = None
            self.clear_inputs()

    def move_entry_down(self):
        if len(self.entries) > 1 and self.selected_index is not None and self.selected_index < len(self.entries) - 1:
            self.entries[self.selected_index + 1], self.entries[self.selected_index] = self.entries[self.selected_index], self.entries[self.selected_index + 1]
            if self.arrow_image and self.selected_index == self.arrow_position and self.arrow_position != 0:
                self.canvas.move(self.arrow_image_id, 0, self.arrow_adj)
                self.arrow_position += 1
            self.entry_list.delete(0, tk.END)
            for entry in self.entries:
                self.entry_list.insert(tk.END, self.format_entry(entry))
                if entry[7]:
                    self.entry_list.itemconfig(tk.END, bg=BRIGHT_RED)
            self.selected_index = None
            self.clear_inputs()

    def next_turn(self, event=None, prevTurn=False):
        if self.arrow_image:
            if prevTurn:
                if self.arrow_position != 0:
                    self.arrow_position -= 1
                    self.canvas.move(self.arrow_image_id, 0, -self.arrow_adj)
                else:
                    full_move = (len(self.entries) - 1) * self.arrow_adj
                    self.canvas.move(self.arrow_image_id, 0, full_move)
                    self.arrow_position = len(self.entries) - 1
            elif self.arrow_position >= (len(self.entries) - 1):
                reset_move = self.arrow_position * -self.arrow_adj
                self.canvas.move(self.arrow_image_id, 0, reset_move)
                self.arrow_position = 0
            else:
                self.arrow_position += 1
                self.canvas.move(self.arrow_image_id, 0, self.arrow_adj)

    def load(self, profile=DEFAULT_PROFILE):
        # Try to load the saved data from a previous session
        try:
            with open(f"dynamic/profiles/{profile}/initTracker.json", "r", encoding='utf-8') as fOpen:
                init_entries = json.load(fOpen)["initiative"]
        except:
            print("Initiative Tracker entries failed to load.")
            init_entries = None

        if init_entries:
            for entry in init_entries:
                try:
                    self.add_entry(entry)
                except:
                    pass

    def save(self, profile=DEFAULT_PROFILE):
        try:
            with open(f"dynamic/profiles/{profile}/initTracker.json","w+", encoding='utf-8') as fSave:
                entry_tracker = {"initiative" : self.entries}
                json_entry_tracker = json.dumps(entry_tracker, indent=4)
                fSave.write(json_entry_tracker)
        except:
            print("Initiative tracker failed to save.")

    def run(self):
        self.window.mainloop()
