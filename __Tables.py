#   This script is a child for DM Tools
#   This script defines the SmartTable class
#
# Classes modified from https://www.geeksforgeeks.org/create-table-using-tkinter/#
import tkinter as tk
# Load config
from ___Config import *

# Table used by Player Lookup
class SmartTable:
    def __init__(self, root, table_items, default_vars, keyBinds=None):
        header, dualLabel, mode, anchors, wraplength, table_text = default_vars
        # code for creating a table
        if header:
            self.h = tk.Label(root, bg=OFF_WHITE, fg=BLACK_BASE, text=header, font='Times 12 bold italic')
            self.h.grid(row=0, column=0, columnspan=len(table_items), sticky="nw")
            if keyBinds: keyBinds(self.h)
        # In the case of columnspan items, make sure the iteration is over the max length
        table_width = len(table_items[0])
        if len(table_items) > 1:
            for x in table_items:
                if len(x) > table_width:
                    table_width = len(x)
        # Automate the anchors variable if mode is set to "class"
        if mode == "class":
            anchors = ["n" for y in range(table_width)]
            if not dualLabel: query_index = 0
            else: query_index = 1
            if "Level" in table_items[query_index]:
                anchors[table_items[query_index].index("Level")] = "nw"
            if "Features" in table_items[query_index]:
                anchors[table_items[query_index].index("Features")] = "nw"
        for i in range(len(table_items)):
            # Skip variable for columnspans in the iteration
            skip_items = 0
            for j in range(table_width):
                if skip_items > 0:
                    skip_items -= 1
                    continue
                # Set the column labels to bold
                if i == 0 or (dualLabel and i == 1):
                    self.font = 'Times 12 bold'
                else:
                    self.font = 'Times 12'
                # Keep the pattern correct if there are two rows of column labels
                if (i % 2 or dualLabel) and ((not dualLabel) or (i > 1 and (i+1) % 2)):
                    self.bg_color = BLANK_GRAY
                else:
                    self.bg_color = OFF_WHITE

                if anchors and len(anchors) > j and anchors[j] in ["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]:
                    column_anchor = anchors[j]
                else:
                    column_anchor = "w"
                # Using an embedded dictionary item to tell the generator to make the table use columnspan
                columnFlag = False
                table_item_text = ""
                if isinstance(table_items[i][j], str):
                    table_item_text = table_items[i][j]
                elif isinstance(table_items[i][j], int):
                    table_item_text =str(table_items[i][j])
                elif isinstance(table_items[i][j], dict):
                    table_item_text = table_items[i][j]["text"]
                    column_anchor = "center"
                    columnFlag = table_items[i][j]["span"]
                
                if wraplength and len(wraplength) > j and wraplength[j]:
                    self.e = tk.Label(root, bg=self.bg_color, fg=BLACK_BASE, text=table_item_text, font=self.font, anchor=column_anchor, wraplength=wraplength[j], justify="left")
                else:
                    self.e = tk.Label(root, bg=self.bg_color, fg=BLACK_BASE, text=table_item_text, font=self.font, anchor=column_anchor)
                
                row_assign = i
                if header: row_assign += 1
                
                if not columnFlag:
                    self.e.grid(row=row_assign, column=j, sticky="nsew")
                else:
                    # Using columnspan, skip iterations until the span has been reached
                    self.e.grid(row=row_assign, column=j, columnspan=columnFlag, sticky="nsew")
                    skip_items = columnFlag - 1
                if keyBinds: keyBinds(self.e)
        if table_text:
            self.text = tk.Label(root, bg=OFF_WHITE, fg=BLACK_BASE, text=table_text[0], font='Times 12')
            if header:
                self.text.grid(row=len(table_items)+2, column=0, columnspan=len(table_width), sticky="nw")
            else:
                self.text.grid(row=len(table_items)+1, column=0, columnspan=len(table_width), sticky="nw")
            if keyBinds: keyBinds(self.text)

# Table used by Crafting Rules
class Table:
    def __init__(self, root, table_items, item_widths, table_text, header=False):
        # code for creating table
        if header:
            self.e = tk.Text(root, width=sum(item_widths), height=1, bg=SCROLL_TAN, fg=BLACK_BASE, font='Times 12 bold italic')
            self.e.grid(row=0, column=0, columnspan=len(item_widths), sticky="nsew")
            self.e.insert(tk.END, header)
            if not EDIT_MODE:
                self.e.configure(state= 'disabled')
        for i in range(len(table_items)):
            for j in range(len(table_items[0])):
                if i == 0:
                    self.font = 'Times 12 bold'
                else:
                    self.font = 'Times 12'
                if i % 2:
                    self.bg_color = DUNE_TAN
                else:
                    self.bg_color = SCROLL_TAN

                item_height = 1
                # Check if the rows to have multiple lines
                if '\n' in table_items[i][j]:
                    for k in table_items[i][j]:
                        if k == '\n':
                            item_height += 1
                self.e = tk.Text(root, width=item_widths[j], height=item_height, bg=self.bg_color, fg=BLACK_BASE, font=self.font)
                
                # Use sticky so the Text fills the grid space correctly even when multi-line rows are introduced
                if header:
                    self.e.grid(row=i+1, column=j, sticky="nsew")
                else:
                    self.e.grid(row=i, column=j, sticky="nsew")
                self.e.insert(tk.END, table_items[i][j])
                if not EDIT_MODE:
                    self.e.configure(state= 'disabled')
        if table_text:
            self.text = tk.Text(root, width=sum(item_widths), height=table_text[1], bg=SCROLL_TAN, fg=BLACK_BASE, font='Times 12')
            if header:
                self.text.grid(row=len(table_items)+2, column=0, columnspan=len(item_widths), sticky="nsew")
            else:
                self.text.grid(row=len(table_items)+1, column=0, columnspan=len(item_widths), sticky="nsew")
            self.text.insert(tk.END, table_text[0])
            if not EDIT_MODE:
                self.text.configure(state= 'disabled')