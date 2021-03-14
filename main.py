# Little implementation of the OmegaUp API
import omegaup

from utils.data import *

main_session = requests.Session()

def submit_code(contest_alias, problem_alias, submit_language, source_path):
    with open(source_path) as target_file:
        submit_data = {
            "contest_alias" : contest_alias,
            "problem_alias" : problem_alias,
            "language" : submit_language,
            "source" : target_file.read()
        }
        return main_session.post(url = omegaup.run.create, data = submit_data)

def main():

    up_user = input(question_status + "Ingresa tu usuario o email: ")
    up_pass = stdiomask.getpass(question_status + "Ingresa tu contraseña: ", mask = "*")

    login_response = omegaup.User(main_session).login(up_user, up_pass)
    json_response = login_response.json()

    if "status" in json_response:
        if json_response["status"] == "ok":
            auth_token = json_response["auth_token"]
            print(ok_status + "Inicio de sesión exitoso!")

            print("Testing Run/Create API...")
            print(omegaup.Run(main_session).create("CLI-test1", "aplusb",
                "tests/source.cpp", "cpp11-gcc").json())
        else:
            print(error_status + json_response["error"])

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

