### Alpha 2.0b
> Cleaned up/Added new skeletons to GM_Tools_alpha for modules to be added
> 
> Added a try-except to any image imports that will allow the program to run without background images
> 
> Redesigned Spell Lookup to use disabled Text objects instead of Label objects to display spell information
> 
> This has reintroduced multiple sizing formulas which may create edge case behavior, but will also allow for integrated bold and italicized text
> 
> Bold and Italic text has been implemented for Spell Lookup

### Alpha 2.0
> Tab System Introduced
> 
> Prototype Initiative Tracker Module created (effectively an embedded notepad)
> 
> Cleanup/Rearranging of Child Scripts performed
> 
> Minor Database clean up
> 
> Scroll Generator's artificer filter was swapped out for inventor
> 
> Scroll Generator Reformatted from the ground up using Global Window Measurements
> 
> Spell Lookup now displays each part of the spell progressively, then formats the next layer after it is displayed

### Alpha 1.1b
> Fixed an issue with the modifier imports that was preventing them from applying
> 
> The class_add modifier now sorts the class list after adding to keep syntax the same across all spells
> 
> Minor changes to the Spell Database

### Alpha 1.1
> Spell Lookup Window can now be resized and includes dynamic input boxes
> 
> Spell Generator now includes the full range of filters for spell styles
> 
> Spell Lookup will only classify legal styles as an acceptable search filter

### Alpha1.0
> The Spell Lookup now compares your query to all parts of the spell name (i.e. if you type flame, a random spell with flame in the name will appear)

### Prototype:
> Started tracking changelog
> 
> The Spell Lookup guess no longer uses dashes or apostrophes
> 
> Added a Yes/No filter on the Scroll Generator for spells with a style
> 
> Fixed \xD7 character parsing for the Spell Database
> 
> The Spell Lookup now can search for a spell based on attributes instead of name alone, this mode can be activated with the '#' symbol, this currently supports level, school, class, and field, but may later be adjusted to include casting time, concentration, source etc. (ex. "#class: bard, field: Liminal, level: 0")
> 
> Moved getSpellInfo() from Scroll Generator and Spell Lookup into a child script Spell Basics
> 
> Fixed an issue with the Scroll Generator 'Ctrl-C' functionality
> 
> Renamed the main window title to Game Master's Tools
