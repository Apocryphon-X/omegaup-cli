import termcolor
import requests
import json

ADD_SYM = termcolor.colored("[+] ", "green")
QUESTION_SYM = termcolor.colored("[?] ", "cyan")
ERROR_SYM = termcolor.colored("[!] ", "red")

def make_login(acc_user, acc_pass):
    API_LOGIN_URL = "https://omegaup.com/api/user/login/"
    login_data = {
        "password" : acc_pass,
        "usernameOrEmail" : acc_user
    }
    return requests.get(url = API_LOGIN_URL, params = login_data)

def main():
    print(QUESTION_SYM + "Ingresa tu usuario o email: ", end = " ")
    up_user = input()

    print(QUESTION_SYM + "Ingresa tu contraseña: ", end = " ")
    up_pass = input()

    login_response = make_login(up_user, up_pass).json()

    if "status" in login_response:
        if login_response["status"] == "ok":
            print("Inicio de sesión exitoso!")
        else:
            print(ERROR_SYM + login_response["error"])

if __name__ == "__main__":
    main()
