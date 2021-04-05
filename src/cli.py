

# General imports and some util definitions
from .utils import *

# Added new "help" directory in order to avoid hardcoding
def show_guide(target_menu):
    if target_menu == "main" : print(get_help("main-help"))
    if target_menu == "run" : print(get_help("run-help"))

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

def main():

   # Checking if there is information
    if not pathlib.Path.is_file(AUTH_DATA):
        print(f"{info_status} No se encontro información de uso previo.")
        print(f"{info_status} Estableciendo configuracion inicial de la CLI...\n")

        print(f"{question_status} Seleccione la opción de su preferencia:")
        print("[1] Proporcionar un APIToken ya existente.")
        print("[2] Generar un nuevo APIToken.")

        answer = "0"
        while answer != "1" and answer != "2":
            answer = input(f"{question_status} Opción: ")
            if answer != "1" and answer != "2": 
                print(f"{error_status} Ingrese una opción valida!")

        if answer == "1":
            api_token = input(f"{question_status} Token: ")
        if answer == "2":
            success, r_username, r_password = False, None, None
            while not success:
                success, r_username, r_password = test_login()
            
            first_use_ctx = omegaup.api.Client(username=r_username, password=r_password)
            token_name = input(f"{question_status} Ingrese el nombre de el token que desea crear: ")

            api_response = first_use_ctx.user.createAPIToken(name = token_name)
            print(api_response)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

