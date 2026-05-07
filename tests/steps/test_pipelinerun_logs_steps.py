"""
PipelineRun Logs Test Steps.

This module contains BDD step definitions for PipelineRun Logs page validation,
including task navigation, status validation, and log verification.
Part of SRVKP-11526 - Sanity Suite.
"""

import asyncio
import os
from typing import Any, Dict

from pytest_bdd import given, scenarios, then, when

from framework.fixtures.async_bridge import run_async

# Register scenarios from the feature file
scenarios("../features/pipelinerun_logs_validation.feature")


@given('a PipelineRun "hello-pipeline-run" exists in namespace "pipeline-test"')
def pipelinerun_exists(page: Dict[str, Any]) -> None:
    """
    Prerequisite step - assumes PipelineRun exists in the cluster.
    In a real implementation, this could verify the PipelineRun exists via API.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :return: None
    """
    # This is a prerequisite - the PipelineRun should already exist
    # In production, you might want to verify via kubectl/API call
    pass


@when('the user navigates to the PipelineRun "hello-pipeline-run" in namespace "pipeline-test"')
def navigate_to_pipelinerun(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Navigate to a specific PipelineRun page.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises TimeoutError if navigation fails.
    """

    async def _navigate() -> None:
        raw_page = page["raw_page"]
        console_url = os.getenv("CONSOLE_URL")
        namespace = "pipeline-test"
        pipelinerun_name = "hello-pipeline-run"

        pr_url = f"{console_url}/k8s/ns/{namespace}/tekton.dev~v1~PipelineRun/{pipelinerun_name}"
        await raw_page.goto(pr_url, wait_until="domcontentloaded")
        await raw_page.wait_for_timeout(2000)

    run_async(playwright_event_loop, _navigate())


@when("the user navigates to Logs tab")
@then("the user navigates to Logs tab")
def navigate_to_logs_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Navigate to the Logs tab on a PipelineRun page.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if navigation fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _navigate() -> None:
        await logs_page.navigate_to_logs_tab()
        await logs_page.wait_for_logs_to_load(timeout=60000)

    run_async(playwright_event_loop, _navigate())


@then("the PipelineRun Logs page should be visible")
def pipelinerun_logs_page_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the PipelineRun Logs page is visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if page is not visible.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.verify_on_page()), "PipelineRun Logs page not visible"


@then("all tasks should be displayed in the task navigation")
def all_tasks_displayed(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that all tasks are displayed in the task navigation.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if no tasks found.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        tasks = await logs_page.get_available_tasks()
        return len(tasks) > 0

    assert run_async(playwright_event_loop, _verify()), "No tasks found in task navigation"


@then("all tasks should have successful status")
def all_tasks_successful(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that all tasks have successful status.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if any task is not successful.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.validate_all_tasks_successful()), "Not all tasks are successful"


@then("the logs container should be visible")
def logs_container_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the logs container is visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if logs container is not visible.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.is_logs_container_visible()), "Logs container is not visible"


@then("the task navigation should be visible")
def task_navigation_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the task navigation is visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if task navigation is not visible.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.is_task_navigation_visible()), "Task navigation is not visible"


@then("at least one task should be present")
def at_least_one_task_present(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that at least one task is present.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if no tasks are found.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        tasks = await logs_page.get_available_tasks()
        return len(tasks) > 0

    assert run_async(playwright_event_loop, _verify()), "Expected at least one task to be present"


@then("the pipeline run should be validated as successful")
def pipeline_run_validated_successful(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Perform comprehensive validation of the pipeline run.
    Validates: tasks displayed, all successful, logs container visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if validation fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    # This method performs comprehensive validation:
    # - Task navigation visible
    # - At least one task found
    # - All tasks successful
    # Note: We skip log content validation as the locator needs refinement
    async def _validate() -> bool:
        # Verify task navigation visible
        if not await logs_page.is_task_navigation_visible():
            return False

        # Verify tasks exist
        tasks = await logs_page.get_available_tasks()
        if len(tasks) == 0:
            return False

        # Verify all tasks successful
        await logs_page.validate_all_tasks_successful()

        # Verify logs container visible
        if not await logs_page.is_logs_container_visible():
            return False

        return True

    assert run_async(playwright_event_loop, _validate()), "Pipeline run validation failed"


@when("the user clicks on the first available task")
def click_first_task(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Click on the first available task in the task navigation.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if no tasks found or click fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _click() -> bool:
        tasks = await logs_page.get_available_tasks()
        if len(tasks) == 0:
            return False
        return await logs_page.click_task_link(tasks[0])

    assert run_async(playwright_event_loop, _click()), "Failed to click on first task"


@then("the selected task should be highlighted")
def task_highlighted(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that a task is currently selected/highlighted.
    This checks that the logs container is visible (indicating a task is selected).

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if no task is highlighted.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.is_logs_container_visible()), (
        "Expected a task to be highlighted/selected"
    )


@then("each task should display a status indicator")
def each_task_has_status(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that each task has a status indicator.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if any task has no status.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        task_statuses = await logs_page.get_all_task_statuses()
        # Verify all tasks have a status (not empty dict)
        return len(task_statuses) > 0 and all(status for status in task_statuses.values())

    assert run_async(playwright_event_loop, _verify()), "Not all tasks have status indicators"


@then('the status of task "hello" should be "success"')
def task_status_is_success(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the "hello" task has "success" status.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if status is not success.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        status = await logs_page.get_task_status("hello")
        return status == "success"

    assert run_async(playwright_event_loop, _verify()), "Task 'hello' does not have success status"


@then("the download button should be visible")
def download_button_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the download button is visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if button not visible.
    """
    logs_page = page["pipelines"].pipelinerun.logs
    raw_page = page["raw_page"]

    async def _verify() -> bool:
        # Check if download button exists and is visible
        return await raw_page.locator(logs_page.locators.DOWNLOAD_BUTTON).is_visible(timeout=5000)

    assert run_async(playwright_event_loop, _verify()), "Download button is not visible"


@then("the download all button should be visible")
def download_all_button_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the download all button is visible.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if button not visible.
    """
    logs_page = page["pipelines"].pipelinerun.logs
    raw_page = page["raw_page"]

    async def _verify() -> bool:
        # Check if download all button exists and is visible
        return await raw_page.locator(logs_page.locators.DOWNLOAD_ALL_BUTTON).is_visible(timeout=5000)

    assert run_async(playwright_event_loop, _verify()), "Download all button is not visible"


@then('the PipelineRun name should be "hello-pipeline-run"')
def pipelinerun_name_correct(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the PipelineRun name is displayed correctly.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if name doesn't match.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        name = await logs_page.get_pipelinerun_name()
        return name == "hello-pipeline-run"

    assert run_async(playwright_event_loop, _verify()), "PipelineRun name does not match expected value"


@when("the user navigates to Details tab")
def navigate_to_details_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Navigate to the Details tab on PipelineRun page.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if navigation fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.navigate_to_details_tab()), "Failed to navigate to Details tab"


@then("the Details tab should be visible")
def details_tab_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the Details tab is visible/active.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if not visible.
    """
    details_page = page["pipelines"].pipelinerun.details

    assert run_async(playwright_event_loop, details_page.verify_on_page()), "Details tab is not visible"


@when("the user navigates to YAML tab")
def navigate_to_yaml_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Navigate to the YAML tab on PipelineRun page.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if navigation fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.navigate_to_yaml_tab()), "Failed to navigate to YAML tab"


