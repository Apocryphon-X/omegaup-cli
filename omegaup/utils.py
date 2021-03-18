import importlib.resources
import json
import sys

import blessed
import requests
import stdiomask

from . import menus as HELP_MODULE
from . import models as JSON_MODULE

ENTRYPOINT = "https://omegaup.com"

# Read the list of colors in: 
# https://blessed.readthedocs.io/en/latest/colors.html

# Status Prefixes:
add_status = blessed.Terminal().limegreen("[+] ")
remove_status = blessed.Terminal().orangered("[-] ")
question_status = blessed.Terminal().deepskyblue("[?] ")
error_status = blessed.Terminal().crimson("[!] ")
ok_status = blessed.Terminal().lawngreen("[✓] ")

def get_dict(res_name):
    with importlib.resources.open_text(JSON_MODULE, res_name + ".json") as target_file:
        return json.load(target_file)

def get_help(help_name):
    return importlib.resources.read_text(HELP_MODULE, 
        help_name + ".txt")
