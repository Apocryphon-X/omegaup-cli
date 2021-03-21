
# Little implementation of
# the OmegaUp API
from .problem import *
from .run import *
from .user import *
from .utils import *


# Added new "help" directory in order to avoid hardcoding
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

    getting_file_success, run_response = Run(target_session).create(submit_path, problem_alias)

    if type(run_response) != type(None):
        # This will be useful for keeping track of submits
        json_response = run_response.json() 

    if not getting_file_success:
        print(error_status + "Archivo no encontrado, verifica si la ruta es correcta.")
        return False, None
    else:
        if "status" in json_response:
            if json_response["status"] == "ok":
                print(ok_status + "Envio realizado con exito.")
                return True, json_response["guid"]

            print(error_status + json_response["error"])
            return False, None
        return False, None
        
def follow_submit(target_session, run_guid):
    
    # Debugging Output
    # print(json.dumps(json_response, indent = 4, sort_keys = True))

    run_status_response = Run(target_session).status(run_guid)
    json_response = run_status_response.json()
    print(info_status + "Evaluación en curso. (Esperando veredicto)")

    
    print(info_status + "Actualizando", end = "", flush = True)
    while json_response["status"] == "waiting":
        run_status_response = Run(target_session).status(run_guid)
        json_response = run_status_response.json()
        
        for _ in range(3):
            print(".", end = "", flush = True)
            time.sleep(1)

        print(cli_terminal.move_left(3) + cli_terminal.clear_eol, 
            end = "", flush = True)

    print("\r", end = "")

    if json_response["status"] == "ready":
        if json_response["verdict"] == "AC" : print(ac_verdict) 
        if json_response["verdict"] == "WA" : print(wa_verdict)
        if json_response["verdict"] == "CE" : print(ce_verdict)
        if json_response["verdict"] == "JE" : print(je_verdict)
        if json_response["verdict"] == "PA" : print(pa_verdict) 

        if json_response["verdict"] == "RTE" : print(rte_verdict) 
        if json_response["verdict"] == "MLE" : print(mle_verdict) 
        if json_response["verdict"] == "OLE" : print(ole_verdict) 
        if json_response["verdict"] == "TLE" : print(tle_verdict)

def setup_lab(target_session, problem_alias):
    if not make_login(target_session):
        return

    problem_details = Problem(target_session).details(problem_alias)
    json_details = problem_details.json()

    print(json.dumps(json_details, indent = 4, sort_keys = True))

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
                submit_success, submit_guid = make_submit(main_session)
                if submit_success:
                    with cli_terminal.hidden_cursor():
                        follow_submit(main_session, submit_guid)
    elif "test" in sys.argv: 
        setup_lab(main_session, "aplusb")


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

