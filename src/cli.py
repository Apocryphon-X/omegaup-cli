
# General imports and some util definitions
from .utils import *

@click.group()
def main():

    # Checking if Auth information already exists
    if not pathlib.Path.is_file(AUTH_DATA):

        token_name = None
        api_token = None

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
            api_token = api_response["token"]

        login_data = {"token_name" : token_name, "token" : api_token}
        with open(str(AUTH_DATA), "w") as data_file:
            data_file.write(json.dumps(login_data))
            print(f"{info_status} Token almacenado correctamente!")

@main.group()
def run():
    pass

@run.command()
@click.argument("problem_alias")
@click.argument("file_path")
@click.option("-l", "--language", default = "cpp11-gcc")
@click.option("-ca", "--contest_alias", default = None)
@click.option("-nf", "--no-follow", is_flag=True, default = False)
def upload(problem_alias, file_path, language, contest_alias, no_follow):

    try:
        source_code = None
        with open(file_path, "r") as target_file:
            source_code = target_file.read()

        ctx = get_client()
        api_dict = ctx.run.create(
            contest_alias = contest_alias,
            problem_alias = problem_alias,
            source = source_code,
            language = language
        )

        #   print(api_dict)

        if "status" in api_dict:
            if api_dict["status"] == "ok":
                print(ok_status + "Envio realizado con exito.")
            else:
                print(error_status + api_dict["error"])

        if no_follow: 
            return

        run_guid = api_dict["guid"]
        api_response = ctx.run.status(run_alias=run_guid)
        print(info_status + "Evaluación en curso. (Esperando veredicto)")
        
        print(info_status + "Actualizando", end = "", flush = True)
        while api_response["status"] == "waiting":
            api_response = ctx.run.status(run_alias=run_guid)
            
            for _ in range(3):
                print(".", end = "", flush = True)
                time.sleep(1)

            print(cli_terminal.move_left(3) + cli_terminal.clear_eol, 
                end = "", flush = True)

        print("\r", end = "")

        if api_response["status"] == "ready":
            api_verdict = api_response["verdict"]
            if api_verdict == "AC" : print(ac_verdict) 
            if api_verdict == "WA" : print(wa_verdict)
            if api_verdict == "CE" : print(ce_verdict)
            if api_verdict == "JE" : print(je_verdict)
            if api_verdict == "PA" : print(pa_verdict) 

            if api_verdict == "RTE" : print(rte_verdict) 
            if api_verdict == "MLE" : print(mle_verdict) 
            if api_verdict == "OLE" : print(ole_verdict) 
            if api_verdict == "TLE" : print(tle_verdict)

    except FileNotFoundError:
        print(f"{error_status} Archivo no encontrado, verifica si la ruta es correcta.")

if __name__ == "__main__":
    main()