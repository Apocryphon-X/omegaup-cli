# OmegaUp API Endpoints
import api.user
import api.run

from utils.data import *

main_session = requests.Session()

def make_login(acc_user, acc_pass):
    login_data = {
        "password" : acc_pass,
        "usernameOrEmail" : acc_user
    }
    return main_session.post(url = api.user.login, data = login_data)

def submit_code(contest_alias, problem_alias, submit_language, source_path):
    with open(source_path) as target_file:
        submit_data = {
            "contest_alias" : contest_alias,
            "problem_alias" : problem_alias,
            "language" : submit_language,
            "source" : target_file.read()
        }
        return main_session.post(url = api.run.create, data = submit_data)

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

