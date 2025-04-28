### Alpha 3.4b
> Fixed issue with profiles not saving correctly

### Alpha 3.4a
> Added a QOL feature for the Custom Monster popup, allowing for variable text boxes such as "Actions" or "Traits" to be expanded and shrunk for easier editing
>
> Fixed outdated variable references that prevented custom monsters or spells from saving
>
> Changed the image position in Scroll Generator
>
> Prototyped Gear and Magic Item Lookup
>
> Designed Data Structure for Gear and Magic Items
>
> Added wraplength variable to SmartTable
>
> Fixed some search edge cases for PlayerLookup
>
> Attribute search prototyped for Magic Item Lookup

### Alpha 3.3a
> Misc Bugfixes
>
> Added the ability to use multiple profiles within a single DM Tools build
>
> Profiles can be created and/or swapped to mid-runtime from the "Home" tab
>
> The profile controls the "Initiative Tracker" and "Note Taker" data and the custom monster and spell data
>
> The app has a "default" profile, which will run automatically on launch (the profile ran on launch can be changed using the config)
>
> Created the Parent classes CustomMonster and CustomSpell for code optimization
>
> Fixed a bug where updating an existing Custom Monster would remove the hasFluffImage attribute
>
> Added some extra labels on the home page to make the profile swapping easier to understand

### Alpha 3.2c
> Add to Initiative can now be toggled to roll for the Max HP and initiative of the monster you add
> 
> parseDiceRoll from Dice Roller can now be configured to return a string or an integer
> 
> The config now has options to allow for the Custom Monster window to show custom sizes and types

### Alpha 3.2b
> Fixed an issue with Spell Lookup where it would poorly handle failed spell searches
>
> Autosave now triggers every 10 minutes (instead of 15)
>
> Fixed Monster Lookup other case Skills formatting
>
> Added a new data directory "random"
>
> Moved the pattern and word data for the Shop Name Generator to the "random" data, and restructured the Crafting Rules data import to accomodate
>
> Forced the maximum refresh rate of the application to one one thousandth of a second, to prevent drag lag when significant amount of labels or text fields are displayed
>
> Tooltips added to Initiative Tracker, Monster Lookup, and Spell Lookup
>
> Refactored the Custom Monster Window setup code

