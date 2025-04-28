# This file contains global variables that should be consistent in all GM_Tools child scripts (as well as the main script)
# This primarily includes color hex-strings and positioning data for GUI placement
# This takes most variables from a config file
import json
from random import choice as randchoice

with open("dynamic/gm_tools_config.json", mode="rb") as c_file:
    config = json.load(c_file)
# What sources to load
SOURCE_INCLUDE = config["include_sources"]
# What profile to use on launch
DEFAULT_PROFILE = config["default profile"]
# Module specific variables
SCROLL_MAX = config["scroll_generator"]["scroll_max"]
MAX_DICE_DISPLAY = config["dice_roller"]["dice_max"]
EDIT_MODE = config["crafting_rules"]["editMode"]
MONSTER_IMAGES = config["monster_lookup"]["images"]
MONSTER_CUSTOM_DROPDOWNS = config["monster_lookup"]["custom_dropdowns"]
MONSTER_CUSTOM_SIZE_DROPDOWN = config["monster_lookup"]["size_dropdown"]
MONSTER_CUSTOM_SIZE_DEFAULT = config["monster_lookup"]["size_default"]
MONSTER_CUSTOM_TYPE_DROPDOWN = config["monster_lookup"]["type_dropdown"]
MONSTER_CUSTOM_TYPE_DEFAULT = config["monster_lookup"]["type_default"]
sources_txt = config["metadata"]["sources_txt"]
sources_dict = config["metadata"]["sources_dict"]
publishers_txt = []
publishers_dict = config["metadata"]["publisher_dict"]
for publisher in publishers_dict:
    publishers_txt.append(publisher)
# Application Dimension configuration
B_DIST = config["dimensions"]["border_distance"]
WIN_W = config["dimensions"]["app_width"]
WIN_H = config["dimensions"]["app_height"]
MID_W = WIN_W//2
MID_H = WIN_H//2
THRD_W = WIN_W//3
THRD_H = WIN_H//3
# Define the custom colors used across the GUI
OFF_WHITE = config["colors"]["white"]
BLACK_BASE = config["colors"]["black"]
RICH_BLUE = config["colors"]["blue"]
SCROLL_TAN = config["colors"]["tan"]
DUNE_TAN = config["colors"]["dark_tan"]
DARK_RED = config["colors"]["dark_red"]
BLANK_GRAY = config["colors"]["gray"]
DARK_GRAY = config["colors"]["dark_gray"]
ORANGE = config["colors"]["orange"]
PURPLE_RED = config["colors"]["purpleish_red"]
BLUE_PURPLE = config["colors"]["blueish_purple"]
BRIGHT_RED = config["colors"]["red"]
BRIGHT_GREEN = config["colors"]["green"]
MUDDY_ORANGE = config["colors"]["muddy_orange"]
MUDDY_RED = config["colors"]["muddy_red"]
DEEP_BLUE = config["colors"]["deep_blue"]
# Get the image dictionary from the config file
bIP = "static/images/"
APP_IMAGES = config["images"]
# Get the sound dictionary from the config file
bSP = 'static/sounds/'
APP_SOUNDS = config["sounds"]
