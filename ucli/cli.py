# -*- coding: utf-8 -*-

# General imports and some util definitions
from .utils import *


@click.group()
def main():
    # Check for Auth information in AUTH_DATA path
    if not pathlib.Path.is_file(AUTH_DATA):

        token_name = None
        api_token = None

        print(f"{info_status} Authentication data not found.")
        print(f"{info_status} Setting up CLI configuration...\n")

        print(f"{question_status} Select an option:")
        print("[1] Add an existing API Token.")
        print("[2] Generate a new APIToken.")

        answer = "0"
        while answer not in ["1", "2"]:
            answer = input(f"{question_status} Input: ")
            if answer not in ["1", "2"]:
                print(f"{error_status} Invalid input data! Try again.")

        if answer == "1":
            api_token = stdiomask.getpass(f"{question_status} API Token: ", mask="*")
        if answer == "2":
            success, r_username, r_password = False, None, None
            while not success:
                success, r_username, r_password = test_login()

            first_use_ctx = omegaup.api.Client(username=r_username, password=r_password)
            token_name = input(f"{question_status} Assign a name to this token: ")

            token_name = get_randseq(token_name)
            api_response = first_use_ctx.user.createAPIToken(name=token_name)
            api_token = api_response["token"]

        login_data = {"token_name": token_name, "token": api_token}
        with open(str(AUTH_DATA), "w") as data_file:
            data_file.write(json.dumps(login_data, indent=4, sort_keys=True))
            print(f"{info_status} Token stored correctly!")


@main.group(name="admin", help="")
def admin():
    pass


@admin.command(
    name="platformReportStats", help="Get stats for an overall platform report."
)
@click.option("--end-time", default=None, type=int)
@click.option("--start-time", default=None, type=int)
def platform_report_stats(end_time, start_time):
    ctx = get_client()
    api_dict = ctx.admin.platformReportStats(end_time=end_time, start_time=start_time)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="authorization", help="")
def authorization():
    pass


@authorization.command(name="problem", help="")
@click.argument("problem_alias")
@click.argument("token")
@click.option("--username", default=None)
def problem(problem_alias, token, username):
    ctx = get_client()
    api_dict = ctx.authorization.problem(
        problem_alias=problem_alias, token=token, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="badge", help="")
def badge():
    pass


