
# Little implementation of the OmegaUp API

from .run import *
from .user import *
from .utils import *


# Add new "help" directory in order to avoid hardcoding?
def show_guide(target_menu):
    if target_menu == "main" : print(get_help("main-help"))
    if target_menu == "run" : print(get_help("run-help"))

def make_login(target_session):
    coder_user = input(question_status + "Ingresa tu usuario o email: ")
    coder_pass = stdiomask.getpass(question_status + "Ingresa tu contraseña: ", mask = "*")

    login_response = User(target_session).login(coder_user, coder_pass)
    json_response = login_response.json()

    if "status" in json_response:
        if json_response["status"] == "ok":
            print(ok_status + "Inicio de sesión exitoso!\n")
            return True

        print(error_status + json_response["error"] + "\n")
        return False
    return False

def make_submit(target_session):
    if not make_login(target_session):
        return

    submit_path = input(add_status + "Archivo a enviar: ")
    problem_alias = input(question_status + "Alias de el problema: ")

    success, run_response = Run(target_session).create(submit_path, problem_alias)

    if type(run_response) != type(None):
        json_response = run_response.json()

    if not success:
        print(error_status + "Archivo no encontrado, verifica si la ruta es correcta.")
    else:
        print(ok_status + "Envio realizado con exito.")
        # print(run_response.json()) # Debugging

def main():

    main_session = requests.Session()

    if len(sys.argv) <= 1:
        show_guide("main")
    elif "envio" in sys.argv:
        submit_idx = sys.argv.index("envio")
        if submit_idx + 1 >= len(sys.argv):
            show_guide("run")
        else:
            cli_arg = sys.argv[submit_idx + 1]
            if cli_arg == "subir":
                make_submit(main_session)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

