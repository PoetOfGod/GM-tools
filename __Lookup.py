#   This script is a child for DM Tools
#   This script defines the Lookup Parent class
#
# Import Application wide-variables
from ___Config import *

class Lookup:
    def __init__(self, master):
        self.window = master
        self.user_objects = []
        self.user_objects_index = 0
    
    def setKeyBinds(self, lookupObject, lookupFunction):
        lookupObject.bind("<MouseWheel>", self.scrollwheel)
        lookupObject.bind("<Return>", lambda event: lookupFunction())
        self.setArrowKeys(lookupObject, lookupFunction)
    
    def setArrowKeys(self, lookupObject, lookupFunction):
        lookupObject.bind("<Right>", lambda event: self.displayNextObject(lookupFunction, True))
        lookupObject.bind("<Left>", lambda event: self.displayNextObject(lookupFunction, False))
    
    def freezeArrowKeys(self, lookupObject):
        lookupObject.unbind("<Right>")
        lookupObject.unbind("<Left>")
    
    def spellcheck(self, s1, s2):
        result = 0
        for x, (i, j) in enumerate(zip(s1, s2)):
            if i != j:
                result += 1
                if result > 1:
                    break
        return result
    
    def displayNextObject(self, descFunction, goForward):
        if goForward:
            try:
                if self.user_objects_index < len(self.user_objects)-1:
                    self.user_objects_index += 1
                    descFunction(self.user_objects[self.user_objects_index])
            except:
                pass
        else:
            try:
                if self.user_objects_index >= 1:
                    self.user_objects_index -= 1
                    descFunction(self.user_objects[self.user_objects_index])
            except:
                pass
        self.updateNextButton()
    
    def updateNextButton(self):
        if self.user_objects_index >= 1:
            self.prev_button.configure(bg= SCROLL_TAN)
        else:
            self.prev_button.configure(bg= BLANK_GRAY)
        if self.user_objects_index < len(self.user_objects)-1:
            self.next_button.configure(bg= SCROLL_TAN)
        else:
            self.next_button.configure(bg= BLANK_GRAY)
    
    def scrollwheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")