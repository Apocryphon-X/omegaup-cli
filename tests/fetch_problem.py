import requests

# import logging

# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

ENTRYPOINT = "https://www.omegaup.com"

def main():

    fetch_data = {
        "problem_alias" : "COMI-a-b",
        "contest_alias" : None,
        "lang" : "es",
        "prevent_problemset_open" : None,
        "problemset_id" : None,
        "show_solvers" : False,
        "statement_type" : None
    }

    print(fetch_data)

    problem_details = requests.post(url =  ENTRYPOINT + "/api/problem/details", params = fetch_data)
    json_problem_details = problem_details.json()

    print(problem_details)
    print(json_problem_details)
    print("\nSTATEMENT: ")
    print(json_problem_details["statement"])

if __name__ == "__main__":
    main()
