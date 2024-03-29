# -*- coding: utf-8 -*-

# import importlib.resources
import json
import pathlib
import random
import string
import subprocess
import sys
import time
import datetime
import typing

import blessed
import click
import omegaup.api
import requests
import stdiomask

ENTRYPOINT = "https://omegaup.com/"

HOME_PATH = pathlib.Path.home()
AUTH_DATA = HOME_PATH.joinpath(".ucl-data")

# Read the list of colors in:
# https://blessed.readthedocs.io/en/latest/colors.html
cli_terminal = blessed.Terminal()

# Veredicts:
ac_verdict = cli_terminal.lawngreen("[✓] AC - Your solution was accepted!")
pa_verdict = cli_terminal.gold("[i] PA - Your solution was partially accepted.")
wa_verdict = cli_terminal.crimson("[✗] WA - Wrong answer.")
je_verdict = cli_terminal.white_on_firebrick3(
    "[!] JE - An unexpected error occurred with the evaluator, omegaUp is already reviewing the incident."
)
ce_verdict = cli_terminal.white_on_darkorange3("[!] CE - Compilation error")
ve_verdict = cli_terminal.white_on_firebrick3("[!] VE - Validator error.")

rfe_verdict = cli_terminal.firebrick1("[!] RFE - Restricted function error.")
rte_verdict = cli_terminal.lightslateblue("[✗] RTE - Your program closed unexpectedly.")
mle_verdict = cli_terminal.darkorange2(
    "[i] MLE - Your solution exceeded the memory limit."
)
ole_verdict = cli_terminal.dodgerblue(
    "[i] OLE - Output limit exceeded. (Did you overprint?)."
)
tle_verdict = cli_terminal.gold("[i] TLE - Your program exceeded the time limit.")

# Easy access
omegaup_verdicts = {
    "AC": ac_verdict,
    "PA": pa_verdict,
    "WA": wa_verdict,
    "JE": je_verdict,
    "CE": ce_verdict,
    "VE": ve_verdict,
    "RTE": rte_verdict,
    "MLE": mle_verdict,
    "OLE": ole_verdict,
    "TLE": tle_verdict,
    "RFE": rfe_verdict,
}

# Status Prefixes:
add_status = cli_terminal.greenyellow("[+]")
remove_status = cli_terminal.orangered("[-]")
question_status = cli_terminal.deepskyblue("[?]")
info_status = cli_terminal.slateblue2("[i]")
error_status = cli_terminal.crimson("[✗]")
ok_status = cli_terminal.lawngreen("[✓]")


def get_auth_data():
    with open(AUTH_DATA, "r") as target_file:
        auth_dict = json.load(target_file)

        token_name = auth_dict["token_name"]
        api_token = auth_dict["token"]

        return token_name, api_token


def get_client():
    _, api_token = get_auth_data()
    return omegaup.api.Client(api_token=api_token)


# def get_help(help_name):
#    return importlib.resources.read_text(HELP_MODULE,
#        help_name + ".txt")
#
# Added new "help" directory in order to avoid hardcoding
# def show_guide(target_menu):
#    if target_menu == "main" : print(get_help("main-help"))
#    if target_menu == "run" : print(get_help("run-help"))


def get_credentials():
    print(f"{info_status} Enter your access credentials: ")
    coder_user = input(f"{question_status} Username or email: ")
    coder_pass = stdiomask.getpass(f"{question_status} Password: ", mask="*")

    return coder_user, coder_pass


def test_login():

    cr_username, cr_password = get_credentials()

    req_data = {"password": cr_password, "usernameOrEmail": cr_username}
    req_response = requests.post(url=ENTRYPOINT + "api/user/login", data=req_data)

    json_response = req_response.json()

    if "status" in json_response:
        if json_response["status"] == "ok":
            print(f"{ok_status} Successful login!\n")
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
        elif reg_mode == 1:
            tmp_input.append(line)
        elif reg_mode == 2:
            tmp_output.append(line)

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


def get_randseq(text):
    return text + ("".join(random.sample(string.ascii_letters + string.digits, 20)))
