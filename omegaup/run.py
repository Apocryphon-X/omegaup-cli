from omegaup.core import *

class Run:
    endpoint = ENTRYPOINT + "/api/run"
    def  __init__(self, target_session):
        self.session = target_session

    # Creates a new run.
    def create(self, contest_alias, problem_alias, source_path, language):
        run_data = get_dict(JSON_PATH + "api/run/create")

        run_data["contest_alias"] = contest_alias
        run_data["problem_alias"] = problem_alias
        run_data["language"] = language

        with open(source_path, "r") as target_file:
            run_data["source"] = target_file.read()

        return self.session.post(url = self.endpoint + "/create",
             params = run_data)

