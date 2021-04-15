
# General imports and some util definitions
from .utils import *

@click.group()
def main():

    TOKEN_NAME = None
    API_TOKEN = None

    # Checking if Auth information already exists
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
            API_TOKEN = input(f"{question_status} Token: ")
        if answer == "2":
            success, r_username, r_password = False, None, None
            while not success:
                success, r_username, r_password = test_login()

            first_use_ctx = omegaup.api.Client(username=r_username, password=r_password)
            TOKEN_NAME = input(f"{question_status} Ingrese el nombre de el token que desea crear: ")

            api_response = first_use_ctx.user.createAPIToken(name = TOKEN_NAME)
            API_TOKEN = api_response["token"]

        login_data = {"TOKEN_NAME" : TOKEN_NAME, "token" : API_TOKEN}
        with open(str(AUTH_DATA), "w") as data_file:
            data_file.write(json.dumps(login_data))
            print(f"{info_status} Token almacenado correctamente!")

    if type(API_TOKEN) == type(None):
        with open(AUTH_DATA, "r") as target_file:
            auth_dict = json.load(target_file)

            TOKEN_NAME = auth_dict["token_name"]
            API_TOKEN = auth_dict["token"]

@main.group()
def run():
    pass

@run.command()
@click.argument("problem_alias")
@click.argument("file_path")
@click.option("-ca", "--contest_alias", default = None)
@click.option("-f/-nf", "--follow/--no-follow", default = True)
def upload(problem_alias, file_path, contest_alias, follow):
    print("Simple Test...")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print("\n" + remove_status + "Hasta luego!")
