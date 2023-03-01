Modifier files are .txt files that allow for easy database tweaks that apply when the application is loaded up.

Their primary use is to allow for Homebrew changes or tweaks to spells without needing to input a full homebrew version.

The following operations are supported:

 - **level change** _Overwrites the spell's level_
 - **school_change** _Overwrites the spell's school_
 - **class_add** _Adds classes to the spell's list of classes
 - **class_change** _Overwrites the spell's list of classes

Example:
```
Flaming Potato; class_add: bard, ranger
```
