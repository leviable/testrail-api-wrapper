class ENVs(object):
    """ OS Envionment variable names """
    USER_KEY = 'TRAW_USERNAME'
    API_KEY = 'TRAW_USER_API_KEY'
    PASS_KEY = 'TRAW_PASSWORD'
    URL_KEY = 'TRAW_URL'


API_PATH = {
    'add_case': 'add_case/{seciont_id}',
    'add_config': 'add_config/{config_group_id}',
    'add_config_group': 'add_config_group/{project_id}',
    'add_milestone': 'add_milestone/{project_id}',
    'add_plan': 'add_plan/{project_id}',
    'add_plan_entry': 'add_plan_entry/{plan_id}',
    'add_project': 'add_project',
    'add_result': 'add_result/{test_id}',
    'add_result_for_case': 'add_result_for_case/{run_id}/{case_id}',
    'add_results': 'add_results/{run_id}',
    'add_results_for_cases': 'add_results_for_cases/{run_id}',
    'add_run': 'add_run/{project_id}',
    'add_section': 'add_section/{project_id}',
    'add_suite': 'add_suite/{project_id}',
    'close_plan': 'close_plan/{plan_id}',
    'close_run': 'close_run/{run_id}',
    'delete_case': 'delete_case/{case_id}',
    'delete_config': 'delete_config/{config_id}',
    'delete_config_group': 'delete_config_group/{config_group_id}',
    'delete_milestone': 'delete_milestone/{milestone_id}',
    'delete_plan': 'delete_plan/{plan_id}',
    'delete_plan_entry': 'delete_plan_entry/{plan_id}/{entry_id}',
    'delete_project': 'delete_project/{project_id}',
    'delete_run': 'delete_run/{run_id}',
    'delete_section': 'delete_section/{section_id}',
    'delete_suite': 'delete_suite/{suite_id}',
    'get_case': 'get_case/{case_id}',
    'get_cases': 'get_cases/{project_id}',
    'get_case_fields': 'get_case_fields',
    'get_case_types': 'get_case_types',
    'get_configs': 'get_configs/{project_id}',
    'get_milestone': 'get_milestone/{milestone_id}',
    'get_milestones': 'get_milestones/{project_id}',
    'get_plan': 'get_plan/{plan_id}',
    'get_plans': 'get_plans/{project_id}',
    'get_priorities': 'get_priorities',
    'get_project': 'get_project/{project_id}',
    'get_projects': 'get_projects',
    'get_results': 'get_results/{test_id}',
    'get_results_for_case': 'get_results_for_case/{run_id}/{case_id}',
    'get_results_for_run': 'get_results_for_run/{run_id}',
    'get_result_fields': 'get_result_fields',
    'get_run': 'get_run/{run_id}',
    'get_runs': 'get_runs/{project_id}',
    'get_section': 'get_section/{section_id}',
    'get_sections': 'get_sections/{project_id}',  # suite_id may be optional
    'get_statuses': 'get_statuses',
    'get_suite': 'get_suite/{suite_id}',
    'get_suites': 'get_suites/{project_id}',
    'get_templates': 'get_templates/{project_id}',
    'get_test': 'get_test/{test_id}',
    'get_tests': 'get_tests/{run_id}',
    'get_user': 'get_user/{user_id}',
    'get_user_by_email': 'get_user_by_email',
    'get_users': 'get_users',
    'update_case': 'update_case/{case_id}',
    'update_config': 'update_config/{config_id}',
    'update_config_group': 'update_config_group/{config_group_id}',
    'update_milestone': 'update_milestone/{milestone_id}',
    'update_plan': 'update_plan/{plan_id}',
    'update_plan_entry': 'update_plan_entry/{plan_id}/{entry_id}',
    'update_project': 'update_project/{project_id}',
    'update_run': 'update_run/{run_id}',
    'update_section': 'update_section/{section_id}',
    'update_suite': 'update_suite/{suite_id}',
}

BASE_API_PATH = '/index.php?/api/v2'

CONFIG_FILE_NAME = '.traw_config'

DEFAULT_CACHE_TIMEOUT = 300  # Seconds

DEFAULT_LIMIT = 250

GET = 'get'
POST = 'post'

# Session retry parameters
DELAY = 1
RETRIES = 3

# Exception messages
NOTIMP = "Not implemented directly. You must pass in {0} object"
SETTER_ERR = 'Expected {0}, found {1}'

TIMEOUT = 16  # TODO: Make this configurable

# POST param names
ANNOUNCEMENT = 'announcement'
ASSIGNEDTO_ID = 'assignedto_id'
CASE_IDS = 'case_ids'
COMMENT = 'comment'
DEFECTS = 'defects'
DESCRIPTION = 'description'
DUE_ON = 'due_on'
ELAPSED = 'elapsed'
ESTIMATE = 'estimate'
ID = 'id'
INCLUDE_ALL = 'include_all'
IS_COMPLETED = 'is_completed'
IS_STARTED = 'is_started'
MILESTONE_ID = 'milestone_id'
NAME = 'name'
PARENT_ID = 'parent_id'
PRIORITY_ID = 'priority_id'
PROJECT_ID = 'project_id'
REFS = 'refs'
SHOW_ANNOUNCEMENT = 'show_announcement'
STATUS_ID = 'status_id'
SUITE_ID = 'suite_id'
SUITE_MODE = 'suite_mode'
START_ON = 'start_on'
TEMPLATE_ID = 'template_id'
TEST_ID = 'test_id'
TYPE_ID = 'type_id'
TITLE = 'title'
VERSION = 'version'

# Add/Delete/Update fields by object
CASE_ADD_FIELDS = (TITLE, TEMPLATE_ID, TYPE_ID, PRIORITY_ID, ESTIMATE,
                   MILESTONE_ID, REFS)
CASE_UPDATE_FIELDS = CASE_ADD_FIELDS
CONFIG_ADD_FIELDS = (NAME, )
CONFIG_UPDATE_FIELDS = CONFIG_ADD_FIELDS
CONFIG_GROUP_ADD_FIELDS = (NAME, )
CONFIG_GROUP_UPDATE_FIELDS = CONFIG_GROUP_ADD_FIELDS
MILESTONE_ADD_FIELDS = (NAME, DESCRIPTION, DUE_ON, PARENT_ID, START_ON)
# TODO: find out why `is_started` doesn't work, and add it back in
MILESTONE_UPDATE_FIELDS = MILESTONE_ADD_FIELDS + (IS_COMPLETED, IS_STARTED, START_ON)
PROJECT_ADD_FIELDS = (NAME, ANNOUNCEMENT, SHOW_ANNOUNCEMENT, SUITE_MODE)
PROJECT_UPDATE_FIELDS = PROJECT_ADD_FIELDS + (IS_COMPLETED, )
RESULT_ADD_FIELDS = (ASSIGNEDTO_ID, COMMENT, DEFECTS, ELAPSED, STATUS_ID, VERSION)
RUN_UPDATE_FIELDS = (NAME, DESCRIPTION, INCLUDE_ALL, CASE_IDS, MILESTONE_ID)
RUN_ADD_FIELDS = RUN_UPDATE_FIELDS + (SUITE_ID, ASSIGNEDTO_ID)
SECTION_ADD_FIELDS = (NAME, DESCRIPTION, PARENT_ID, SUITE_ID)
SECTION_UPDATE_FIELDS = (NAME, DESCRIPTION)
SUITE_ADD_FIELDS = (NAME, DESCRIPTION)
SUITE_UPDATE_FIELDS = SUITE_ADD_FIELDS
