# -*- coding: utf-8 -*-

# General imports and some util definitions
from .utils import *


@click.group()
def main():
    # Check for Auth information in AUTH_DATA path
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
            token_name = input(
                f"{question_status} Ingrese el nombre de el token que desea crear: "
            )

            api_response = first_use_ctx.user.createAPIToken(name=token_name)
            api_token = api_response["token"]

        login_data = {"token_name": token_name, "token": api_token}
        with open(str(AUTH_DATA), "w") as data_file:
            data_file.write(json.dumps(login_data, indent=4, sort_keys=True))
            print(f"{info_status} Token almacenado correctamente!")


@main.group()
def run():
    pass


@run.command()
@click.argument("guid")
@click.option("-r", "--raw", is_flag=True, default=False)
def source(guid, raw):

    ctx = get_client()
    api_dict = ctx.run.source(run_alias=guid)

    if raw:
        print(json.dumps(api_dict, indent=4, sort_keys=True))
        return

    print(api_dict["source"])


@run.command()
@click.argument("problem_alias")
@click.argument("file_path")
@click.option("-l", "--language", default="cpp11-gcc")
@click.option("-ca", "--contest_alias", default=None)
@click.option("-nf", "--no-follow", is_flag=True, default=False)
@click.option("-r", "--raw", is_flag=True, default=False)
def upload(problem_alias, file_path, language, contest_alias, no_follow, raw):
    try:
        source_code = None
        with open(file_path, "r") as target_file:
            source_code = target_file.read()

        ctx = get_client()
        api_dict = ctx.run.create(
            contest_alias=contest_alias,
            problem_alias=problem_alias,
            source=source_code,
            language=language,
        )

        if "status" in api_dict and not raw:
            if api_dict["status"] == "ok":
                print(f"{ok_status} Envío realizado con éxito.")
            else:
                print(error_status + api_dict["error"])

        if no_follow:
            return

        run_guid = api_dict["guid"]
        api_response = ctx.run.status(run_alias=run_guid)

        if not raw:
            print(f"{info_status} Evaluación en curso. (Esperando veredicto)")
            print(f"{info_status} Actualizando", end="", flush=True)

        while api_response["status"] == "waiting":
            api_response = ctx.run.status(run_alias=run_guid)
            for _ in range(3):
                if not raw:
                    print(".", end="", flush=True)
                time.sleep(1)

            if not raw:
                print(
                    cli_terminal.move_left(3) + cli_terminal.clear_eol,
                    end="",
                    flush=True,
                )

        print(f"\r{' ' * 25}")

        if api_response["status"] == "ready":
            if not raw:
                api_verdict = api_response["verdict"]
                print(f"{omegaup_verdicts[api_verdict]}\n")

                print(f"{info_status} Lenguaje:\t{api_response['language']}")
                print(f"{info_status} GUID:\t{api_response['guid']}\n")

                print(f"{info_status} Puntaje:\t{api_response['score'] * 100:.2f} %")
                print(f"{info_status} Memoria:\t{api_response['memory'] / 1048576} MiB")
                print(f"{info_status} Tiempo: \t{api_response['runtime'] / 1000} s")
            else:
                print(json.dumps(api_response, indent=4, sort_keys=True))
    except FileNotFoundError:
        if not raw:
            print(
                f"{error_status} Archivo no encontrado, verifica si la ruta es correcta."
            )


@main.group()
def contest():
    pass


@contest.command()
@click.argument("contest_alias")
@click.option("-r", "--raw", is_flag=True, default=False)
def details(contest_alias, raw):
    ctx = get_client()

    api_dict = ctx.contest.details(contest_alias=contest_alias)

    if raw:
        print(json.dumps(api_dict, indent=4, sort_keys=True))
        return

    access = None

    if api_dict["admission_mode"] == "public":
        access = cli_terminal.lawngreen("Publico")
    if api_dict["admission_mode"] == "private":
        access = cli_terminal.red("Privado")

    start_time = cli_terminal.greenyellow(
        str(datetime.fromtimestamp(api_dict["start_time"]))
    )
    finish_time = cli_terminal.greenyellow(
        str(datetime.fromtimestamp(api_dict["finish_time"]))
    )

    print(" ")
    print(f"{info_status} Nombre: {api_dict['title']}")
    print(f"{info_status} Acceso: {access}\n")

    print(f"{info_status} Descripción: {api_dict['description']}")
    print(f"{info_status} Organizador: {api_dict['director']}\n")

    print(f"{info_status} Fecha de inicio: {start_time}")
    print(f"{info_status} Fecha de fin:    {finish_time}\n")

    print(f"{info_status} {len(api_dict['problems'])} Problemas: \n")

    for problem in api_dict["problems"]:
        print(f"{info_status} {problem['letter']}. {problem['title']}")
        print(f"{info_status} Puntos: {problem['points']}")
        print(f"{info_status} Alias: {problem['alias']}")
        print(f"{info_status} ID: {problem['problem_id']}\n")


# @run.command()
# def status():
#     pass


@main.group()
def problem():
    pass


@problem.command()
@click.argument("problem_alias")
@click.option("-r", "--raw", is_flag=True, default=False)
def runs(problem_alias, raw):

    ctx = get_client()
    api_dict = ctx.problem.runs(problem_alias=problem_alias)

    if raw:
        print(json.dumps(api_dict, indent=4, sort_keys=True))
        return

    print(f"\n{info_status} {len(api_dict['runs'])} envios:\n")

    print(f"{cli_terminal.gray48('-' * 50)}\n")

    for i_run in api_dict["runs"]:

        submit_date = str(datetime.fromtimestamp(i_run["time"]))
        api_verdict = i_run["verdict"]

        print(f"{omegaup_verdicts[api_verdict]}\n")

        print(f"{info_status} Enviado:\t{submit_date}")
        print(f"{info_status} Lenguaje:\t{i_run['language']}")
        print(f"{info_status} GUID:\t{i_run['guid']}\n")

        print(f"{info_status} Puntaje:\t{i_run['score'] * 100:.2f} %")
        print(f"{info_status} Memoria:\t{i_run['memory'] / 1048576} MiB")
        print(f"{info_status} Tiempo: \t{i_run['runtime'] / 1000} s\n")

        print(f"{cli_terminal.gray48('-' * 50)}\n")


# @problem.command()
# @click.argument("problem_alias")
# @click.option("-v", "--visibility", default = "private")
# @click.option("-t", "--title")
# @click.option("-s", "--source")
# @click.option("-il", "--input-limit")
# @click.option("-ol", "--output-limit")
# @click.option("-ml", "--memory-limit")
# @click.option("-tl", "--time-limit")
# @click.option("-ec", "--email-clarifications", is_flag = True, default = False)
# def settings(
#     problem_alias,
#     visibility,
#     title,
#     source,
#     input_limit,
#     output_limit,
#     memory_limit,
#     email_clarifications
# ):
#     try:
#         ctx = get_client()
#         api_dict = ctx.problem.create(
#             problem_alias = problem_alias,
#             visibility = visibility,
#             title = title,
#             source = source,
#             input_limit = input_limit,
#             ouput_limit = output_limit,
#             memory_limit = memory_limit,
#             email_clarifications = email_clarifications
#         )
#     except FileNotFoundError:
#         print(f"{error_status} Archivo no encontrado, verifica si la ruta es correcta.")

if __name__ == "__main__":
    main()
