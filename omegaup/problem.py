from .utils import *

class Problem:
    endpoint = ENTRYPOINT + "/api/problem"
    def __init__(self, target_session):
        self.session = target_session
    
    def details(self, problem_alias, contest_alias = None, lang = "es", 
        prevent_problemset_open = None, problemset_id = None,
            show_solvers = False, statement_type = None):
    
        problem_data = get_dict("api-problem-details")

        problem_data["problem_alias"] = problem_alias
        problem_data["contest_alias"] = contest_alias
        problem_data["lang"] = lang
        problem_data["prevent_problemset_open"] = prevent_problemset_open
        problem_data["problemset_id"] = problemset_id
        problem_data["show_solvers"] = show_solvers
        problem_data["statement_type"] = statement_type

        return self.session.post(url = self.endpoint + "/details", 
            params = problem_data)


    
