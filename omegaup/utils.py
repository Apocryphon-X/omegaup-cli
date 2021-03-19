import importlib.resources
import json
import sys
import time

import blessed
import requests
import stdiomask

from . import menus as HELP_MODULE
from . import models as JSON_MODULE

ENTRYPOINT = "https://omegaup.com"

# Read the list of colors in: 
# https://blessed.readthedocs.io/en/latest/colors.html

# Status Prefixes:
add_status      =  blessed.Terminal().olivedrab1("[+] ")
remove_status   =  blessed.Terminal().orangered("[-] ")
question_status =  blessed.Terminal().deepskyblue("[?] ")
info_status     =  blessed.Terminal().gold("[i] ")
error_status    =  blessed.Terminal().crimson("[✗] ")
ok_status       =  blessed.Terminal().lawngreen("[✓] ")

# Veredicts:

ac_verdict = blessed.Terminal().lawngreen("[✓]: AC - Tu solución fue aceptada!")
pa_verdict = blessed.Terminal().yellow("[i]: PA - Tu solución fue parcialmente aceptada.")
wa_verdict = blessed.Terminal().crimson("[✗]: WA - Respuesta incorrecta.")
je_verdict = blessed.Terminal().white_on_firebrick3("[!]: JE - Ocurrio un error inesperado con el evaluador!")
ce_verdict = blessed.Terminal().orangered("[i]: CE - Error de compilación.")

rte_verdict = blessed.Terminal().lightslateblue("[✗]: RTE - Tu programa se cerro de forma inesperada.")
mle_verdict = blessed.Terminal().darkorange("[i]: MLE - Tu solución excedio el limite de memoria.")
ole_verdict = blessed.Terminal().dodgerblue("[i]: OLE - Limite de salida excedido. (¿Imprimiste de mas?)")
tle_verdict = blessed.Terminal().firebrick1("[i]: TLE - Tu programa excedio el limite de tiempo.")

def get_dict(res_name):
    with importlib.resources.open_text(JSON_MODULE, res_name + ".json") as target_file:
        return json.load(target_file)

def get_help(help_name):
    return importlib.resources.read_text(HELP_MODULE, 
        help_name + ".txt")
