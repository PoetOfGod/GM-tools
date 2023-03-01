The Spell Lookup and Spell Generator use Spell Data in a .json file format.

Included in the repository is a json file for the Spell Data from the 5e System Reference Document.

Here is a guideline to creating your own Spell Data files:
```
{ #Each file is a single dictionary, start with an open brace
  "flaming potato" : { #The name of the spell as a key string, must be all lowercase, can included special characters (but shouldn't include # or "()")
    "name" : "Flaming Potato", #The name of the spell
    "classes" : ["sorcerer", "wizard"], #A list of classes the spell can be used by, all lowercase
    "source" : ["Thravieus' Homebrew", "1"], #The source of the spell followed by the page number
    "level" : "2", #The level of the spell, from 0-9
    "school" : "Evocation", #The class of the spell, standard 5e schools are supported
    "ritual" : "True", #Optional, only include this attribute if the spell can be ritual casted
    "style" : "Chaos", #Optional, an additional classification of the spell
    "time" : "1 action", #The time it takes to cast the spell
    "range" : "20 feet", #Primary range of the spell
    "components" : "Verbal, Somatic, Material" #Requirements of casting the spell
    "materials" : "A potato", #Optional, the materials needed to cast the spell
    "duration" : "Instantaneous", #The amount of time the effect of the spell lasts
    "description" : "You light a potato on fire and pass it to someone. Make a spell attack against a target in range. On a hit they take 2d6 bludgeoning damage and 4d6 fire damage, then, if they have an open hand they may make a Dexterity saving throw. On a successful save they may catch the potato and throw it again on their turn as an action, recasting this spell with a new target and without consuming a spell slot or requiring the spellcasting feature, and using your spellcasting DC. If they fail the save, they instead take an additional 2d6 fire damage.",
    #The full description of the spell as a string, it can include special characters
  } #End of flaming potato, include a comma here if there are additional spells
}
``` 