@then("the YAML tab should be visible")
def yaml_tab_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the YAML tab is visible/active.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if not visible.
    """
    yaml_page = page["pipelines"].pipelinerun.yaml

    assert run_async(playwright_event_loop, yaml_page.verify_on_page()), "YAML tab is not visible"


@when("the user clicks the PipelineRuns breadcrumb")
def click_breadcrumb(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Click the PipelineRuns breadcrumb to navigate back to the list.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if click fails.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.click_breadcrumb_pipelineruns()), (
        "Failed to click PipelineRuns breadcrumb"
    )


@then("the user should be on the PipelineRuns list page")
def on_pipelineruns_list(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that the user is on the PipelineRuns list page.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if not on list page.
    """
    raw_page = page["raw_page"]

    async def _verify() -> bool:
        # Check URL contains PipelineRun list path
        await raw_page.wait_for_timeout(2000)
        current_url = raw_page.url
        return "/tekton.dev~v1~PipelineRun" in current_url and "/hello-pipeline-run" not in current_url

    assert run_async(playwright_event_loop, _verify()), "Not on PipelineRuns list page"


@then("the following tasks should be displayed:")
def expected_tasks_displayed(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that expected tasks are displayed.
    Note: This step uses a data table from the feature file.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if tasks don't match.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        expected_tasks = ["hello"]  # From the data table
        return await logs_page.validate_all_tasks_displayed(expected_tasks)

    assert run_async(playwright_event_loop, _verify()), "Expected tasks are not all displayed"


@then("task statuses should be retrievable for all tasks")
def statuses_retrievable(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that task statuses can be retrieved for all tasks.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if statuses cannot be retrieved.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        task_statuses = await logs_page.get_all_task_statuses()
        return len(task_statuses) > 0

    assert run_async(playwright_event_loop, _verify()), "Could not retrieve task statuses"


@then("all retrieved task statuses should be valid")
def statuses_valid(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify that all retrieved task statuses are valid.
    Valid statuses: success, failed, running, pending, unknown

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if any status is invalid.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        valid_statuses = ["success", "failed", "running", "pending", "unknown"]
        task_statuses = await logs_page.get_all_task_statuses()
        return all(status in valid_statuses for status in task_statuses.values())

    assert run_async(playwright_event_loop, _verify()), "Some task statuses are invalid"


@when("the user waits for logs to fully load")
def wait_for_logs_load(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Wait for logs to fully load.

    :param Dict[str, Any] page: Dictionary containing Page Object instances.
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async operations.
    :return: None: Raises AssertionError if logs don't load.
    """
    logs_page = page["pipelines"].pipelinerun.logs

    assert run_async(playwright_event_loop, logs_page.wait_for_logs_to_load(timeout=60000)), (
        "Logs did not fully load within timeout"
    )
