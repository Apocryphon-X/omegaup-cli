
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

    problem_alias = None

    # If the actual path is environment, then import the metadata
    try: 
        with open(".ucl_metadata", "r") as environment_data:
            print(info_status + "Entorno detectado, importando metadatos del problema...")
            meta_data = json.load(environment_data)
            problem_alias = meta_data["alias"]
    except FileNotFoundError:
        problem_alias = input(question_status + "Alias de el problema: ")

    submit_path = input(add_status + "Archivo a enviar: ")

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

def setup_env(target_session, problem_alias):
    
    print(info_status + "Conectando con OmegaUp... (Esperando respuesta)")
    problem_details = Problem(target_session).details(problem_alias)
    json_details = problem_details.json()

    # print(json.dumps(json_details, indent = 4, sort_keys = True))
    print(ok_status + "Conexión exitosa!")
    problem_markdown = json_details["statement"]["markdown"].splitlines()
    sample_inputs, sample_outputs = extract_cases(problem_markdown)

    problem_id = str(json_details["problem_id"])

    # Checking if environment already exists
    try:
        os.mkdir(problem_id)
        os.mkdir(problem_id + "/casos-ucl")
    except FileExistsError:
        print(error_status + "Ya existe un entorno para este problema.")
        return

    # Adding test cases to the environment
    idx = 0
    for input_case in sample_inputs:
        new_case_path = problem_id + "/casos-ucl/caso_" + str(idx) + ".in"
        with open(new_case_path, "w") as new_case:
            for line in input_case:
                new_case.write(line + "\n")
        idx += 1

    idx = 0
    for output_case in sample_outputs:
        new_case_path = problem_id + "/casos-ucl/caso_" + str(idx) + ".out"
        with open(new_case_path, "w") as new_case:
            for line in output_case:
                new_case.write(line + "\n")
        idx += 1

    # Adding Problem redaction
    with open(problem_id + "/Redacción.md", "w") as markdown_file:
        for line in problem_markdown:
            markdown_file.write(line + "\n")
    
    # Dumping meta data of the problem
    with open(problem_id + "/.ucl_metadata", "w") as meta_data_file:
        json.dump(json_details, meta_data_file)

    print(ok_status + "Entorno generado ", end = "")
    print("en el directorio: \"" + str(problem_id) + "/\"")

def test_env():

    env_path = os.getcwd()
    dir_content = os.listdir(env_path)

    if not ".ucl_metadata" in dir_content:
        print(error_status + "No se detecto ningun entorno en el directorio actual.")
        return

    print(info_status + "Buscando directorio \"casos-ucl/\"...")
    if not "casos-ucl" in dir_content:
        print(error_status + "Directorio con casos no encontrado.")
        return

    file_name = input(question_status + "Archivo a probar: ") 
    _, file_extension = os.path.splitext(file_name)

    if file_extension == ".cpp": 
        p = subprocess.Popen(["g++", "-std=c++11", file_name, "-o", "result.out"])
        if p.wait() != 0:
            return

    cases_dir_content = os.listdir("casos-ucl")

    input_cases = []
    output_cases = []
    for file_name in cases_dir_content:
        if file_name.endswith(".in"):  input_cases.append(file_name)
        if file_name.endswith(".out"): output_cases.append(file_name)

    case_idx = 0
    for case in input_cases:
        case_name, _ = os.path.splitext(case)
        # expected_output_idx = output_cases.index(case_name + ".out")

        with open("./casos-ucl/" + case_name + ".in", "r") as input_data:
            with open("./casos-ucl/" + case_name + ".out", "r") as output_data:
                with open("./casos-ucl/" + case_name + "-result.out", "w") as result_output:
                    exe_code = subprocess.Popen("./result.out", stdin = input_data, stdout = result_output)
                    exe_code.wait()
                with open("./casos-ucl/" + case_name + "-result.out", "r") as result_output:
                    if output_data.read() != result_output.read():
                        print(error_status + "Caso de prueba #" + str(case_idx) + " no aprobado.")
                    else:
                        print(ok_status + "Caso de prueba #" + str(case_idx) + " aprobado.")


def main():

    main_session = requests.Session()

    if len(sys.argv) <= 1:
        show_guide("main")

    # Submit statement
    elif "envio" in sys.argv:
        submit_idx = sys.argv.index("envio")
        if submit_idx + 1 >= len(sys.argv):
            show_guide("run")
        else:
            run_arg = sys.argv[submit_idx + 1]

            # Subcommands statement
            if run_arg == "subir":
                submit_success, submit_guid = make_submit(main_session)
                if submit_success:
                    with cli_terminal.hidden_cursor():
                        follow_submit(main_session, submit_guid)

    # Environment statement
    elif "entorno" in sys.argv:
        env_idx = sys.argv.index("entorno")
        if env_idx + 1 >= len(sys.argv):
            print(error_status + "Falta un argumento.")
        else:
            env_arg = sys.argv[env_idx + 1]

            # Subcommands statement
            if env_arg == "crear":
                target_alias = input(question_status + "Alias de el problema: ")
                setup_env(main_session, target_alias)
            if env_arg == "probar":
                test_env()
                    



if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")

