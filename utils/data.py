import termcolor
import requests
import stdiomask

# Status Prefixes:
add_status = termcolor.colored("[+] ", "green")
ok_status = termcolor.colored("[🗸] ", "green")
remove_status = termcolor.colored("[-] ", "yellow")
question_status = termcolor.colored("[?] ", "blue")
error_status = termcolor.colored("[!] ", "red")
