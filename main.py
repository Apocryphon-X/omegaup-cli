import api.user # OmegaUp API Endpoints
from utils.data import *

def make_login(acc_user, acc_pass):
    login_data = {
        "password" : acc_pass,
        "usernameOrEmail" : acc_user
    }
    return requests.post(url = api.user.login, data = login_data)

def main():
    up_user = input(question_status + "Ingresa tu usuario o email: ")
    up_pass = stdiomask.getpass(question_status + "Ingresa tu contraseña: ", mask = "*")

    login_response = make_login(up_user, up_pass).json()
    auth_token = None

    if "status" in login_response:
        if login_response["status"] == "ok":
            auth_token = login_response["auth_token"]
            print(ok_status + "Inicio de sesión exitoso!")
        else:
            print(error_status + login_response["error"])

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")
