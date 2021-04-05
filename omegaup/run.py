from .utils import *

class Run:
    endpoint = ENTRYPOINT + "/api/run"
    def __init__(self, target_session):
        self.session = target_session  

    # Creates a new run.
    def create(self, source_path, problem_alias, language = "cpp11-gcc", contest_alias = None):
        run_data = get_dict("api-run-create")

        run_data["contest_alias"] = contest_alias
        run_data["problem_alias"] = problem_alias
        run_data["language"] = language

        try:
            with open(source_path, "r") as target_file:
                run_data["source"] = target_file.read()
        except FileNotFoundError:
            return False, None

        return True, self.session.post(url = self.endpoint + "/create",
            params = run_data)

    def details(self, run_guid):
        run_data = get_dict("api-run-details")

        run_data["run_alias"] = run_guid
        return self.session.post(url = self.endpoint + "/details", 
            params = run_data)
    
    def status(self, run_guid):
        run_data = get_dict("api-run-status")

        run_data["run_alias"] = run_guid
        return self.session.post(url = self.endpoint + "/status",
            params = run_data)