@badge.command(
    name="badgeDetails",
    help="Returns the number of owners and the first assignation timestamp for a certain badge",
)
@click.option("--badge-alias", default=None, type=str)
def badge_details(badge_alias):
    ctx = get_client()
    api_dict = ctx.badge.badgeDetails(badge_alias=badge_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@badge.command(name="list", help="Returns a list of existing badges")
def list_():
    ctx = get_client()
    api_dict = ctx.badge.list()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@badge.command(
    name="myBadgeAssignationTime",
    help="Returns a the assignation timestamp of a badge for current user.",
)
@click.option("--badge-alias", default=None, type=str)
def my_badge_assignation_time(badge_alias):
    ctx = get_client()
    api_dict = ctx.badge.myBadgeAssignationTime(badge_alias=badge_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@badge.command(name="myList", help="Returns a list of badges owned by current user")
def my_list():
    ctx = get_client()
    api_dict = ctx.badge.myList()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@badge.command(name="userList", help="Returns a list of badges owned by a certain user")
@click.option("--target-username", default=None)
def user_list(target_username):
    ctx = get_client()
    api_dict = ctx.badge.userList(target_username=target_username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="clarification", help="")
def clarification():
    pass


@clarification.command(
    name="create",
    help="Creates a Clarification for a contest or an assignment of a course",
)
@click.argument("message")
@click.argument("problem_alias")
@click.option("--assignment-alias", default=None, type=str)
@click.option("--contest-alias", default=None, type=str)
@click.option("--course-alias", default=None, type=str)
@click.option("--username", default=None, type=str)
def create(
    message, problem_alias, assignment_alias, contest_alias, course_alias, username
):
    ctx = get_client()
    api_dict = ctx.clarification.create(
        message=message,
        problem_alias=problem_alias,
        assignment_alias=assignment_alias,
        contest_alias=contest_alias,
        course_alias=course_alias,
        username=username,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@clarification.command(name="details", help="API for getting a clarification")
@click.argument("clarification_id")
def details(clarification_id):
    ctx = get_client()
    api_dict = ctx.clarification.details(clarification_id=clarification_id)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@clarification.command(name="update", help="Update a clarification")
@click.argument("clarification_id")
@click.option("--answer", default=None, type=str)
@click.option("--message", default=None, type=str)
@click.option("--public", default=None, type=bool)
def update(clarification_id, answer, message, public):
    ctx = get_client()
    api_dict = ctx.clarification.update(
        clarification_id=clarification_id, answer=answer, message=message, public=public
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="client", help="")
def client():
    pass


@client.command(name="query", help="Issues a raw query to the omegaUp API.")
@click.argument("endpoint")
@click.argument("query")
def query(endpoint, payload):
    ctx = get_client()
    api_dict = ctx.client.query(endpoint=endpoint, payload=payload)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="contest", help="")
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
        access = cli_terminal.lawngreen("Public")
    if api_dict["admission_mode"] == "private":
        access = cli_terminal.red("Private")

    start_time = cli_terminal.greenyellow(
        str(datetime.fromtimestamp(api_dict["start_time"]))
    )
    finish_time = cli_terminal.greenyellow(
        str(datetime.fromtimestamp(api_dict["finish_time"]))
    )

    print()
    print(f"{info_status} Tittle:      {api_dict['title']}")
    print(f"{info_status} Access type: {access}\n")

    print(f"{info_status} Description: {api_dict['description']}")
    print(f"{info_status} Organizer:   {api_dict['director']}\n")

    print(f"{info_status} Start time:  {start_time}")
    print(f"{info_status} Finish time: {finish_time}\n")

    print(f"{info_status} {len(api_dict['problems'])} problems: \n")

    for problem in api_dict["problems"]:
        print(f"{info_status} {problem['letter']}. {problem['title']}")
        print(f"{info_status} Points: {problem['points']}")
        print(f"{info_status} Alias:  {problem['alias']}")
        print(f"{info_status} ID:     {problem['problem_id']}\n")


@contest.command(
    name="activityReport", help="Returns a report with all user activity for a contest."
)
@click.argument("contest_alias")
@click.option("--length", default=None, type=int)
@click.option("--page", default=None, type=int)
@click.option("--token", default=None, type=str)
def activity_report(contest_alias, length, page, token):
    ctx = get_client()
    api_dict = ctx.contest.activityReport(
        contest_alias=contest_alias, length=length, page=page, token=token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="addAdmin", help="Adds an admin to a contest")
@click.argument("contest_alias")
@click.argument("username_or_email")
def add_admin(contest_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.contest.addAdmin(
        contest_alias=contest_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="addGroup", help="Adds a group to a contest")
@click.argument("contest_alias")
@click.argument("group")
def add_group(contest_alias, group):
    ctx = get_client()
    api_dict = ctx.contest.addGroup(contest_alias=contest_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="addGroupAdmin", help="Adds a group admin to a contest")
@click.argument("contest_alias")
@click.argument("group")
def add_group_admin(contest_alias, group):
    ctx = get_client()
    api_dict = ctx.contest.addGroupAdmin(contest_alias=contest_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="addProblem", help="Adds a problem to a contest")
@click.argument("contest_alias")
@click.argument("order_in_contest")
@click.argument("points")
@click.argument("problem_alias")
@click.option("--commit", default=None, type=str)
def add_problem(contest_alias, order_in_contest, points, problem_alias, commit):
    ctx = get_client()
    api_dict = ctx.contest.addProblem(
        contest_alias=contest_alias,
        order_in_contest=order_in_contest,
        points=points,
        problem_alias=problem_alias,
        commit=commit,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="addUser",
    help="Adds a user to a contest. By default, any user can view details of public contests. Only users added through this API can view private contests",
)
@click.argument("contest_alias")
@click.argument("username_or_email")
def add_user(contest_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.contest.addUser(
        contest_alias=contest_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="adminDetails",
    help="Returns details of a Contest, for administrators. This differs from apiDetails in the sense that it does not attempt to calculate the remaining time from the contest, or register the opened time.",
)
@click.argument("contest_alias")
@click.option("--token", default=None, type=str)
def admin_details(contest_alias, token):
    ctx = get_client()
    api_dict = ctx.contest.adminDetails(contest_alias=contest_alias, token=token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="adminList",
    help="Returns a list of contests where current user has admin rights (or is the director).",
)
@click.option("--page", default=None, type=int)
@click.option("--page-size", default=None, type=int)
@click.option("--show-archived", default=None, type=bool)
def admin_list(page, page_size, show_archived):
    ctx = get_client()
    api_dict = ctx.contest.adminList(
        page=page, page_size=page_size, show_archived=show_archived
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="admins", help="Returns all contest administrators")
@click.argument("contest_alias")
def admins(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.admins(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="arbitrateRequest", help="")
@click.argument("contest_alias")
@click.argument("username")
@click.option("--note", default=None, type=str)
@click.option("--resolution", default=None)
def arbitrate_request(contest_alias, username, note, resolution):
    ctx = get_client()
    api_dict = ctx.contest.arbitrateRequest(
        contest_alias=contest_alias, username=username, note=note, resolution=resolution
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="archive", help="Archives or Unarchives a contest if user is the creator"
)
@click.argument("contest_alias")
@click.option("--archive", default=None, type=bool)
def archive(contest_alias, archive):
    ctx = get_client()
    api_dict = ctx.contest.archive(contest_alias=contest_alias, archive=archive)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="clarifications", help="Get clarifications of a contest")
@click.argument("contest_alias")
@click.argument("offset")
@click.argument("rowcount")
def clarifications(contest_alias, offset, rowcount):
    ctx = get_client()
    api_dict = ctx.contest.clarifications(
        contest_alias=contest_alias, offset=offset, rowcount=rowcount
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="clone", help="Clone a contest")
@click.argument("contest_alias")
@click.argument("description")
@click.argument("start_time")
@click.argument("title")
@click.option("--alias", default=None, type=str)
@click.option("--auth-token", default=None, type=str)
def clone(contest_alias, description, start_time, title, alias, auth_token):
    ctx = get_client()
    api_dict = ctx.contest.clone(
        contest_alias=contest_alias,
        description=description,
        start_time=start_time,
        title=title,
        alias=alias,
        auth_token=auth_token,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="contestants",
    help="Return users who participate in a contest, as long as contest admin has chosen to ask for users information and contestants have previously agreed to share their information.",
)
@click.argument("contest_alias")
def contestants(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.contestants(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="create", help="Creates a new contest")
@click.option("--admission-mode", default=None)
@click.option("--alias", default=None)
@click.option("--contest-for-teams", default=None, type=bool)
@click.option("--description", default=None)
@click.option("--feedback", default=None)
@click.option("--finish-time", default=None)
@click.option("--languages", default=None)
@click.option("--needs-basic-information", default=None, type=bool)
@click.option("--partial-score", default=None, type=bool)
@click.option("--penalty", default=None)
@click.option("--penalty-calc-policy", default=None)
@click.option("--penalty-type", default=None)
@click.option("--points-decay-factor", default=None)
@click.option("--problems", default=None, type=str)
@click.option("--requests-user-information", default=None)
@click.option("--scoreboard", default=None)
@click.option("--show-scoreboard-after", default=None)
@click.option("--start-time", default=None)
@click.option("--submissions-gap", default=None)
@click.option("--teams-group-alias", default=None, type=str)
@click.option("--title", default=None)
@click.option("--window-length", default=None, type=int)
def create(
    admission_mode,
    alias,
    contest_for_teams,
    description,
    feedback,
    finish_time,
    languages,
    needs_basic_information,
    partial_score,
    penalty,
    penalty_calc_policy,
    penalty_type,
    points_decay_factor,
    problems,
    requests_user_information,
    scoreboard,
    show_scoreboard_after,
    start_time,
    submissions_gap,
    teams_group_alias,
    title,
    window_length,
):
    ctx = get_client()
    api_dict = ctx.contest.create(
        admission_mode=admission_mode,
        alias=alias,
        contest_for_teams=contest_for_teams,
        description=description,
        feedback=feedback,
        finish_time=finish_time,
        languages=languages,
        needs_basic_information=needs_basic_information,
        partial_score=partial_score,
        penalty=penalty,
        penalty_calc_policy=penalty_calc_policy,
        penalty_type=penalty_type,
        points_decay_factor=points_decay_factor,
        problems=problems,
        requests_user_information=requests_user_information,
        scoreboard=scoreboard,
        show_scoreboard_after=show_scoreboard_after,
        start_time=start_time,
        submissions_gap=submissions_gap,
        teams_group_alias=teams_group_alias,
        title=title,
        window_length=window_length,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="createVirtual", help="")
@click.argument("alias")
@click.argument("start_time")
def create_virtual(alias, start_time):
    ctx = get_client()
    api_dict = ctx.contest.createVirtual(alias=alias, start_time=start_time)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="list", help="Returns a list of contests")
@click.argument("page")
@click.argument("page_size")
@click.argument("query")
@click.argument("tab_name")
@click.option("--active", default=None, type=int)
@click.option("--admission-mode", default=None)
@click.option("--participating", default=None, type=int)
@click.option("--recommended", default=None, type=int)
def list_(
    page, page_size, query, tab_name, active, admission_mode, participating, recommended
):
    ctx = get_client()
    api_dict = ctx.contest.list(
        page=page,
        page_size=page_size,
        query=query,
        tab_name=tab_name,
        active=active,
        admission_mode=admission_mode,
        participating=participating,
        recommended=recommended,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="listParticipating",
    help="Returns a list of contests where current user is participating in",
)
@click.option("--page", default=None, type=int)
@click.option("--page-size", default=None, type=int)
@click.option("--query", default=None, type=str)
@click.option("--show-archived", default=None, type=bool)
def list_participating(page, page_size, query, show_archived):
    ctx = get_client()
    api_dict = ctx.contest.listParticipating(
        page=page, page_size=page_size, query=query, show_archived=show_archived
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="myList", help="Returns a list of contests where current user is the director"
)
@click.option("--page", default=None, type=int)
@click.option("--page-size", default=None, type=int)
@click.option("--query", default=None, type=str)
@click.option("--show-archived", default=None, type=bool)
def my_list(page, page_size, query, show_archived):
    ctx = get_client()
    api_dict = ctx.contest.myList(
        page=page, page_size=page_size, query=query, show_archived=show_archived
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="open", help="Joins a contest - explicitly adds a identity to a contest."
)
@click.argument("contest_alias")
@click.argument("privacy_git_object_id")
@click.argument("statement_type")
@click.option("--share-user-information", default=None, type=bool)
@click.option("--token", default=None, type=str)
def open_(
    contest_alias, privacy_git_object_id, statement_type, share_user_information, token
):
    ctx = get_client()
    api_dict = ctx.contest.open(
        contest_alias=contest_alias,
        privacy_git_object_id=privacy_git_object_id,
        statement_type=statement_type,
        share_user_information=share_user_information,
        token=token,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="problemClarifications", help="Get clarifications of problem in a contest"
)
@click.argument("contest_alias")
@click.argument("offset")
@click.argument("problem_alias")
@click.argument("rowcount")
def problem_clarifications(contest_alias, offset, problem_alias, rowcount):
    ctx = get_client()
    api_dict = ctx.contest.problemClarifications(
        contest_alias=contest_alias,
        offset=offset,
        problem_alias=problem_alias,
        rowcount=rowcount,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="problems", help="Gets the problems from a contest")
@click.argument("contest_alias")
def problems(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.problems(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="publicDetails", help="")
@click.argument("contest_alias")
def public_details(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.publicDetails(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="registerForContest", help="")
@click.argument("contest_alias")
def register_for_contest(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.registerForContest(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="removeAdmin", help="Removes an admin from a contest")
@click.argument("contest_alias")
@click.argument("username_or_email")
def remove_admin(contest_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.contest.removeAdmin(
        contest_alias=contest_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="removeGroup", help="Removes a group from a contest")
@click.argument("contest_alias")
@click.argument("group")
def remove_group(contest_alias, group):
    ctx = get_client()
    api_dict = ctx.contest.removeGroup(contest_alias=contest_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="removeGroupAdmin", help="Removes a group admin from a contest")
@click.argument("contest_alias")
@click.argument("group")
def remove_group_admin(contest_alias, group):
    ctx = get_client()
    api_dict = ctx.contest.removeGroupAdmin(contest_alias=contest_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="removeProblem", help="Removes a problem from a contest")
@click.argument("contest_alias")
@click.argument("problem_alias")
def remove_problem(contest_alias, problem_alias):
    ctx = get_client()
    api_dict = ctx.contest.removeProblem(
        contest_alias=contest_alias, problem_alias=problem_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="removeUser", help="Remove a user from a private contest")
@click.argument("contest_alias")
@click.argument("username_or_email")
def remove_user(contest_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.contest.removeUser(
        contest_alias=contest_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="replaceTeamsGroup", help="Replace the teams group assigned to a contest"
)
@click.argument("contest_alias")
@click.argument("teams_group_alias")
def replace_teams_group(contest_alias, teams_group_alias):
    ctx = get_client()
    api_dict = ctx.contest.replaceTeamsGroup(
        contest_alias=contest_alias, teams_group_alias=teams_group_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="report", help="Returns a detailed report of the contest")
@click.argument("contest_alias")
@click.option("--auth-token", default=None, type=str)
@click.option("--filter-by", default=None, type=str)
def report(contest_alias, auth_token, filter_by):
    ctx = get_client()
    api_dict = ctx.contest.report(
        contest_alias=contest_alias, auth_token=auth_token, filterBy=filter_by
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="requests", help="")
@click.argument("contest_alias")
def requests(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.requests(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="role", help="")
@click.argument("contest_alias")
@click.option("--token", default=None, type=str)
def role(contest_alias, token):
    ctx = get_client()
    api_dict = ctx.contest.role(contest_alias=contest_alias, token=token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="runs", help="Returns all runs for a contest")
@click.argument("contest_alias")
@click.argument("problem_alias")
@click.option("--language", default=None, type=str)
@click.option("--offset", default=None, type=int)
@click.option("--rowcount", default=None, type=int)
@click.option("--status", default=None, type=str)
@click.option("--username", default=None, type=str)
@click.option("--verdict", default=None, type=str)
def runs(
    contest_alias, problem_alias, language, offset, rowcount, status, username, verdict
):
    ctx = get_client()
    api_dict = ctx.contest.runs(
        contest_alias=contest_alias,
        problem_alias=problem_alias,
        language=language,
        offset=offset,
        rowcount=rowcount,
        status=status,
        username=username,
        verdict=verdict,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="runsDiff",
    help="Return a report of which runs would change due to a version change.",
)
@click.argument("contest_alias")
@click.argument("version")
@click.option("--problem-alias", default=None, type=str)
def runs_diff(contest_alias, version, problem_alias):
    ctx = get_client()
    api_dict = ctx.contest.runsDiff(
        contest_alias=contest_alias, version=version, problem_alias=problem_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="scoreboard", help="Returns the Scoreboard")
@click.argument("contest_alias")
@click.option("--token", default=None, type=str)
def scoreboard(contest_alias, token):
    ctx = get_client()
    api_dict = ctx.contest.scoreboard(contest_alias=contest_alias, token=token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="scoreboardEvents", help="Returns the Scoreboard events")
@click.argument("contest_alias")
@click.option("--token", default=None, type=str)
def scoreboard_events(contest_alias, token):
    ctx = get_client()
    api_dict = ctx.contest.scoreboardEvents(contest_alias=contest_alias, token=token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="scoreboardMerge",
    help="Gets the accomulative scoreboard for an array of contests",
)
@click.argument("contest_aliases")
@click.option("--contest-params", default=None)
@click.option("--usernames-filter", default=None, type=str)
def scoreboard_merge(contest_aliases, contest_params, usernames_filter):
    ctx = get_client()
    api_dict = ctx.contest.scoreboardMerge(
        contest_aliases=contest_aliases,
        contest_params=contest_params,
        usernames_filter=usernames_filter,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="searchUsers", help="Search users in contest")
@click.argument("contest_alias")
@click.option("--query", default=None, type=str)
def search_users(contest_alias, query):
    ctx = get_client()
    api_dict = ctx.contest.searchUsers(contest_alias=contest_alias, query=query)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="setRecommended",
    help="Given a contest_alias, sets the recommended flag on/off. Only omegaUp admins can call this API.",
)
@click.argument("contest_alias")
@click.option("--value", default=None, type=bool)
def set_recommended(contest_alias, value):
    ctx = get_client()
    api_dict = ctx.contest.setRecommended(contest_alias=contest_alias, value=value)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="stats", help="Stats of a contest")
@click.option("--contest-alias", default=None, type=str)
def stats(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.stats(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="update", help="Update a Contest")
@click.argument("contest_alias")
@click.argument("finish_time")
@click.argument("submissions_gap")
@click.argument("window_length")
@click.option("--admission-mode", default=None, type=str)
@click.option("--alias", default=None, type=str)
@click.option("--contest-for-teams", default=None, type=bool)
@click.option("--default-show-all-contestants-in-scoreboard", default=None, type=bool)
@click.option("--description", default=None, type=str)
@click.option("--feedback", default=None)
@click.option("--languages", default=None)
@click.option("--needs-basic-information", default=None, type=bool)
@click.option("--partial-score", default=None, type=bool)
@click.option("--penalty", default=None, type=int)
@click.option("--penalty-calc-policy", default=None)
@click.option("--penalty-type", default=None)
@click.option("--points-decay-factor", default=None, type=float)
@click.option("--problems", default=None, type=str)
@click.option("--requests-user-information", default=None, type=str)
@click.option("--scoreboard", default=None, type=float)
@click.option("--show-scoreboard-after", default=None, type=bool)
@click.option("--start-time", default=None, type=datetime.datetime)
@click.option("--teams-group-alias", default=None, type=str)
@click.option("--title", default=None, type=str)
def update(
    contest_alias,
    finish_time,
    submissions_gap,
    window_length,
    admission_mode,
    alias,
    contest_for_teams,
    default_show_all_contestants_in_scoreboard,
    description,
    feedback,
    languages,
    needs_basic_information,
    partial_score,
    penalty,
    penalty_calc_policy,
    penalty_type,
    points_decay_factor,
    problems,
    requests_user_information,
    scoreboard,
    show_scoreboard_after,
    start_time,
    teams_group_alias,
    title,
):
    ctx = get_client()
    api_dict = ctx.contest.update(
        contest_alias=contest_alias,
        finish_time=finish_time,
        submissions_gap=submissions_gap,
        window_length=window_length,
        admission_mode=admission_mode,
        alias=alias,
        contest_for_teams=contest_for_teams,
        default_show_all_contestants_in_scoreboard=default_show_all_contestants_in_scoreboard,
        description=description,
        feedback=feedback,
        languages=languages,
        needs_basic_information=needs_basic_information,
        partial_score=partial_score,
        penalty=penalty,
        penalty_calc_policy=penalty_calc_policy,
        penalty_type=penalty_type,
        points_decay_factor=points_decay_factor,
        problems=problems,
        requests_user_information=requests_user_information,
        scoreboard=scoreboard,
        show_scoreboard_after=show_scoreboard_after,
        start_time=start_time,
        teams_group_alias=teams_group_alias,
        title=title,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(
    name="updateEndTimeForIdentity",
    help="Update Contest end time for an identity when window_length option is turned on",
)
@click.argument("contest_alias")
@click.argument("end_time")
@click.argument("username")
def update_end_time_for_identity(contest_alias, end_time, username):
    ctx = get_client()
    api_dict = ctx.contest.updateEndTimeForIdentity(
        contest_alias=contest_alias, end_time=end_time, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@contest.command(name="users", help="Returns ALL identities participating in a contest")
@click.argument("contest_alias")
def users(contest_alias):
    ctx = get_client()
    api_dict = ctx.contest.users(contest_alias=contest_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="course", help="")
def course():
    pass


@course.command(
    name="activityReport", help="Returns a report with all user activity for a course."
)
@click.argument("course_alias")
@click.option("--length", default=None, type=int)
@click.option("--page", default=None, type=int)
def activity_report(course_alias, length, page):
    ctx = get_client()
    api_dict = ctx.course.activityReport(
        course_alias=course_alias, length=length, page=page
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="addAdmin", help="Adds an admin to a course")
@click.argument("course_alias")
@click.argument("username_or_email")
def add_admin(course_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.course.addAdmin(
        course_alias=course_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="addGroupAdmin", help="Adds an group admin to a course")
@click.argument("course_alias")
@click.argument("group")
def add_group_admin(course_alias, group):
    ctx = get_client()
    api_dict = ctx.course.addGroupAdmin(course_alias=course_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="addProblem", help="Adds a problem to an assignment")
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("points")
@click.argument("problem_alias")
@click.option("--commit", default=None, type=str)
@click.option("--is-extra-problem", default=None, type=bool)
def add_problem(
    assignment_alias, course_alias, points, problem_alias, commit, is_extra_problem
):
    ctx = get_client()
    api_dict = ctx.course.addProblem(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        points=points,
        problem_alias=problem_alias,
        commit=commit,
        is_extra_problem=is_extra_problem,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="addStudent", help="Add Student to Course.")
@click.argument("accept_teacher_git_object_id")
@click.argument("course_alias")
@click.argument("privacy_git_object_id")
@click.argument("share_user_information")
@click.argument("statement_type")
@click.argument("username_or_email")
@click.option("--accept-teacher", default=None, type=bool)
def add_student(
    accept_teacher_git_object_id,
    course_alias,
    privacy_git_object_id,
    share_user_information,
    statement_type,
    username_or_email,
    accept_teacher,
):
    ctx = get_client()
    api_dict = ctx.course.addStudent(
        accept_teacher_git_object_id=accept_teacher_git_object_id,
        course_alias=course_alias,
        privacy_git_object_id=privacy_git_object_id,
        share_user_information=share_user_information,
        statement_type=statement_type,
        usernameOrEmail=username_or_email,
        accept_teacher=accept_teacher,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="adminDetails", help="Returns all details of a given Course")
@click.argument("alias")
def admin_details(alias):
    ctx = get_client()
    api_dict = ctx.course.adminDetails(alias=alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="admins", help="Returns all course administrators")
@click.argument("course_alias")
def admins(course_alias):
    ctx = get_client()
    api_dict = ctx.course.admins(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="arbitrateRequest",
    help="Stores the resolution given to a certain request made by a contestant interested to join the course.",
)
@click.argument("course_alias")
@click.argument("resolution")
@click.argument("username")
def arbitrate_request(course_alias, resolution, username):
    ctx = get_client()
    api_dict = ctx.course.arbitrateRequest(
        course_alias=course_alias, resolution=resolution, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="archive", help="Archives or un-archives a course")
@click.argument("archive")
@click.argument("course_alias")
def archive(archive, course_alias):
    ctx = get_client()
    api_dict = ctx.course.archive(archive=archive, course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="assignmentDetails", help="Returns details of a given assignment")
@click.argument("assignment")
@click.argument("course")
@click.option("--token", default=None, type=str)
def assignment_details(assignment, course, token):
    ctx = get_client()
    api_dict = ctx.course.assignmentDetails(
        assignment=assignment, course=course, token=token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="assignmentScoreboard", help="Gets Scoreboard for an assignment")
@click.argument("assignment")
@click.argument("course")
@click.option("--token", default=None, type=str)
def assignment_scoreboard(assignment, course, token):
    ctx = get_client()
    api_dict = ctx.course.assignmentScoreboard(
        assignment=assignment, course=course, token=token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="assignmentScoreboardEvents", help="Returns the Scoreboard events")
@click.argument("assignment")
@click.argument("course")
@click.option("--token", default=None, type=str)
def assignment_scoreboard_events(assignment, course, token):
    ctx = get_client()
    api_dict = ctx.course.assignmentScoreboardEvents(
        assignment=assignment, course=course, token=token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="clarifications", help="Gets the clarifications of all assignments in a course"
)
@click.argument("course_alias")
@click.argument("offset")
@click.argument("rowcount")
def clarifications(course_alias, offset, rowcount):
    ctx = get_client()
    api_dict = ctx.course.clarifications(
        course_alias=course_alias, offset=offset, rowcount=rowcount
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="clone", help="Clone a course")
@click.argument("alias")
@click.argument("course_alias")
@click.argument("name")
@click.argument("start_time")
@click.option("--token", default=None, type=str)
def clone(alias, course_alias, name, start_time, token):
    ctx = get_client()
    api_dict = ctx.course.clone(
        alias=alias,
        course_alias=course_alias,
        name=name,
        start_time=start_time,
        token=token,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="create", help="Create new course API")
@click.option("--admission-mode", default=None)
@click.option("--alias", default=None)
@click.option("--description", default=None)
@click.option("--finish-time", default=None)
@click.option("--languages", default=None)
@click.option("--level", default=None, type=str)
@click.option("--name", default=None)
@click.option("--needs-basic-information", default=None)
@click.option("--objective", default=None, type=str)
@click.option("--public", default=None)
@click.option("--requests-user-information", default=None)
@click.option("--school-id", default=None)
@click.option("--show-scoreboard", default=None)
@click.option("--start-time", default=None)
@click.option("--unlimited-duration", default=None, type=bool)
def create(
    admission_mode,
    alias,
    description,
    finish_time,
    languages,
    level,
    name,
    needs_basic_information,
    objective,
    public,
    requests_user_information,
    school_id,
    show_scoreboard,
    start_time,
    unlimited_duration,
):
    ctx = get_client()
    api_dict = ctx.course.create(
        admission_mode=admission_mode,
        alias=alias,
        description=description,
        finish_time=finish_time,
        languages=languages,
        level=level,
        name=name,
        needs_basic_information=needs_basic_information,
        objective=objective,
        public=public,
        requests_user_information=requests_user_information,
        school_id=school_id,
        show_scoreboard=show_scoreboard,
        start_time=start_time,
        unlimited_duration=unlimited_duration,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="createAssignment", help="API to Create an assignment")
@click.argument("course_alias")
@click.option("--alias", default=None)
@click.option("--assignment-type", default=None)
@click.option("--description", default=None)
@click.option("--finish-time", default=None)
@click.option("--name", default=None)
@click.option("--order", default=None, type=int)
@click.option("--problems", default=None, type=str)
@click.option("--publish-time-delay", default=None)
@click.option("--start-time", default=None)
@click.option("--unlimited-duration", default=None, type=bool)
def create_assignment(
    course_alias,
    alias,
    assignment_type,
    description,
    finish_time,
    name,
    order,
    problems,
    publish_time_delay,
    start_time,
    unlimited_duration,
):
    ctx = get_client()
    api_dict = ctx.course.createAssignment(
        course_alias=course_alias,
        alias=alias,
        assignment_type=assignment_type,
        description=description,
        finish_time=finish_time,
        name=name,
        order=order,
        problems=problems,
        publish_time_delay=publish_time_delay,
        start_time=start_time,
        unlimited_duration=unlimited_duration,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="details", help="Returns details of a given course")
@click.argument("alias")
def details(alias):
    ctx = get_client()
    api_dict = ctx.course.details(alias=alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="generateTokenForCloneCourse", help="")
@click.argument("course_alias")
def generate_token_for_clone_course(course_alias):
    ctx = get_client()
    api_dict = ctx.course.generateTokenForCloneCourse(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="getProblemUsers", help="")
@click.argument("course_alias")
@click.argument("problem_alias")
def get_problem_users(course_alias, problem_alias):
    ctx = get_client()
    api_dict = ctx.course.getProblemUsers(
        course_alias=course_alias, problem_alias=problem_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="introDetails",
    help="Show course intro only on public courses when user is not yet registered",
)
@click.argument("course_alias")
def intro_details(course_alias):
    ctx = get_client()
    api_dict = ctx.course.introDetails(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="listAssignments", help="List course assignments")
@click.argument("course_alias")
def list_assignments(course_alias):
    ctx = get_client()
    api_dict = ctx.course.listAssignments(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="listSolvedProblems", help="Get Problems solved by users of a course"
)
@click.argument("course_alias")
def list_solved_problems(course_alias):
    ctx = get_client()
    api_dict = ctx.course.listSolvedProblems(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="listStudents", help="List students in a course")
@click.argument("course_alias")
def list_students(course_alias):
    ctx = get_client()
    api_dict = ctx.course.listStudents(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="listUnsolvedProblems", help="Get Problems unsolved by users of a course"
)
@click.argument("course_alias")
def list_unsolved_problems(course_alias):
    ctx = get_client()
    api_dict = ctx.course.listUnsolvedProblems(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="myProgress", help="Returns details of a given course")
@click.argument("alias")
def my_progress(alias):
    ctx = get_client()
    api_dict = ctx.course.myProgress(alias=alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="problemClarifications", help="Get clarifications of problem in a contest"
)
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("offset")
@click.argument("problem_alias")
@click.argument("rowcount")
def problem_clarifications(
    assignment_alias, course_alias, offset, problem_alias, rowcount
):
    ctx = get_client()
    api_dict = ctx.course.problemClarifications(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        offset=offset,
        problem_alias=problem_alias,
        rowcount=rowcount,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="registerForCourse", help="")
@click.argument("course_alias")
@click.option("--accept-teacher", default=None, type=bool)
@click.option("--share-user-information", default=None, type=bool)
def register_for_course(course_alias, accept_teacher, share_user_information):
    ctx = get_client()
    api_dict = ctx.course.registerForCourse(
        course_alias=course_alias,
        accept_teacher=accept_teacher,
        share_user_information=share_user_information,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="removeAdmin", help="Removes an admin from a course")
@click.argument("course_alias")
@click.argument("username_or_email")
def remove_admin(course_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.course.removeAdmin(
        course_alias=course_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="removeAssignment", help="Remove an assignment from a course")
@click.argument("assignment_alias")
@click.argument("course_alias")
def remove_assignment(assignment_alias, course_alias):
    ctx = get_client()
    api_dict = ctx.course.removeAssignment(
        assignment_alias=assignment_alias, course_alias=course_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="removeGroupAdmin", help="Removes a group admin from a course")
@click.argument("course_alias")
@click.argument("group")
def remove_group_admin(course_alias, group):
    ctx = get_client()
    api_dict = ctx.course.removeGroupAdmin(course_alias=course_alias, group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="removeProblem", help="Remove a problem from an assignment")
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("problem_alias")
def remove_problem(assignment_alias, course_alias, problem_alias):
    ctx = get_client()
    api_dict = ctx.course.removeProblem(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        problem_alias=problem_alias,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="removeStudent", help="Remove Student from Course")
@click.argument("course_alias")
@click.argument("username_or_email")
def remove_student(course_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.course.removeStudent(
        course_alias=course_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(
    name="requests",
    help="Returns the list of requests made by participants who are interested to join the course",
)
@click.argument("course_alias")
def requests(course_alias):
    ctx = get_client()
    api_dict = ctx.course.requests(course_alias=course_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="runs", help="Returns all runs for a course")
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.option("--language", default=None, type=str)
@click.option("--offset", default=None, type=int)
@click.option("--problem-alias", default=None, type=str)
@click.option("--rowcount", default=None, type=int)
@click.option("--status", default=None, type=str)
@click.option("--username", default=None, type=str)
@click.option("--verdict", default=None, type=str)
def runs(
    assignment_alias,
    course_alias,
    language,
    offset,
    problem_alias,
    rowcount,
    status,
    username,
    verdict,
):
    ctx = get_client()
    api_dict = ctx.course.runs(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        language=language,
        offset=offset,
        problem_alias=problem_alias,
        rowcount=rowcount,
        status=status,
        username=username,
        verdict=verdict,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="studentProgress", help="")
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("username_or_email")
def student_progress(assignment_alias, course_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.course.studentProgress(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        usernameOrEmail=username_or_email,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="studentsProgress", help="")
@click.argument("course")
@click.argument("length")
@click.argument("page")
def students_progress(course, length, page):
    ctx = get_client()
    api_dict = ctx.course.studentsProgress(course=course, length=length, page=page)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="update", help="Edit Course contents")
@click.argument("alias")
@click.argument("languages")
@click.argument("school_id")
@click.option("--admission-mode", default=None, type=str)
@click.option("--description", default=None, type=str)
@click.option("--finish-time", default=None, type=datetime.datetime)
@click.option("--level", default=None, type=str)
@click.option("--name", default=None, type=str)
@click.option("--needs-basic-information", default=None, type=bool)
@click.option("--objective", default=None, type=str)
@click.option("--requests-user-information", default=None, type=str)
@click.option("--show-scoreboard", default=None, type=bool)
@click.option("--start-time", default=None, type=datetime.datetime)
@click.option("--unlimited-duration", default=None, type=bool)
def update(
    alias,
    languages,
    school_id,
    admission_mode,
    description,
    finish_time,
    level,
    name,
    needs_basic_information,
    objective,
    requests_user_information,
    show_scoreboard,
    start_time,
    unlimited_duration,
):
    ctx = get_client()
    api_dict = ctx.course.update(
        alias=alias,
        languages=languages,
        school_id=school_id,
        admission_mode=admission_mode,
        description=description,
        finish_time=finish_time,
        level=level,
        name=name,
        needs_basic_information=needs_basic_information,
        objective=objective,
        requests_user_information=requests_user_information,
        show_scoreboard=show_scoreboard,
        start_time=start_time,
        unlimited_duration=unlimited_duration,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="updateAssignment", help="Update an assignment")
@click.argument("assignment")
@click.argument("course")
@click.argument("finish_time")
@click.argument("start_time")
@click.option("--unlimited-duration", default=None, type=bool)
def update_assignment(assignment, course, finish_time, start_time, unlimited_duration):
    ctx = get_client()
    api_dict = ctx.course.updateAssignment(
        assignment=assignment,
        course=course,
        finish_time=finish_time,
        start_time=start_time,
        unlimited_duration=unlimited_duration,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="updateAssignmentsOrder", help="")
@click.argument("assignments")
@click.argument("course_alias")
def update_assignments_order(assignments, course_alias):
    ctx = get_client()
    api_dict = ctx.course.updateAssignmentsOrder(
        assignments=assignments, course_alias=course_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@course.command(name="updateProblemsOrder", help="")
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("problems")
def update_problems_order(assignment_alias, course_alias, problems):
    ctx = get_client()
    api_dict = ctx.course.updateProblemsOrder(
        assignment_alias=assignment_alias, course_alias=course_alias, problems=problems
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="grader", help="")
def grader():
    pass


@grader.command(name="status", help="Calls to /status grader")
def status():
    ctx = get_client()
    api_dict = ctx.grader.status()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="group", help="")
def group():
    pass


@group.command(name="addUser", help="Add identity to group")
@click.argument("group_alias")
@click.argument("username_or_email")
def add_user(group_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.group.addUser(
        group_alias=group_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="create", help="New group")
@click.argument("alias")
@click.argument("description")
@click.argument("name")
def create(alias, description, name):
    ctx = get_client()
    api_dict = ctx.group.create(alias=alias, description=description, name=name)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="createScoreboard", help="Create a scoreboard set to a group")
@click.argument("group_alias")
@click.argument("name")
@click.option("--alias", default=None, type=str)
@click.option("--description", default=None, type=str)
def create_scoreboard(group_alias, name, alias, description):
    ctx = get_client()
    api_dict = ctx.group.createScoreboard(
        group_alias=group_alias, name=name, alias=alias, description=description
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="details", help="Details of a group (scoreboards)")
@click.argument("group_alias")
def details(group_alias):
    ctx = get_client()
    api_dict = ctx.group.details(group_alias=group_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(
    name="list",
    help="Returns a list of groups that match a partial name. This returns an array instead of an object since it is used by typeahead.",
)
@click.option("--query", default=None, type=str)
def list_(query):
    ctx = get_client()
    api_dict = ctx.group.list(query=query)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="members", help="Members of a group (usernames only).")
@click.argument("group_alias")
def members(group_alias):
    ctx = get_client()
    api_dict = ctx.group.members(group_alias=group_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="myList", help="Returns a list of groups by owner")
def my_list():
    ctx = get_client()
    api_dict = ctx.group.myList()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="removeUser", help="Remove user from group")
@click.argument("group_alias")
@click.argument("username_or_email")
def remove_user(group_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.group.removeUser(
        group_alias=group_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group.command(name="update", help="Update an existing group")
@click.argument("alias")
@click.argument("description")
@click.argument("name")
def update(alias, description, name):
    ctx = get_client()
    api_dict = ctx.group.update(alias=alias, description=description, name=name)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="groupScoreboard", help="")
def group_scoreboard():
    pass


@group_scoreboard.command(name="addContest", help="Add contest to a group scoreboard")
@click.argument("contest_alias")
@click.argument("group_alias")
@click.argument("scoreboard_alias")
@click.argument("weight")
@click.option("--only-ac", default=None, type=bool)
def add_contest(contest_alias, group_alias, scoreboard_alias, weight, only_ac):
    ctx = get_client()
    api_dict = ctx.groupScoreboard.addContest(
        contest_alias=contest_alias,
        group_alias=group_alias,
        scoreboard_alias=scoreboard_alias,
        weight=weight,
        only_ac=only_ac,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group_scoreboard.command(
    name="details",
    help="Details of a scoreboard. Returns a list with all contests that belong to the given scoreboard_alias",
)
@click.argument("group_alias")
@click.argument("scoreboard_alias")
def details(group_alias, scoreboard_alias):
    ctx = get_client()
    api_dict = ctx.groupScoreboard.details(
        group_alias=group_alias, scoreboard_alias=scoreboard_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group_scoreboard.command(name="list", help="Details of a scoreboard")
@click.option("--group-alias", default=None, type=str)
def list_(group_alias):
    ctx = get_client()
    api_dict = ctx.groupScoreboard.list(group_alias=group_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@group_scoreboard.command(
    name="removeContest", help="Add contest to a group scoreboard"
)
@click.argument("contest_alias")
@click.argument("group_alias")
@click.argument("scoreboard_alias")
def remove_contest(contest_alias, group_alias, scoreboard_alias):
    ctx = get_client()
    api_dict = ctx.groupScoreboard.removeContest(
        contest_alias=contest_alias,
        group_alias=group_alias,
        scoreboard_alias=scoreboard_alias,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="identity", help="")
def identity():
    pass


@identity.command(name="bulkCreate", help="Entry point for Create bulk Identities API")
@click.argument("identities")
@click.option("--group-alias", default=None, type=str)
@click.option("--name", default=None)
@click.option("--username", default=None)
def bulk_create(identities, group_alias, name, username):
    ctx = get_client()
    api_dict = ctx.identity.bulkCreate(
        identities=identities, group_alias=group_alias, name=name, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(
    name="bulkCreateForTeams",
    help="Entry point for Create bulk Identities for teams API",
)
@click.argument("team_group_alias")
@click.argument("team_identities")
def bulk_create_for_teams(team_group_alias, team_identities):
    ctx = get_client()
    api_dict = ctx.identity.bulkCreateForTeams(
        team_group_alias=team_group_alias, team_identities=team_identities
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(
    name="changePassword", help="Entry point for change passowrd of an identity"
)
@click.argument("group_alias")
@click.argument("password")
@click.argument("username")
@click.option("--identities", default=None)
@click.option("--name", default=None)
def change_password(group_alias, password, username, identities, name):
    ctx = get_client()
    api_dict = ctx.identity.changePassword(
        group_alias=group_alias,
        password=password,
        username=username,
        identities=identities,
        name=name,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(name="create", help="Entry point for Create an Identity API")
@click.argument("gender")
@click.argument("name")
@click.argument("password")
@click.argument("school_name")
@click.argument("username")
@click.option("--country-id", default=None, type=str)
@click.option("--group-alias", default=None, type=str)
@click.option("--identities", default=None)
@click.option("--state-id", default=None, type=str)
def create(
    gender,
    name,
    password,
    school_name,
    username,
    country_id,
    group_alias,
    identities,
    state_id,
):
    ctx = get_client()
    api_dict = ctx.identity.create(
        gender=gender,
        name=name,
        password=password,
        school_name=school_name,
        username=username,
        country_id=country_id,
        group_alias=group_alias,
        identities=identities,
        state_id=state_id,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(
    name="selectIdentity",
    help="Entry point for switching between associated identities for a user",
)
@click.argument("username_or_email")
@click.option("--auth-token", default=None, type=str)
def select_identity(username_or_email, auth_token):
    ctx = get_client()
    api_dict = ctx.identity.selectIdentity(
        usernameOrEmail=username_or_email, auth_token=auth_token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(name="update", help="Entry point for Update an Identity API")
@click.argument("gender")
@click.argument("group_alias")
@click.argument("name")
@click.argument("original_username")
@click.argument("school_name")
@click.argument("username")
@click.option("--country-id", default=None, type=str)
@click.option("--identities", default=None)
@click.option("--state-id", default=None, type=str)
def update(
    gender,
    group_alias,
    name,
    original_username,
    school_name,
    username,
    country_id,
    identities,
    state_id,
):
    ctx = get_client()
    api_dict = ctx.identity.update(
        gender=gender,
        group_alias=group_alias,
        name=name,
        original_username=original_username,
        school_name=school_name,
        username=username,
        country_id=country_id,
        identities=identities,
        state_id=state_id,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@identity.command(
    name="updateIdentityTeam", help="Entry point for Update an Identity team API"
)
@click.argument("gender")
@click.argument("group_alias")
@click.argument("name")
@click.argument("original_username")
@click.argument("school_name")
@click.argument("username")
@click.option("--country-id", default=None, type=str)
@click.option("--identities", default=None)
@click.option("--state-id", default=None, type=str)
def update_identity_team(
    gender,
    group_alias,
    name,
    original_username,
    school_name,
    username,
    country_id,
    identities,
    state_id,
):
    ctx = get_client()
    api_dict = ctx.identity.updateIdentityTeam(
        gender=gender,
        group_alias=group_alias,
        name=name,
        original_username=original_username,
        school_name=school_name,
        username=username,
        country_id=country_id,
        identities=identities,
        state_id=state_id,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="notification", help="")
def notification():
    pass


@notification.command(
    name="myList", help="Returns a list of unread notifications for user"
)
def my_list():
    ctx = get_client()
    api_dict = ctx.notification.myList()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@notification.command(
    name="readNotifications", help="Updates notifications as read in database"
)
@click.option("--notifications", default=None)
def read_notifications(notifications):
    ctx = get_client()
    api_dict = ctx.notification.readNotifications(notifications=notifications)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="problem", help="")
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

    print(f"\n{info_status} {len(api_dict['runs'])} Submissions:\n")

    print(f"{cli_terminal.gray48('-' * 50)}\n")

    for i_run in api_dict["runs"]:

        submit_date = str(datetime.fromtimestamp(i_run["time"]))
        api_verdict = i_run["verdict"]

        print(f"{omegaup_verdicts[api_verdict]}\n")

        print(f"{info_status} Submit date:\t{submit_date}")
        print(f"{info_status} Language:\t{i_run['language']}")
        print(f"{info_status} GUID:\t{i_run['guid']}\n")

        print(f"{info_status} Score:\t{i_run['score'] * 100:.2f} %")
        print(f"{info_status} Memory:\t{i_run['memory'] / 1048576} MiB")
        print(f"{info_status} Time: \t{i_run['runtime'] / 1000} s\n")

        print(f"{cli_terminal.gray48('-' * 50)}\n")


@problem.command(name="addAdmin", help="Adds an admin to a problem")
@click.argument("problem_alias")
@click.argument("username_or_email")
def add_admin(problem_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.problem.addAdmin(
        problem_alias=problem_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="addGroupAdmin", help="Adds a group admin to a problem")
@click.argument("group")
@click.argument("problem_alias")
def add_group_admin(group, problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.addGroupAdmin(group=group, problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="addTag", help="Adds a tag to a problem")
@click.argument("name")
@click.argument("problem_alias")
@click.option("--public", default=None, type=bool)
def add_tag(name, problem_alias, public):
    ctx = get_client()
    api_dict = ctx.problem.addTag(name=name, problem_alias=problem_alias, public=public)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="adminList",
    help="Returns a list of problems where current user has admin rights (or is the owner).",
)
@click.argument("page")
@click.argument("page_size")
@click.option("--query", default=None, type=str)
def admin_list(page, page_size, query):
    ctx = get_client()
    api_dict = ctx.problem.adminList(page=page, page_size=page_size, query=query)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="admins", help="Returns all problem administrators")
@click.argument("problem_alias")
def admins(problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.admins(problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="bestScore", help="Returns the best score for a problem")
@click.option("--contest-alias", default=None, type=str)
@click.option("--problem-alias", default=None, type=str)
@click.option("--problemset-id", default=None)
@click.option("--statement-type", default=None, type=str)
@click.option("--username", default=None, type=str)
def best_score(contest_alias, problem_alias, problemset_id, statement_type, username):
    ctx = get_client()
    api_dict = ctx.problem.bestScore(
        contest_alias=contest_alias,
        problem_alias=problem_alias,
        problemset_id=problemset_id,
        statement_type=statement_type,
        username=username,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="clarifications", help="Entry point for Problem clarifications API"
)
@click.argument("problem_alias")
@click.option("--offset", default=None)
@click.option("--rowcount", default=None)
def clarifications(problem_alias, offset, rowcount):
    ctx = get_client()
    api_dict = ctx.problem.clarifications(
        problem_alias=problem_alias, offset=offset, rowcount=rowcount
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="create", help="Create a new problem")
@click.argument("problem_alias")
@click.argument("visibility")
@click.option("--allow-user-add-tags", default=None, type=bool)
@click.option("--email-clarifications", default=None, type=bool)
@click.option("--extra-wall-time", default=None)
@click.option("--group-score-policy", default=None, type=str)
@click.option("--input-limit", default=None)
@click.option("--languages", default=None)
@click.option("--memory-limit", default=None)
@click.option("--output-limit", default=None)
@click.option("--overall-wall-time-limit", default=None)
@click.option("--problem-level", default=None, type=str)
@click.option("--selected-tags", default=None, type=str)
@click.option("--show-diff", default=None, type=str)
@click.option("--source", default=None, type=str)
@click.option("--time-limit", default=None)
@click.option("--title", default=None, type=str)
@click.option("--update-published", default=None, type=str)
@click.option("--validator", default=None, type=str)
@click.option("--validator-time-limit", default=None)
def create(
    problem_alias,
    visibility,
    allow_user_add_tags,
    email_clarifications,
    extra_wall_time,
    group_score_policy,
    input_limit,
    languages,
    memory_limit,
    output_limit,
    overall_wall_time_limit,
    problem_level,
    selected_tags,
    show_diff,
    source,
    time_limit,
    title,
    update_published,
    validator,
    validator_time_limit,
):
    ctx = get_client()
    api_dict = ctx.problem.create(
        problem_alias=problem_alias,
        visibility=visibility,
        allow_user_add_tags=allow_user_add_tags,
        email_clarifications=email_clarifications,
        extra_wall_time=extra_wall_time,
        group_score_policy=group_score_policy,
        input_limit=input_limit,
        languages=languages,
        memory_limit=memory_limit,
        output_limit=output_limit,
        overall_wall_time_limit=overall_wall_time_limit,
        problem_level=problem_level,
        selected_tags=selected_tags,
        show_diff=show_diff,
        source=source,
        time_limit=time_limit,
        title=title,
        update_published=update_published,
        validator=validator,
        validator_time_limit=validator_time_limit,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="delete", help="Removes a problem whether user is the creator")
@click.argument("problem_alias")
def delete(problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.delete(problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="details", help="Entry point for Problem Details API")
@click.argument("problem_alias")
@click.option("--contest-alias", default=None, type=str)
@click.option("--lang", default=None, type=str)
@click.option("--prevent-problemset-open", default=None, type=bool)
@click.option("--problemset-id", default=None, type=int)
@click.option("--show-solvers", default=None, type=bool)
@click.option("--statement-type", default=None, type=str)
def details(
    problem_alias,
    contest_alias,
    lang,
    prevent_problemset_open,
    problemset_id,
    show_solvers,
    statement_type,
):
    ctx = get_client()
    api_dict = ctx.problem.details(
        problem_alias=problem_alias,
        contest_alias=contest_alias,
        lang=lang,
        prevent_problemset_open=prevent_problemset_open,
        problemset_id=problemset_id,
        show_solvers=show_solvers,
        statement_type=statement_type,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="list", help="List of public and user's private problems")
@click.argument("only_quality_seal")
@click.option("--difficulty", default=None, type=str)
@click.option("--difficulty-range", default=None, type=str)
@click.option("--language", default=None)
@click.option("--level", default=None, type=str)
@click.option("--max-difficulty", default=None, type=int)
@click.option("--min-difficulty", default=None, type=int)
@click.option("--min-visibility", default=None, type=int)
@click.option("--offset", default=None)
@click.option("--only-karel", default=None)
@click.option("--order-by", default=None)
@click.option("--page", default=None)
@click.option("--programming-languages", default=None, type=str)
@click.option("--query", default=None, type=str)
@click.option("--require-all-tags", default=None)
@click.option("--rowcount", default=None)
@click.option("--some-tags", default=None)
@click.option("--sort-order", default=None)
def list_(
    only_quality_seal,
    difficulty,
    difficulty_range,
    language,
    level,
    max_difficulty,
    min_difficulty,
    min_visibility,
    offset,
    only_karel,
    order_by,
    page,
    programming_languages,
    query,
    require_all_tags,
    rowcount,
    some_tags,
    sort_order,
):
    ctx = get_client()
    api_dict = ctx.problem.list(
        only_quality_seal=only_quality_seal,
        difficulty=difficulty,
        difficulty_range=difficulty_range,
        language=language,
        level=level,
        max_difficulty=max_difficulty,
        min_difficulty=min_difficulty,
        min_visibility=min_visibility,
        offset=offset,
        only_karel=only_karel,
        order_by=order_by,
        page=page,
        programming_languages=programming_languages,
        query=query,
        require_all_tags=require_all_tags,
        rowcount=rowcount,
        some_tags=some_tags,
        sort_order=sort_order,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="myList", help="Gets a list of problems where current user is the owner"
)
@click.argument("page")
@click.option("--query", default=None, type=str)
@click.option("--rowcount", default=None, type=int)
def my_list(page, query, rowcount):
    ctx = get_client()
    api_dict = ctx.problem.myList(page=page, query=query, rowcount=rowcount)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="randomKarelProblem", help="")
def random_karel_problem():
    ctx = get_client()
    api_dict = ctx.problem.randomKarelProblem()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="randomLanguageProblem", help="")
def random_language_problem():
    ctx = get_client()
    api_dict = ctx.problem.randomLanguageProblem()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="rejudge", help="Rejudge problem")
@click.argument("problem_alias")
def rejudge(problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.rejudge(problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="removeAdmin", help="Removes an admin from a problem")
@click.argument("problem_alias")
@click.argument("username_or_email")
def remove_admin(problem_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.problem.removeAdmin(
        problem_alias=problem_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="removeGroupAdmin", help="Removes a group admin from a problem")
@click.argument("group")
@click.argument("problem_alias")
def remove_group_admin(group, problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.removeGroupAdmin(group=group, problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="removeTag", help="Removes a tag from a contest")
@click.argument("name")
@click.argument("problem_alias")
def remove_tag(name, problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.removeTag(name=name, problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="runsDiff",
    help="Return a report of which runs would change due to a version change.",
)
@click.argument("version")
@click.option("--problem-alias", default=None, type=str)
def runs_diff(version, problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.runsDiff(version=version, problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="selectVersion", help="Change the version of the problem.")
@click.option("--commit", default=None, type=str)
@click.option("--problem-alias", default=None, type=str)
@click.option("--update-published", default=None, type=str)
def select_version(commit, problem_alias, update_published):
    ctx = get_client()
    api_dict = ctx.problem.selectVersion(
        commit=commit, problem_alias=problem_alias, update_published=update_published
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="solution",
    help="Returns the solution for a problem if conditions are satisfied.",
)
@click.option("--contest-alias", default=None, type=str)
@click.option("--forfeit-problem", default=None, type=bool)
@click.option("--lang", default=None, type=str)
@click.option("--problem-alias", default=None, type=str)
@click.option("--problemset-id", default=None)
@click.option("--statement-type", default=None, type=str)
def solution(
    contest_alias, forfeit_problem, lang, problem_alias, problemset_id, statement_type
):
    ctx = get_client()
    api_dict = ctx.problem.solution(
        contest_alias=contest_alias,
        forfeit_problem=forfeit_problem,
        lang=lang,
        problem_alias=problem_alias,
        problemset_id=problemset_id,
        statement_type=statement_type,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="stats", help="Stats of a problem")
@click.argument("problem_alias")
def stats(problem_alias):
    ctx = get_client()
    api_dict = ctx.problem.stats(problem_alias=problem_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="tags", help="Returns every tag associated to a given problem.")
@click.argument("problem_alias")
@click.option("--include-voted", default=None)
def tags(problem_alias, include_voted):
    ctx = get_client()
    api_dict = ctx.problem.tags(
        problem_alias=problem_alias, include_voted=include_voted
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="update", help="Update problem contents")
@click.argument("message")
@click.argument("problem_alias")
@click.option("--allow-user-add-tags", default=None, type=bool)
@click.option("--email-clarifications", default=None, type=bool)
@click.option("--extra-wall-time", default=None)
@click.option("--group-score-policy", default=None, type=str)
@click.option("--input-limit", default=None)
@click.option("--languages", default=None)
@click.option("--memory-limit", default=None)
@click.option("--output-limit", default=None)
@click.option("--overall-wall-time-limit", default=None)
@click.option("--problem-level", default=None, type=str)
@click.option("--redirect", default=None)
@click.option("--selected-tags", default=None, type=str)
@click.option("--show-diff", default=None, type=str)
@click.option("--source", default=None, type=str)
@click.option("--time-limit", default=None)
@click.option("--title", default=None, type=str)
@click.option("--update-published", default=None, type=str)
@click.option("--validator", default=None, type=str)
@click.option("--validator-time-limit", default=None)
@click.option("--visibility", default=None, type=str)
def update(
    message,
    problem_alias,
    allow_user_add_tags,
    email_clarifications,
    extra_wall_time,
    group_score_policy,
    input_limit,
    languages,
    memory_limit,
    output_limit,
    overall_wall_time_limit,
    problem_level,
    redirect,
    selected_tags,
    show_diff,
    source,
    time_limit,
    title,
    update_published,
    validator,
    validator_time_limit,
    visibility,
):
    ctx = get_client()
    api_dict = ctx.problem.update(
        message=message,
        problem_alias=problem_alias,
        allow_user_add_tags=allow_user_add_tags,
        email_clarifications=email_clarifications,
        extra_wall_time=extra_wall_time,
        group_score_policy=group_score_policy,
        input_limit=input_limit,
        languages=languages,
        memory_limit=memory_limit,
        output_limit=output_limit,
        overall_wall_time_limit=overall_wall_time_limit,
        problem_level=problem_level,
        redirect=redirect,
        selected_tags=selected_tags,
        show_diff=show_diff,
        source=source,
        time_limit=time_limit,
        title=title,
        update_published=update_published,
        validator=validator,
        validator_time_limit=validator_time_limit,
        visibility=visibility,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(
    name="updateProblemLevel", help="Updates the problem level of a problem"
)
@click.argument("problem_alias")
@click.option("--level-tag", default=None, type=str)
def update_problem_level(problem_alias, level_tag):
    ctx = get_client()
    api_dict = ctx.problem.updateProblemLevel(
        problem_alias=problem_alias, level_tag=level_tag
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="updateSolution", help="Updates problem solution only")
@click.argument("message")
@click.argument("problem_alias")
@click.argument("solution")
@click.argument("visibility")
@click.option("--allow-user-add-tags", default=None, type=bool)
@click.option("--email-clarifications", default=None, type=bool)
@click.option("--extra-wall-time", default=None)
@click.option("--group-score-policy", default=None, type=str)
@click.option("--input-limit", default=None)
@click.option("--lang", default=None, type=str)
@click.option("--languages", default=None)
@click.option("--memory-limit", default=None)
@click.option("--output-limit", default=None)
@click.option("--overall-wall-time-limit", default=None)
@click.option("--problem-level", default=None, type=str)
@click.option("--selected-tags", default=None, type=str)
@click.option("--show-diff", default=None, type=str)
@click.option("--source", default=None, type=str)
@click.option("--time-limit", default=None)
@click.option("--title", default=None, type=str)
@click.option("--update-published", default=None, type=str)
@click.option("--validator", default=None, type=str)
@click.option("--validator-time-limit", default=None)
def update_solution(
    message,
    problem_alias,
    solution,
    visibility,
    allow_user_add_tags,
    email_clarifications,
    extra_wall_time,
    group_score_policy,
    input_limit,
    lang,
    languages,
    memory_limit,
    output_limit,
    overall_wall_time_limit,
    problem_level,
    selected_tags,
    show_diff,
    source,
    time_limit,
    title,
    update_published,
    validator,
    validator_time_limit,
):
    ctx = get_client()
    api_dict = ctx.problem.updateSolution(
        message=message,
        problem_alias=problem_alias,
        solution=solution,
        visibility=visibility,
        allow_user_add_tags=allow_user_add_tags,
        email_clarifications=email_clarifications,
        extra_wall_time=extra_wall_time,
        group_score_policy=group_score_policy,
        input_limit=input_limit,
        lang=lang,
        languages=languages,
        memory_limit=memory_limit,
        output_limit=output_limit,
        overall_wall_time_limit=overall_wall_time_limit,
        problem_level=problem_level,
        selected_tags=selected_tags,
        show_diff=show_diff,
        source=source,
        time_limit=time_limit,
        title=title,
        update_published=update_published,
        validator=validator,
        validator_time_limit=validator_time_limit,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="updateStatement", help="Updates problem statement only")
@click.argument("message")
@click.argument("problem_alias")
@click.argument("statement")
@click.argument("visibility")
@click.option("--allow-user-add-tags", default=None, type=bool)
@click.option("--email-clarifications", default=None, type=bool)
@click.option("--extra-wall-time", default=None)
@click.option("--group-score-policy", default=None, type=str)
@click.option("--input-limit", default=None)
@click.option("--lang", default=None)
@click.option("--languages", default=None)
@click.option("--memory-limit", default=None)
@click.option("--output-limit", default=None)
@click.option("--overall-wall-time-limit", default=None)
@click.option("--problem-level", default=None, type=str)
@click.option("--selected-tags", default=None, type=str)
@click.option("--show-diff", default=None, type=str)
@click.option("--source", default=None, type=str)
@click.option("--time-limit", default=None)
@click.option("--title", default=None, type=str)
@click.option("--update-published", default=None, type=str)
@click.option("--validator", default=None, type=str)
@click.option("--validator-time-limit", default=None)
def update_statement(
    message,
    problem_alias,
    statement,
    visibility,
    allow_user_add_tags,
    email_clarifications,
    extra_wall_time,
    group_score_policy,
    input_limit,
    lang,
    languages,
    memory_limit,
    output_limit,
    overall_wall_time_limit,
    problem_level,
    selected_tags,
    show_diff,
    source,
    time_limit,
    title,
    update_published,
    validator,
    validator_time_limit,
):
    ctx = get_client()
    api_dict = ctx.problem.updateStatement(
        message=message,
        problem_alias=problem_alias,
        statement=statement,
        visibility=visibility,
        allow_user_add_tags=allow_user_add_tags,
        email_clarifications=email_clarifications,
        extra_wall_time=extra_wall_time,
        group_score_policy=group_score_policy,
        input_limit=input_limit,
        lang=lang,
        languages=languages,
        memory_limit=memory_limit,
        output_limit=output_limit,
        overall_wall_time_limit=overall_wall_time_limit,
        problem_level=problem_level,
        selected_tags=selected_tags,
        show_diff=show_diff,
        source=source,
        time_limit=time_limit,
        title=title,
        update_published=update_published,
        validator=validator,
        validator_time_limit=validator_time_limit,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problem.command(name="versions", help="Entry point for Problem Versions API")
@click.option("--problem-alias", default=None, type=str)
@click.option("--problemset-id", default=None, type=int)
def versions(problem_alias, problemset_id):
    ctx = get_client()
    api_dict = ctx.problem.versions(
        problem_alias=problem_alias, problemset_id=problemset_id
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="problemForfeited", help="")
def problem_forfeited():
    pass


@problem_forfeited.command(
    name="getCounts",
    help="Returns the number of solutions allowed and the number of solutions already seen",
)
def get_counts():
    ctx = get_client()
    api_dict = ctx.problemForfeited.getCounts()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="problemset", help="")
def problemset():
    pass


@problemset.command(name="details", help="")
@click.argument("assignment")
@click.argument("contest_alias")
@click.argument("course")
@click.argument("problemset_id")
@click.option("--auth-token", default=None)
@click.option("--token", default=None, type=str)
@click.option("--tokens", default=None)
def details(
    assignment, contest_alias, course, problemset_id, auth_token, token, tokens
):
    ctx = get_client()
    api_dict = ctx.problemset.details(
        assignment=assignment,
        contest_alias=contest_alias,
        course=course,
        problemset_id=problemset_id,
        auth_token=auth_token,
        token=token,
        tokens=tokens,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problemset.command(name="scoreboard", help="")
@click.argument("assignment")
@click.argument("contest_alias")
@click.argument("course")
@click.argument("problemset_id")
@click.option("--auth-token", default=None)
@click.option("--token", default=None)
@click.option("--tokens", default=None)
def scoreboard(
    assignment, contest_alias, course, problemset_id, auth_token, token, tokens
):
    ctx = get_client()
    api_dict = ctx.problemset.scoreboard(
        assignment=assignment,
        contest_alias=contest_alias,
        course=course,
        problemset_id=problemset_id,
        auth_token=auth_token,
        token=token,
        tokens=tokens,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@problemset.command(name="scoreboardEvents", help="Returns the Scoreboard events")
@click.argument("assignment")
@click.argument("contest_alias")
@click.argument("course")
@click.argument("problemset_id")
@click.option("--auth-token", default=None)
@click.option("--token", default=None)
@click.option("--tokens", default=None)
def scoreboard_events(
    assignment, contest_alias, course, problemset_id, auth_token, token, tokens
):
    ctx = get_client()
    api_dict = ctx.problemset.scoreboardEvents(
        assignment=assignment,
        contest_alias=contest_alias,
        course=course,
        problemset_id=problemset_id,
        auth_token=auth_token,
        token=token,
        tokens=tokens,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="qualityNomination", help="")
def quality_nomination():
    pass


@quality_nomination.command(
    name="create",
    help="Creates a new QualityNomination  There are three ways in which users can interact with this:  # Suggestion  A user that has already solved a problem can make suggestions about a problem. This expects the `nomination` field to be `suggestion` and the `contents` field should be a JSON blob with at least one the following fields:  * `difficulty`: (Optional) A number in the range [0-4] indicating the difficulty of the problem. * `quality`: (Optional) A number in the range [0-4] indicating the quality of the problem. * `tags`: (Optional) An array of tag names that will be added to the problem upon promotion. * `before_ac`: (Optional) Boolean indicating if the suggestion has been sent before receiving an AC verdict for problem run.  # Quality tag  A reviewer could send this type of nomination to make the user marked as a quality problem or not. The reviewer could also specify which category is the one the problem belongs to. The 'contents' field should have the following subfields:  * tag: The name of the tag corresponding to the category of the problem * quality_seal: A boolean that if activated, means that the problem is a quality problem  # Promotion  A user that has already solved a problem can nominate it to be promoted as a Quality Problem. This expects the `nomination` field to be `promotion` and the `contents` field should be a JSON blob with the following fields:  * `statements`: A dictionary of languages to objects that contain a `markdown` field, which is the markdown-formatted problem statement for that language. * `source`: A URL or string clearly documenting the source or full name of original author of the problem. * `tags`: An array of tag names that will be added to the problem upon promotion.  # Demotion  A demoted problem is banned, and cannot be un-banned or added to any new problemsets. This expects the `nomination` field to be `demotion` and the `contents` field should be a JSON blob with the following fields:  * `rationale`: A small text explaining the rationale for demotion. * `reason`: One of `['duplicate', 'no-problem-statement', 'offensive', 'other', 'spam']`. * `original`: If the `reason` is `duplicate`, the alias of the original problem. # Dismissal A user that has already solved a problem can dismiss suggestions. The `contents` field is empty.",
)
@click.argument("contents")
@click.argument("nomination")
@click.argument("problem_alias")
def create(contents, nomination, problem_alias):
    ctx = get_client()
    api_dict = ctx.qualityNomination.create(
        contents=contents, nomination=nomination, problem_alias=problem_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@quality_nomination.command(
    name="details",
    help="Displays the details of a nomination. The user needs to be either the nominator or a member of the reviewer group.",
)
@click.argument("qualitynomination_id")
def details(qualitynomination_id):
    ctx = get_client()
    api_dict = ctx.qualityNomination.details(qualitynomination_id=qualitynomination_id)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@quality_nomination.command(name="list", help="")
@click.argument("offset")
@click.argument("rowcount")
@click.option("--column", default=None, type=str)
@click.option("--query", default=None, type=str)
@click.option("--status", default=None)
def list_(offset, rowcount, column, query, status):
    ctx = get_client()
    api_dict = ctx.qualityNomination.list(
        offset=offset, rowcount=rowcount, column=column, query=query, status=status
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@quality_nomination.command(
    name="myAssignedList",
    help="Displays the nominations that this user has been assigned.",
)
@click.argument("page")
@click.argument("page_size")
def my_assigned_list(page, page_size):
    ctx = get_client()
    api_dict = ctx.qualityNomination.myAssignedList(page=page, page_size=page_size)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@quality_nomination.command(name="myList", help="")
@click.argument("offset")
@click.argument("rowcount")
def my_list(offset, rowcount):
    ctx = get_client()
    api_dict = ctx.qualityNomination.myList(offset=offset, rowcount=rowcount)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@quality_nomination.command(
    name="resolve",
    help="Marks a problem of a nomination (only the demotion type supported for now) as (resolved, banned, warning).",
)
@click.argument("problem_alias")
@click.argument("qualitynomination_id")
@click.argument("rationale")
@click.argument("status")
@click.option("--all-", default=None, type=bool)
def resolve(problem_alias, qualitynomination_id, rationale, status, all_):
    ctx = get_client()
    api_dict = ctx.qualityNomination.resolve(
        problem_alias=problem_alias,
        qualitynomination_id=qualitynomination_id,
        rationale=rationale,
        status=status,
        all=all_,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="reset", help="")
def reset():
    pass


@reset.command(
    name="create",
    help="Creates a reset operation, the first of two steps needed to reset a password. The first step consist of sending an email to the user with instructions to reset he's password, if and only if the email is valid.",
)
@click.argument("email")
def create(email):
    ctx = get_client()
    api_dict = ctx.reset.create(email=email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@reset.command(
    name="generateToken",
    help="Creates a reset operation, support team members can generate a valid token and then they can send it to end user",
)
@click.argument("email")
def generate_token(email):
    ctx = get_client()
    api_dict = ctx.reset.generateToken(email=email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@reset.command(
    name="update",
    help="Updates the password of a given user, this is the second and last step in order to reset the password. This operation is done if and only if the correct parameters are suplied.",
)
@click.argument("email")
@click.argument("password")
@click.argument("password_confirmation")
@click.argument("reset_token")
def update(email, password, password_confirmation, reset_token):
    ctx = get_client()
    api_dict = ctx.reset.update(
        email=email,
        password=password,
        password_confirmation=password_confirmation,
        reset_token=reset_token,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="run", help="")
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
                print(f"{ok_status} Submission successful.")
            else:
                print(error_status + api_dict["error"])

        if no_follow:
            return

        run_guid = api_dict["guid"]
        api_response = ctx.run.status(run_alias=run_guid)

        if not raw:
            print(f"{info_status} Ongoing evaluation. (Waiting for verdict)")
            print(f"{info_status} Updating", end="", flush=True)

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

                print(f"{info_status} Language:\t{api_response['language']}")
                print(f"{info_status} GUID:\t{api_response['guid']}\n")

                print(f"{info_status} Score:\t{api_response['score'] * 100:.2f} %")
                print(f"{info_status} Memory:\t{api_response['memory'] / 1048576} MiB")
                print(f"{info_status} Runtime: \t{api_response['runtime'] / 1000} s")
            else:
                print(json.dumps(api_response, indent=4, sort_keys=True))
    except FileNotFoundError:
        if not raw:
            print(f"{error_status} File not found, check if the specified path exists.")


@run.command(name="counts", help="Get total of last 6 months")
def counts():
    ctx = get_client()
    api_dict = ctx.run.counts()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@run.command(
    name="details", help="Gets the details of a run. Includes admin details if admin."
)
@click.argument("run_alias")
def details(run_alias):
    ctx = get_client()
    api_dict = ctx.run.details(run_alias=run_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@run.command(name="disqualify", help="Disqualify a submission")
@click.argument("run_alias")
def disqualify(run_alias):
    ctx = get_client()
    api_dict = ctx.run.disqualify(run_alias=run_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@run.command(name="list", help="Gets a list of latest runs overall")
@click.argument("offset")
@click.argument("problem_alias")
@click.argument("rowcount")
@click.argument("username")
@click.option("--language", default=None, type=str)
@click.option("--status", default=None, type=str)
@click.option("--verdict", default=None, type=str)
def list_(offset, problem_alias, rowcount, username, language, status, verdict):
    ctx = get_client()
    api_dict = ctx.run.list(
        offset=offset,
        problem_alias=problem_alias,
        rowcount=rowcount,
        username=username,
        language=language,
        status=status,
        verdict=verdict,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@run.command(name="rejudge", help="Re-sends a problem to Grader.")
@click.argument("run_alias")
@click.option("--debug", default=None)
def rejudge(run_alias, debug):
    ctx = get_client()
    api_dict = ctx.run.rejudge(run_alias=run_alias, debug=debug)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@run.command(name="status", help="Get basic details of a run")
@click.argument("run_alias")
def status(run_alias):
    ctx = get_client()
    api_dict = ctx.run.status(run_alias=run_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="school", help="")
def school():
    pass


@school.command(name="create", help="Api to create new school")
@click.argument("name")
@click.option("--country-id", default=None, type=str)
@click.option("--state-id", default=None, type=str)
def create(name, country_id, state_id):
    ctx = get_client()
    api_dict = ctx.school.create(name=name, country_id=country_id, state_id=state_id)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@school.command(name="list", help="Gets a list of schools")
@click.option("--query", default=None)
@click.option("--term", default=None)
def list_(query, term):
    ctx = get_client()
    api_dict = ctx.school.list(query=query, term=term)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@school.command(
    name="selectSchoolOfTheMonth",
    help="Selects a certain school as school of the month",
)
@click.argument("school_id")
def select_school_of_the_month(school_id):
    ctx = get_client()
    api_dict = ctx.school.selectSchoolOfTheMonth(school_id=school_id)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="scoreboard", help="")
def scoreboard():
    pass


@scoreboard.command(name="refresh", help="Returns a list of contests")
@click.argument("alias")
@click.option("--course-alias", default=None, type=str)
@click.option("--token", default=None)
def refresh(alias, course_alias, token):
    ctx = get_client()
    api_dict = ctx.scoreboard.refresh(
        alias=alias, course_alias=course_alias, token=token
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="session", help="")
def session():
    pass


@session.command(
    name="currentSession",
    help="Returns information about current session. In order to avoid one full server roundtrip (about ~100msec on each pageload), it also returns the current time to be able to calculate the time delta between the contestant's machine and the server.",
)
@click.option("--auth-token", default=None, type=str)
def current_session(auth_token):
    ctx = get_client()
    api_dict = ctx.session.currentSession(auth_token=auth_token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@session.command(name="googleLogin", help="")
@click.argument("store_token")
def google_login(store_token):
    ctx = get_client()
    api_dict = ctx.session.googleLogin(storeToken=store_token)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="submission", help="")
def submission():
    pass


@submission.command(
    name="setFeedback", help="Updates the admin feedback for a submission"
)
@click.argument("assignment_alias")
@click.argument("course_alias")
@click.argument("feedback")
@click.argument("guid")
def set_feedback(assignment_alias, course_alias, feedback, guid):
    ctx = get_client()
    api_dict = ctx.submission.setFeedback(
        assignment_alias=assignment_alias,
        course_alias=course_alias,
        feedback=feedback,
        guid=guid,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="tag", help="")
def tag():
    pass


@tag.command(
    name="frequentTags", help="Return most frequent public tags of a certain level"
)
@click.argument("problem_level")
@click.argument("rows")
def frequent_tags(problem_level, rows):
    ctx = get_client()
    api_dict = ctx.tag.frequentTags(problemLevel=problem_level, rows=rows)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@tag.command(name="list", help="Gets a list of tags")
@click.option("--query", default=None)
@click.option("--term", default=None)
def list_(query, term):
    ctx = get_client()
    api_dict = ctx.tag.list(query=query, term=term)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="teamsGroup", help="")
def teams_group():
    pass


@teams_group.command(name="addMembers", help="Add one or more users to a given team")
@click.argument("team_group_alias")
@click.argument("usernames")
def add_members(team_group_alias, usernames):
    ctx = get_client()
    api_dict = ctx.teamsGroup.addMembers(
        team_group_alias=team_group_alias, usernames=usernames
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(name="create", help="New team group")
@click.argument("alias")
@click.argument("description")
@click.argument("name")
@click.option("--number-of-contestants", default=None, type=int)
def create(alias, description, name, number_of_contestants):
    ctx = get_client()
    api_dict = ctx.teamsGroup.create(
        alias=alias,
        description=description,
        name=name,
        numberOfContestants=number_of_contestants,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(name="details", help="Details of a team group")
@click.argument("team_group_alias")
def details(team_group_alias):
    ctx = get_client()
    api_dict = ctx.teamsGroup.details(team_group_alias=team_group_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(
    name="list",
    help="Gets a list of teams groups. This returns an array instead of an object since it is used by typeahead.",
)
@click.option("--query", default=None, type=str)
def list_(query):
    ctx = get_client()
    api_dict = ctx.teamsGroup.list(query=query)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(
    name="removeMember", help="Remove an existing team member of a teams group"
)
@click.argument("team_group_alias")
@click.argument("username")
def remove_member(team_group_alias, username):
    ctx = get_client()
    api_dict = ctx.teamsGroup.removeMember(
        team_group_alias=team_group_alias, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(name="removeTeam", help="Remove team from teams group")
@click.argument("team_group_alias")
@click.argument("username_or_email")
def remove_team(team_group_alias, username_or_email):
    ctx = get_client()
    api_dict = ctx.teamsGroup.removeTeam(
        team_group_alias=team_group_alias, usernameOrEmail=username_or_email
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(name="teams", help="Teams of a teams group")
@click.argument("team_group_alias")
def teams(team_group_alias):
    ctx = get_client()
    api_dict = ctx.teamsGroup.teams(team_group_alias=team_group_alias)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(
    name="teamsMembers", help="Get a list of team members of a teams group"
)
@click.argument("page")
@click.argument("page_size")
@click.argument("team_group_alias")
def teams_members(page, page_size, team_group_alias):
    ctx = get_client()
    api_dict = ctx.teamsGroup.teamsMembers(
        page=page, page_size=page_size, team_group_alias=team_group_alias
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@teams_group.command(name="update", help="Update an existing teams group")
@click.argument("alias")
@click.argument("description")
@click.argument("name")
@click.option("--number-of-contestants", default=None, type=int)
def update(alias, description, name, number_of_contestants):
    ctx = get_client()
    api_dict = ctx.teamsGroup.update(
        alias=alias,
        description=description,
        name=name,
        numberOfContestants=number_of_contestants,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@main.group(name="user", help="")
def user():
    pass


@user.command(
    name="acceptPrivacyPolicy",
    help="Keeps a record of a user who accepts the privacy policy",
)
@click.argument("privacy_git_object_id")
@click.argument("statement_type")
@click.option("--username", default=None, type=str)
def accept_privacy_policy(privacy_git_object_id, statement_type, username):
    ctx = get_client()
    api_dict = ctx.user.acceptPrivacyPolicy(
        privacy_git_object_id=privacy_git_object_id,
        statement_type=statement_type,
        username=username,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="addExperiment", help="Adds the experiment to the user.")
@click.argument("experiment")
@click.argument("username")
def add_experiment(experiment, username):
    ctx = get_client()
    api_dict = ctx.user.addExperiment(experiment=experiment, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="addGroup", help="Adds the identity to the group.")
@click.argument("group")
def add_group(group):
    ctx = get_client()
    api_dict = ctx.user.addGroup(group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="addRole", help="Adds the role to the user.")
@click.argument("role")
@click.argument("username")
def add_role(role, username):
    ctx = get_client()
    api_dict = ctx.user.addRole(role=role, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="associateIdentity",
    help="Associates an identity to the logged user given the username",
)
@click.argument("password")
@click.argument("username")
def associate_identity(password, username):
    ctx = get_client()
    api_dict = ctx.user.associateIdentity(password=password, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="changePassword", help="Changes the password of a user")
@click.argument("old_password")
@click.argument("username")
@click.option("--password", default=None, type=str)
@click.option("--permission-key", default=None)
def change_password(old_password, username, password, permission_key):
    ctx = get_client()
    api_dict = ctx.user.changePassword(
        old_password=old_password,
        username=username,
        password=password,
        permission_key=permission_key,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="coderOfTheMonth",
    help="Get coder of the month by trying to find it in the table using the first day of the current month. If there's no coder of the month for the given date, calculate it and save it.",
)
@click.option("--category", default=None)
@click.option("--date", default=None, type=str)
def coder_of_the_month(category, date):
    ctx = get_client()
    api_dict = ctx.user.coderOfTheMonth(category=category, date=date)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="coderOfTheMonthList", help="Returns the list of coders of the month"
)
@click.option("--category", default=None)
@click.option("--date", default=None, type=str)
def coder_of_the_month_list(category, date):
    ctx = get_client()
    api_dict = ctx.user.coderOfTheMonthList(category=category, date=date)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="contestStats", help="Get Contests which a certain user has participated in"
)
@click.option("--username", default=None, type=str)
def contest_stats(username):
    ctx = get_client()
    api_dict = ctx.user.contestStats(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="create", help="Entry point for Create a User API")
def create():
    ctx = get_client()
    api_dict = ctx.user.create()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="createAPIToken",
    help="Creates a new API token associated with the user.  This token can be used to authenticate against the API in other calls through the [HTTP `Authorization` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization) in the request:  ``` Authorization: token 92d8c5a0eceef3c05f4149fc04b62bb2cd50d9c6 ```  The following alternative syntax allows to specify an associated identity:  ``` Authorization: token Credential=92d8c5a0eceef3c05f4149fc04b62bb2cd50d9c6,Username=groupname:username ```  There is a limit of 1000 requests that can be done every hour, after which point all requests will fail with [HTTP 429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429). The `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` response headers will be set whenever an API token is used and will contain useful information about the limit to the caller.  There is a limit of 5 API tokens that each user can have.",
)
@click.argument("name")
def create_a_p_i_token(name):
    ctx = get_client()
    api_dict = ctx.user.createAPIToken(name=name)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="extraInformation",
    help="Gets extra information of the identity: - last password change request - verify status - birth date to verify the user identity",
)
@click.argument("email")
def extra_information(email):
    ctx = get_client()
    api_dict = ctx.user.extraInformation(email=email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="generateGitToken",
    help="Generate a new gitserver token. This token can be used to authenticate against the gitserver.",
)
def generate_git_token():
    ctx = get_client()
    api_dict = ctx.user.generateGitToken()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="generateOmiUsers", help="")
@click.argument("auth_token")
@click.argument("contest_alias")
@click.argument("contest_type")
@click.argument("id_")
@click.argument("old_password")
@click.argument("permission_key")
@click.argument("username")
@click.option("--change-password", default=None)
@click.option("--password", default=None, type=str)
@click.option("--username-or-email", default=None, type=str)
def generate_omi_users(
    auth_token,
    contest_alias,
    contest_type,
    id_,
    old_password,
    permission_key,
    username,
    change_password,
    password,
    username_or_email,
):
    ctx = get_client()
    api_dict = ctx.user.generateOmiUsers(
        auth_token=auth_token,
        contest_alias=contest_alias,
        contest_type=contest_type,
        id=id_,
        old_password=old_password,
        permission_key=permission_key,
        username=username,
        change_password=change_password,
        password=password,
        usernameOrEmail=username_or_email,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="lastPrivacyPolicyAccepted",
    help="Gets the last privacy policy accepted by user",
)
@click.option("--username", default=None, type=str)
def last_privacy_policy_accepted(username):
    ctx = get_client()
    api_dict = ctx.user.lastPrivacyPolicyAccepted(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="list", help="Gets a list of users.")
@click.option("--query", default=None, type=str)
@click.option("--rowcount", default=None, type=int)
@click.option("--term", default=None, type=str)
def list_(query, rowcount, term):
    ctx = get_client()
    api_dict = ctx.user.list(query=query, rowcount=rowcount, term=term)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="listAPITokens",
    help="Returns a list of all the API tokens associated with the user.",
)
def list_a_p_i_tokens():
    ctx = get_client()
    api_dict = ctx.user.listAPITokens()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="listAssociatedIdentities",
    help="Get the identities that have been associated to the logged user",
)
def list_associated_identities():
    ctx = get_client()
    api_dict = ctx.user.listAssociatedIdentities()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="listUnsolvedProblems", help="Get Problems unsolved by user")
@click.option("--username", default=None, type=str)
def list_unsolved_problems(username):
    ctx = get_client()
    api_dict = ctx.user.listUnsolvedProblems(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="login", help="Exposes API /user/login Expects in request: user password"
)
@click.argument("password")
@click.argument("username_or_email")
def login(password, username_or_email):
    ctx = get_client()
    api_dict = ctx.user.login(password=password, usernameOrEmail=username_or_email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="mailingListBackfill",
    help="Registers to the mailing list all users that have not been added before. Admin only",
)
def mailing_list_backfill():
    ctx = get_client()
    api_dict = ctx.user.mailingListBackfill()
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="problemsCreated", help="Get Problems created by user")
@click.option("--username", default=None, type=str)
def problems_created(username):
    ctx = get_client()
    api_dict = ctx.user.problemsCreated(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="problemsSolved", help="Get Problems solved by user")
@click.option("--username", default=None, type=str)
def problems_solved(username):
    ctx = get_client()
    api_dict = ctx.user.problemsSolved(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="profile", help="Get general user info")
@click.option("--category", default=None)
@click.option("--omit-rank", default=None, type=bool)
@click.option("--username", default=None, type=str)
def profile(category, omit_rank, username):
    ctx = get_client()
    api_dict = ctx.user.profile(
        category=category, omit_rank=omit_rank, username=username
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="removeExperiment", help="Removes the experiment from the user.")
@click.argument("experiment")
@click.argument("username")
def remove_experiment(experiment, username):
    ctx = get_client()
    api_dict = ctx.user.removeExperiment(experiment=experiment, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="removeGroup", help="Removes the user to the group.")
@click.argument("group")
def remove_group(group):
    ctx = get_client()
    api_dict = ctx.user.removeGroup(group=group)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="removeRole", help="Removes the role from the user.")
@click.argument("role")
@click.argument("username")
def remove_role(role, username):
    ctx = get_client()
    api_dict = ctx.user.removeRole(role=role, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="revokeAPIToken", help="Revokes an API token associated with the user."
)
@click.argument("name")
def revoke_a_p_i_token(name):
    ctx = get_client()
    api_dict = ctx.user.revokeAPIToken(name=name)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="selectCoderOfTheMonth", help="Selects coder of the month for next month."
)
@click.argument("username")
@click.option("--category", default=None)
def select_coder_of_the_month(username, category):
    ctx = get_client()
    api_dict = ctx.user.selectCoderOfTheMonth(username=username, category=category)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="stats", help="Get stats")
@click.option("--username", default=None, type=str)
def stats(username):
    ctx = get_client()
    api_dict = ctx.user.stats(username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="statusVerified", help="Gets verify status of a user")
@click.argument("email")
def status_verified(email):
    ctx = get_client()
    api_dict = ctx.user.statusVerified(email=email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="update", help="Update user profile")
@click.argument("birth_date")
@click.argument("country_id")
@click.argument("graduation_date")
@click.argument("locale")
@click.argument("state_id")
@click.option("--auth-token", default=None)
@click.option("--gender", default=None, type=str)
@click.option("--has-competitive-objective", default=None, type=bool)
@click.option("--has-learning-objective", default=None, type=bool)
@click.option("--has-scholar-objective", default=None, type=bool)
@click.option("--has-teaching-objective", default=None, type=bool)
@click.option("--hide-problem-tags", default=None, type=bool)
@click.option("--is-private", default=None, type=bool)
@click.option("--name", default=None, type=str)
@click.option("--scholar-degree", default=None, type=str)
@click.option("--school-id", default=None, type=int)
@click.option("--school-name", default=None)
@click.option("--username", default=None)
def update(
    birth_date,
    country_id,
    graduation_date,
    locale,
    state_id,
    auth_token,
    gender,
    has_competitive_objective,
    has_learning_objective,
    has_scholar_objective,
    has_teaching_objective,
    hide_problem_tags,
    is_private,
    name,
    scholar_degree,
    school_id,
    school_name,
    username,
):
    ctx = get_client()
    api_dict = ctx.user.update(
        birth_date=birth_date,
        country_id=country_id,
        graduation_date=graduation_date,
        locale=locale,
        state_id=state_id,
        auth_token=auth_token,
        gender=gender,
        has_competitive_objective=has_competitive_objective,
        has_learning_objective=has_learning_objective,
        has_scholar_objective=has_scholar_objective,
        has_teaching_objective=has_teaching_objective,
        hide_problem_tags=hide_problem_tags,
        is_private=is_private,
        name=name,
        scholar_degree=scholar_degree,
        school_id=school_id,
        school_name=school_name,
        username=username,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="updateBasicInfo",
    help="Update basic user profile info when logged with fb/gool",
)
@click.argument("password")
@click.argument("username")
def update_basic_info(password, username):
    ctx = get_client()
    api_dict = ctx.user.updateBasicInfo(password=password, username=username)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="updateMainEmail", help="Updates the main email of the current user")
@click.argument("email")
@click.option("--original-email", default=None, type=str)
def update_main_email(email, original_email):
    ctx = get_client()
    api_dict = ctx.user.updateMainEmail(email=email, originalEmail=original_email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(
    name="validateFilter",
    help="Parses and validates a filter string to be used for event notification filtering.  The Request must have a 'filter' key with comma-delimited URI paths representing the resources the caller is interested in receiving events for. If the caller has enough privileges to receive notifications for ALL the requested filters, the request will return successfully, otherwise an exception will be thrown.  This API does not need authentication to be used. This allows to track contest updates with an access token.",
)
@click.argument("filter_")
@click.argument("problemset_id")
@click.option("--auth-token", default=None, type=str)
@click.option("--contest-admin", default=None, type=str)
@click.option("--contest-alias", default=None, type=str)
@click.option("--token", default=None, type=str)
@click.option("--tokens", default=None)
def validate_filter(
    filter_, problemset_id, auth_token, contest_admin, contest_alias, token, tokens
):
    ctx = get_client()
    api_dict = ctx.user.validateFilter(
        filter=filter_,
        problemset_id=problemset_id,
        auth_token=auth_token,
        contest_admin=contest_admin,
        contest_alias=contest_alias,
        token=token,
        tokens=tokens,
    )
    print(json.dumps(api_dict, indent=4, sort_keys=True))


@user.command(name="verifyEmail", help="Verifies the user given its verification id")
@click.argument("id_")
@click.option("--username-or-email", default=None, type=str)
def verify_email(id_, username_or_email):
    ctx = get_client()
    api_dict = ctx.user.verifyEmail(id=id_, usernameOrEmail=username_or_email)
    print(json.dumps(api_dict, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
