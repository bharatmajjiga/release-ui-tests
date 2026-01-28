from typing import Any, Dict

from pytest_bdd import given, parsers, then, when


@given("the user is on the OpenShift login page")
def user_on_login_page(page: Dict[str, Any]) -> None:
    """
    step for navigating to and verifying the OpenShift login page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation or verification fails.
    """
    assert page["login"].goto() and page["login"].verify_successful_navigation_to_login_page()


@when(parsers.parse("user chooses to login with {auth_type}"))
def user_to_chose_login_auth_type(page: Dict[str, Any], auth_type: str) -> None:
    """
    step for choosing the authentication type.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :param str auth_type: the type of authentication user chosen for login
    :return: None: Raises AssertionError if login verification fails, TimeoutError if operations timeout.
    """
    page["login"].choose_login_auth_type(auth_type)


@when("the user logs in with valid credentials")
def user_logs_in(page: Dict[str, Any]) -> None:
    """
    step for performing login with valid credentials.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises AssertionError if login verification fails, TimeoutError if operations timeout.
    """
    page["login"].login()
    # Verify login by checking Overview page is displayed
    page["overview"].verify_on_page()


@when("Validate Pipelines button is visible in the left navigation bar")
@then("Validate Pipelines button is visible in the left navigation bar")
def validate_pipelines_button_visible(page: Dict[str, Any]) -> None:
    """
    step for validating that the Pipelines button is visible in the left navigation bar.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises AssertionError if Pipelines button is not visible, TimeoutError if operations timeout.
    """
    assert page["nav"].verify_pipelines_button_visible(), "Pipelines button is not visible in left navigation bar."


@when("the user clicks on Pipelines button")
def user_navigates_to_pipelines_section(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Pipelines section.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation elements are not clickable within the timeout.
    """
    assert page["nav"].click_pipelines_button()


@when("the user navigates to the Pipelines page")
@then("the user navigates to the Pipelines page")
def user_navigates_to_pipelines(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Pipelines page and verifying successful navigation.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation elements are not clickable within the timeout.
    Raises AssertionError if navigation verification fails.
    """
    assert page["nav"].navigate_to_pipelines(), "Failed to navigate to Pipelines page."
    assert page["pipelines"].verify_on_page(), "Pipelines page verification failed."
    assert page["pipelines"].verify_data_load(tab_name="Pipelines tab")


@when("the user navigates to Pipelines tab")
@then("the user navigates to Pipelines tab")
def user_navigates_to_pipelines_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Pipelines tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["pipelines"].navigate_to_pipelines_tab(), "Failed to navigate to Pipelines tab."
    assert page["pipelines"].verify_data_load(tab_name="Pipelines tab")


@when("the user navigates to PipelineRuns tab")
@then("the user navigates to PipelineRuns tab")
def user_navigates_to_pipeline_runs_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the PipelineRuns tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["pipelines"].navigate_to_pipeline_runs_tab(), "Failed to navigate to PipelineRuns tab."
    assert page["pipelines"].verify_data_load(tab_name="PipelineRuns tab")


@when("the user navigates to Repositories tab")
@then("the user navigates to Repositories tab")
def user_navigates_to_repositories_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Repositories tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["pipelines"].navigate_to_repositories_tab(), "Failed to navigate to Repositories tab."
    assert page["pipelines"].verify_data_load(tab_name="Repositories tab")


@then(parsers.parse("Verify the following {links} are available under Pipelines button"))
def verify_links_available_under_pipelines_button(page: Dict[str, Any], links: str) -> None:
    """
    step for verifying that a specific link is available under the Pipelines button in the left navigation bar.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :param str links: The name of the link to verify (e.g., "Overview", "Pipelines", "Tasks", "Triggers").
    :return: None: Raises AssertionError if the link is not visible or if an invalid link name is provided.
    """
    assert page["nav"].verify_link_available_under_pipelines_button(links), (
        f"Link '{links}' is not available under Pipelines button."
    )


@when("the user navigates to the Overview page")
@then("the user navigates to the Overview page")
def user_navigates_to_overview(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Pipelines Overview page and verifying successful navigation.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation elements are not clickable within the timeout.
    Raises AssertionError if navigation verification fails.
    """
    assert page["nav"].navigate_to_overview(), "Failed to navigate to Overview page."
    assert page["pipelines_overview"].verify_on_page(), "Pipelines Overview page verification failed."


@when("the user navigates to the Tasks page")
@then("the user navigates to the Tasks page")
def user_navigates_to_tasks(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Tasks page and verifying successful navigation.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation elements are not clickable within the timeout.
    Raises AssertionError if navigation verification fails.
    """
    assert page["nav"].navigate_to_tasks(), "Failed to navigate to Tasks page."
    assert page["tasks"].verify_on_page(), "Tasks page verification failed."
    assert page["tasks"].verify_data_load(tab_name="Tasks tab")


@when("the user navigates to Tasks tab")
@then("the user navigates to Tasks tab")
def user_navigates_to_tasks_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Tasks tab on the Tasks page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["tasks"].navigate_to_tasks_tab(), "Failed to navigate to Tasks tab."
    assert page["tasks"].verify_data_load(tab_name="Tasks tab")


@when("the user navigates to TaskRuns tab")
@then("the user navigates to TaskRuns tab")
def user_navigates_to_task_runs_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the TaskRuns tab on the Tasks page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["tasks"].navigate_to_task_runs_tab(), "Failed to navigate to TaskRuns tab."
    assert page["tasks"].verify_data_load(tab_name="TaskRuns tab")


@when("the user navigates to the Triggers page")
@then("the user navigates to the Triggers page")
def user_navigates_to_triggers(page: Dict[str, Any]) -> None:
    """
    step for navigating to the Triggers page and verifying successful navigation.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation elements are not clickable within the timeout.
    Raises AssertionError if navigation verification fails.
    """
    assert page["nav"].navigate_to_triggers(), "Failed to navigate to Triggers page."
    assert page["triggers"].verify_on_page(), "Triggers page verification failed."
    assert page["triggers"].verify_data_load(tab_name="Triggers tab")


@when("the user navigates to EventListeners tab")
@then("the user navigates to EventListeners tab")
def user_navigates_to_event_listeners_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the EventListeners tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["triggers"].navigate_to_event_listeners_tab(), "Failed to navigate to EventListeners tab."
    assert page["triggers"].verify_data_load(tab_name="EventListeners tab")


@when("the user navigates to TriggerTemplates tab")
@then("the user navigates to TriggerTemplates tab")
def user_navigates_to_trigger_templates_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the TriggerTemplates tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["triggers"].navigate_to_trigger_templates_tab(), "Failed to navigate to TriggerTemplates tab."
    assert page["triggers"].verify_data_load(tab_name="TriggerTemplates tab")


@when("the user navigates to TriggerBindings tab")
@then("the user navigates to TriggerBindings tab")
def user_navigates_to_trigger_bindings_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the TriggerBindings tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["triggers"].navigate_to_trigger_bindings_tab(), "Failed to navigate to TriggerBindings tab."
    assert page["triggers"].verify_data_load(tab_name="TriggerBindings tab")


@when("the user navigates to ClusterTriggerBindings tab")
@then("the user navigates to ClusterTriggerBindings tab")
def user_navigates_to_cluster_trigger_templates_tab(page: Dict[str, Any]) -> None:
    """
    step for navigating to the ClusterTriggerBindings tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert page["triggers"].navigate_to_cluster_trigger_bindings_tab(), (
        "Failed to navigate to ClusterTriggerBindings tab."
    )
    assert page["triggers"].verify_data_load(tab_name="ClusterTriggerBindings tab")