### Alpha 3.2a
> Monster Image database size reduced by >45% by converting files to .webp and using compression techniques
> 
> Dice Roller and Calculator prototyped
> 
> Full Heal All on the initiative tracker now automatically removes "Bleeding Out" and "DEAD"
>
> Spell Lookup format algorithm tweaked to implement the previous loop fix (don't check the last character for the last space of a line) when parsing the first line
>
> Spell Lookup format algorithm now uses a more liberal approach to the second info-line, determining pixel width based on italicized font to prevent overflow cases
>
> "bind_all" Notebook issues circumnavigated
>
> Dice Roller can handle duplicate die tasks appropriately
>
> Now also displays the results of the individual dice (up to a max defined in the config), displays the full result of a roll if above the maximum

### Alpha 3.1b
> Monster Database structure fully reformatted
>
> Monsters now have their full stat blocks displayed, even the super complex ones
>
> You can create a custom monster with the same functionalities as a custom spell
>
> You can now query monsters by attributes, including source book, size, type, subtype, alignment, and more
>
> Monster Lookup can now show an image of the monster in a popup window
>
> Monster attribute query has been slightly optimized
>
> Minor display issue resolved with Monster Lookup

### Alpha 3.0c
> The config can now be used to change image file names for the application
>
> Player Lookup input is now much more aggressive in its return, it gives all relevant items to a query
>
> Database dependecy os has been removed, a config option now manually controls what sources to include
>
> Tested different methods of customizing spells/monsters + creating spells and monsters from scratch
>
> Creating a custom spell is now fully implemented

### Alpha 3.0b
> PlayerLookup Scrollbar now works even while hovering over a generated table
>
> Lookup Scrollbars are now accounted for in the default program width
>
> SpellLookup Scroll Region has been fixed
>
> Minor bugfixes and formatting issues addressed
>
> Relocated database collection from the main file to __Database.py

### Alpha 3.0a
> Complete Refactor into classes, optimized old code solutions
>
> Updated Player Lookup to support multiple queries, similar to Monster Lookup and Spell Lookup
>
> Moved the editMode dynamic variable to the config instead of the CraftingRules Database
>
> Add a Splash screen when compiled with PyInstaller

### Alpha 2.3a
> editMode added to Crafting_Rules to enable dynamic swapping between editMode and not editMode
>
> Minor changes/optimizations to Monster Lookup and Spell Lookup
>
> Player Lookup and Player Database prototyped
>
> Player Lookup overhauled
>
> Cross Tab functionality buttons "Add to Initiative" and "Lookup Spells" were moved slightly to account for formatting differences

### Alpha 2.2b
> Fixed edge case with initiative tracker that stopped the sort_entries function from working while the pointer isn't looking at an entry
>
> Fixed monsters with spellcasting not rendering on Monster Lookup due to a missing import
>
> Fixed monster display overlapping when the program ignored my update calls
>
> Initiative Tracker Current HP box now accepts complex inputs as long as they start with + or - (multiplication/division/multiple additions or subtractions, follows PEMDAS)
>
> Initiative Tracker Current HP can no longer go above the Max HP
>
> Added handling in monster lookup for complicated damage immunities, resistances, and vulnerabilities
>
> Monster Lookup now has previous and next buttons, work same as Spell Lookup
>
> Monster Infoline creation has been shifted to the database creation function to significantly reduce the workload and complexity of the monster lookup itself
>
> Monster Lookup has been made considerably more robust, and should not give an "Unknown" return for complicated objects
>
> Major changes to the monster database to reduce storage size, processing times and more
>
> Fixed some initiative turn hallucinations, and made current health sticky when updating entries

### Alpha 2.2a
> Minor Spell Lookup bugfixes when querying a list of spells
>
> Fully reformatted initiative tracker using positional arguments instead of the grid method
>
> Initiative Tracker can now track the current turn in combat
>
> Began redo of Crafting Rules
>
> Implemented a Store Name Generator within the Purchasing section of Crafting Rules
>
> DM Tools tabs have been re-ordered for convenience

### Alpha 2.1c
> Swapped from a .toml to a .json config for simplicity
>
> Modifiers are now applied on spell database generation to reduce initialization load
>
> Fixed some issues with Spell Lookup display
>
> Scroll Generator now supports Custom spell level distributions

### Alpha 2.1b
> Fixed a bug where a list of inputted spells could result in a spell search instead of a spell match due to spaces
>
> Initiative Tracker autosaves
>
> Progress has been started on a replacement for the old Crafting Rules
>
> Initiative Tracker now prompts for confirmation with "Delete", "Clear Entries", and "Full Heal", and the UI has been overhauled


### Alpha 2.1a
> Arrow keys can now cycle through spells in Spell Lookup
>
> GM_Tools now supports a config file (integrated through GM_Basics), which will be utilized more as development progresses
>
> Initiative tracker has been extensively reworked in accordance to requests, is now fully prototyped
>
> The previous one has been renamed "Note Taker", and will remain in the program as is until further notice
>
> An auto save feature has been implemented for the note taker
>
> Monster spellcasting is now included in the monster lookup

### Alpha 2.0e
> Modifier files are now .json instead of .txt, and use a new format that will make it easier to expand/develop new modifiers
>
> Bound scrollwheel event to most of the objects in the spell lookup to allow for much easier scrolling
>
> Set big_line calculation to treat tab carriage as 6 spaces to prevent width display errors
>
> Set to trigger an additional line after bold_count reaches > 5

### Alpha 2.0d
> Development started on a Prototype Monster Lookup
>
> Prototype up and running in a passable state

### Alpha 2.0c
> Spell Lookup now uses a Search by Attributes toggle instead of the # symbol
> 
> No longer requires formatting the attribute, instead text can be thrown down
> 
> Multiple of the same attribute can be searched
> 
> The class_add spell modifier can no longer add duplicate classes, they will instead be ignored
> 
> Created import code to check for spell naming conflicts, does not yet include a robust way to handle them
>
> Cleaned up the text formatting of Spell Lookup into its own function
> 
> Reordered functions in the Child Scripts to make more sense
> 
> Spell Lookup: The name of the spell has custom width handling to hopefully reduce edge cases
>
> Spell Lookup now supports two buttons: Previous and Next Spell
> 
> In addition, many searches will now return multiple spells, which can be viewed using these buttons
> 
> You can lookup multiple spells at once using the ';' as a  divider between queries
> 
> Spells are generally grouped alphabetically, however exceptions apply to allow for random behavior with specific query inputs
> 
> Searching for a spell that has a name duplicate that's been patched will now return both spells

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
