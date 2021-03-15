
# Little implementation of the OmegaUp API

from .utils import *
from .user import *
from .run import *

def show_help():
    print(" ")
    print("Trabaja de manera mas rapida en OmegaUp, sin salir del terminal!")
    print(" ")
    print("USO: up <comando> <subcomando> [banderas]")
    print(" ")
    print("COMANDOS CENTRALES ")
    print(" ├─ envio ........ Realiza y administra envios")
    print(" ├─ usuario ...... Administra tu usuario")
    print(" ├─ concurso ..... Administra concursos")
    print(" ├─ dudas ........ Envia clarificaciones")
    print(" ├─ problema ..... Administra y crea problemas")
    print(" └─ curso ........ Administra cursos")
    print(" ")

def main():

    main_session = requests.Session()

    if(len(sys.argv) == 1):
        show_help()
        exit()

    coder_user = input(question_status + "Ingresa tu usuario o email: ")
    coder_pass = stdiomask.getpass(question_status + "Ingresa tu contraseña: ", mask = "*")

    login_response = User(main_session).login(coder_user, coder_pass)
    json_response = login_response.json()

    if "status" in json_response:
        if json_response["status"] == "ok":
            auth_token = json_response["auth_token"]
            print(ok_status + "Inicio de sesión exitoso!")

            # Temporal Test Code
            # print("Probando Run/Create API...")
            # print(omegaup.Run(main_session).create("CLI-test1", "aplusb",
            #      "tests/source.cpp", "cpp11-gcc").json())
        else:
            print(error_status + json_response["error"])

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

