# -*- coding: utf-8 -*-

import importlib.resources
import json
import pathlib
import subprocess
import sys
import time
import gettext
from datetime import datetime

import blessed
import click
import omegaup.api
import requests
import stdiomask

ENTRYPOINT = "https://omegaup.com/"

HOME_PATH = pathlib.Path.home()
AUTH_DATA = HOME_PATH.joinpath(".ucl-data")

# Click methods overload
def __format_usage(self, ctx, formatter):
    """Writes the usage line into the formatter.
    This is a low-level method called by :meth:`get_usage`.
    """
    pieces = self.collect_usage_pieces(ctx)
    formatter.write_usage(ctx.command_path, " ".join(pieces), "Uso: ")

def __format_options(self, ctx, formatter):
    """Writes all the options into the formatter if they exist."""
    opts = []
    for param in self.get_params(ctx):
        rv = param.get_help_record(ctx)
        if rv is not None:
            opts.append(rv)

    if opts:
        with formatter.section("Opciones"):
            formatter.write_dl(opts)

def __format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
    """Extra format methods for multi methods that adds all the commands
    after the options.
    """
    commands = []
    for subcommand in self.list_commands(ctx):
        cmd = self.get_command(ctx, subcommand)
        # What is this, the tool lied about a command.  Ignore it
        if cmd is None:
            continue
        if cmd.hidden:
            continue

        commands.append((subcommand, cmd))

    # allow for 3 times the default spacing
    if len(commands):
        limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

        rows = []
        for subcommand, cmd in commands:
            help = cmd.get_short_help_str(limit)
            rows.append((subcommand, help))

        if rows:
            with formatter.section(gettext._("List of commands")):
                formatter.write_dl(rows)

click.Command.format_usage = __format_usage
click.Command.format_options = __format_options
click.MultiCommand.format_commands = __format_commands

# Read the list of colors in: 
# https://blessed.readthedocs.io/en/latest/colors.html
cli_terminal = blessed.Terminal()

# Veredicts:
ac_verdict = cli_terminal.lawngreen("[✓] AC - Tu solución fue aceptada!")
pa_verdict = cli_terminal.gold("[i] PA - Tu solución fue parcialmente aceptada.")
wa_verdict = cli_terminal.crimson("[✗] WA - Respuesta incorrecta.")
je_verdict = cli_terminal.white_on_firebrick3("[!] JE - Ocurrio un error inesperado con el evaluador!")
ce_verdict = cli_terminal.white_on_darkorange3("[!] CE - Error de compilación.")
ve_verdict = cli_terminal.white_on_firebrick3("[!] VE - Error del validador.")

rfe_verdict = cli_terminal.firebrick1("[!] RFE - Uso de función restringida.")
rte_verdict = cli_terminal.lightslateblue("[✗] RTE - Tu programa se cerro de forma inesperada.")
mle_verdict = cli_terminal.darkorange2("[i] MLE - Tu solución excedio el limite de memoria.")
ole_verdict = cli_terminal.dodgerblue("[i] OLE - Limite de salida excedido. (¿Imprimiste de mas?)")
tle_verdict = cli_terminal.gold("[i] TLE - Tu programa excedio el limite de tiempo.")

# Easy access
omegaup_verdicts = {
    "AC" : ac_verdict, "PA" : pa_verdict,
    "WA" : wa_verdict, "JE" : je_verdict,
    "CE" : ce_verdict, "VE" : ve_verdict,

    "RTE" : rte_verdict, "MLE" : mle_verdict,
    "OLE" : ole_verdict, "TLE" : tle_verdict,
    "RFE" : rfe_verdict
}

# Status Prefixes:
add_status      =  cli_terminal.greenyellow("[+]")
remove_status   =  cli_terminal.orangered("[-]")
question_status =  cli_terminal.deepskyblue("[?]")
info_status     =  cli_terminal.slateblue2("[i]")
error_status    =  cli_terminal.crimson("[✗]")
ok_status       =  cli_terminal.lawngreen("[✓]")

def get_auth_data():
    with open(AUTH_DATA, "r") as target_file:
        auth_dict = json.load(target_file)

        token_name = auth_dict["token_name"]
        api_token = auth_dict["token"]

        return token_name, api_token
        
def get_client():
    _, api_token = get_auth_data()
    return omegaup.api.Client(api_token = api_token)

# def get_help(help_name):
#    return importlib.resources.read_text(HELP_MODULE, 
#        help_name + ".txt")
#
# Added new "help" directory in order to avoid hardcoding
# def show_guide(target_menu):
#    if target_menu == "main" : print(get_help("main-help"))
#    if target_menu == "run" : print(get_help("run-help"))

def get_credentials():
    coder_user = input(f"{question_status} Ingresa tu usuario o email: ")
    coder_pass = stdiomask.getpass(f"{question_status} Ingresa tu contraseña: ", mask = "*")

    return coder_user, coder_pass

def test_login():

    cr_username, cr_password = get_credentials()

    req_data = {"password": cr_password, "usernameOrEmail" : cr_username}
    req_response = requests.post(url = ENTRYPOINT + "api/user/login", data = req_data)

    json_response = req_response.json()

    if "status" in json_response:
        if json_response["status"] == "ok":
            print(f"{ok_status} Inicio de sesión exitoso!\n")
            return True, cr_username, cr_password

        error_msg = json_response["error"]
        print(f"{error_status} {error_msg}\n")

        return False, None, None
    return False, None, None

# Some problems doesnt have "settings" -> "cases" list,
# despite having examples in "statement" -> "markdown".

# I.e: "aplusb" problem
def extract_cases(markdown):
    
    input_cases, output_cases = [], []
    tmp_input, tmp_output = [], []

    reg_mode = 0

    for line in markdown:
        if line.startswith("||"): 
            line = line.replace(" ", "")
        elif reg_mode == 1: tmp_input.append(line)
        elif reg_mode == 2: tmp_output.append(line)

        if line == "||input":
            reg_mode = 1
            if tmp_output:
                output_cases.append(tmp_output)
                tmp_output = []

        if line == "||output": 
            reg_mode = 2
            if tmp_input:
                input_cases.append(tmp_input)
                tmp_input = []
        
        if line == "||description":
            reg_mode = 0
            if tmp_output:
                output_cases.append(tmp_output)
                tmp_output = []
            
        if line == "||end":
            reg_mode = 0
            if tmp_output:
                output_cases.append(tmp_output)
                tmp_output = []

    return input_cases, output_cases
    