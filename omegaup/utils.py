import importlib.resources
import json
import os
import sys
import time

import blessed
import requests
import stdiomask

from . import menus as HELP_MODULE
from . import models as JSON_MODULE

ENTRYPOINT = "https://omegaup.com"
cli_terminal = blessed.Terminal()

# Read the list of colors in: 
# https://blessed.readthedocs.io/en/latest/colors.html

# Status Prefixes:
add_status      =  cli_terminal.olivedrab1("[+] ")
remove_status   =  cli_terminal.orangered("[-] ")
question_status =  cli_terminal.deepskyblue("[?] ")
info_status     =  cli_terminal.gold("[i] ")
error_status    =  cli_terminal.crimson("[✗] ")
ok_status       =  cli_terminal.lawngreen("[✓] ")

# Veredicts:
ac_verdict = cli_terminal.lawngreen("[✓]: AC - Tu solución fue aceptada!")
pa_verdict = cli_terminal.yellow("[i]: PA - Tu solución fue parcialmente aceptada.")
wa_verdict = cli_terminal.crimson("[✗]: WA - Respuesta incorrecta.")
je_verdict = cli_terminal.white_on_firebrick3("[!]: JE - Ocurrio un error inesperado con el evaluador!")
ce_verdict = cli_terminal.orangered("[i]: CE - Error de compilación.")

rte_verdict = cli_terminal.lightslateblue("[✗]: RTE - Tu programa se cerro de forma inesperada.")
mle_verdict = cli_terminal.darkorange("[i]: MLE - Tu solución excedio el limite de memoria.")
ole_verdict = cli_terminal.dodgerblue("[i]: OLE - Limite de salida excedido. (¿Imprimiste de mas?)")
tle_verdict = cli_terminal.firebrick1("[i]: TLE - Tu programa excedio el limite de tiempo.")

def get_dict(res_name):
    with importlib.resources.open_text(JSON_MODULE, res_name + ".json") as target_file:
        return json.load(target_file)

def get_help(help_name):
    return importlib.resources.read_text(HELP_MODULE, 
        help_name + ".txt")
