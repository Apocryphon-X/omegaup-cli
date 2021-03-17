import json
import termcolor
import requests
import stdiomask
import sys
import importlib.resources

from . import models as JSON_MODULE
from . import menus as HELP_MODULE

ENTRYPOINT = "https://omegaup.com"

# importlib.import_module('omegaup.models')

# Status Prefixes:
add_status = termcolor.colored("[+] ", "green")
remove_status = termcolor.colored("[-] ", "yellow")
question_status = termcolor.colored("[?] ", "blue")
error_status = termcolor.colored("[!] ", "red", attrs = ["blink"])
ok_status = termcolor.colored("[✓] ", "green")


def get_dict(res_name):
    with importlib.resources.open_text(JSON_MODULE, res_name + ".json") as target_file:
        return json.load(target_file)

def get_help(help_name):
    return importlib.resources.read_text(HELP_MODULE, 
        help_name + ".txt")