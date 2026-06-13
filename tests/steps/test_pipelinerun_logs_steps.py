"""
PipelineRun Logs Test Steps.

This module contains BDD step definitions for PipelineRun Logs page validation and CRUD operations.

Step definitions are reused across two feature files:
- pipelinerun_logs_validation.feature: UI validation (page elements, navigation, task interactions)
- pipelinerun_logs_crud_operations.feature: CRUD operations with log content verification
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import parsers, scenarios, then, when

from framework.fixtures.async_bridge import run_async

# Register scenarios from both feature files
scenarios("../features/pipelinerun_logs_validation.feature")
scenarios("../features/pipelinerun_logs_crud_operations.feature")


@when("the user navigates to Logs tab")
@then("the user navigates to Logs tab")
def navigate_to_logs_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Navigate to the PipelineRun Logs tab and wait for logs to load.

    Clicks the Logs tab and waits for the log content area to be ready for interaction.
    Uses extended timeout to accommodate log streaming.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises TimeoutError if logs fail to load
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _navigate() -> None:
        await logs_page.navigate_to_logs_tab()
        await logs_page.wait_for_logs_to_load(timeout=60000)

    run_async(playwright_event_loop, _navigate())


@then("the PipelineRun Logs page should be visible")
def pipelinerun_logs_page_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify the PipelineRun Logs page is currently displayed.

    Validates page presence by checking URL pattern matches logs tab route.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if logs page is not visible
    """
    assert run_async(playwright_event_loop, page["pipelines"].pipelinerun.logs.verify_on_page()), (
        "PipelineRun Logs page not visible"
    )


@then("all tasks should be displayed in the task navigation")
def all_tasks_displayed(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify all pipeline tasks appear in the navigation sidebar.

    Checks that at least one task is present in the task navigation list.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if no tasks are found
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        tasks = await logs_page.get_available_tasks()
        return len(tasks) > 0

    assert run_async(playwright_event_loop, _verify()), "No tasks found in task navigation"


@then("all tasks should have successful status")
def all_tasks_successful(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify all tasks completed with success status.

    Checks each task's status indicator to confirm successful execution.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if any task has non-success status
    """
    assert run_async(playwright_event_loop, page["pipelines"].pipelinerun.logs.validate_all_tasks_successful()), (
        "Not all tasks are successful"
    )


@then("the logs container should be visible")
def logs_container_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify the main logs content area is displayed.

    Validates that the logs container element is visible on the page.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if logs container is not visible
    """
    assert run_async(playwright_event_loop, page["pipelines"].pipelinerun.logs.is_logs_container_visible()), (
        "Logs container is not visible"
    )


@then("the task navigation should be visible")
def task_navigation_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify the task navigation sidebar is displayed.

    Validates that the navigation menu containing task links is visible.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if task navigation is not visible
    """
    assert run_async(playwright_event_loop, page["pipelines"].pipelinerun.logs.is_task_navigation_visible()), (
        "Task navigation is not visible"
    )


@when("the user clicks on the first available task")
def click_first_task(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Click the first task in the navigation sidebar.

    Retrieves available tasks and clicks the first task link to view its logs.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if click fails or no tasks available
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
    Verify the selected task is visually indicated.

    Confirms task selection by checking logs container visibility for the active task.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if no task appears selected
    """
    assert run_async(playwright_event_loop, page["pipelines"].pipelinerun.logs.is_logs_container_visible()), (
        "Expected a task to be highlighted/selected"
    )


@then("each task should display a status indicator")
def each_task_has_status(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Verify all tasks show status indicators.

    Checks that every task in the navigation has an associated status icon.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if any task lacks a status indicator
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        task_statuses = await logs_page.get_all_task_statuses()
        return len(task_statuses) > 0 and all(status for status in task_statuses.values())

    assert run_async(playwright_event_loop, _verify()), "Not all tasks have status indicators"


@then(parsers.parse('the status of task "{task_name}" should be "{expected_status}"'))
def task_status_is(
    page: Dict[str, Any], task_name: str, expected_status: str, playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    Verify a specific task has the expected execution status.

    Checks the task's status indicator against expected value (success, failed, running, pending).

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param str task_name: Name of the task to verify
    :param str expected_status: Expected status value (success, failed, running, pending)
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if status does not match expected value
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        status = await logs_page.get_task_status(task_name)
        return status == expected_status

    assert run_async(playwright_event_loop, _verify()), f"Task '{task_name}' does not have '{expected_status}' status"


@when("the user waits for logs to fully load")
def wait_for_logs_load(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Wait for logs to finish loading and all tasks to complete execution.

    Optimized to check task status first - if tasks are already complete, skips polling.
    Only waits for extended periods if tasks are actually still running.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises TimeoutError if logs fail to load or tasks don't complete within timeout
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _wait() -> None:
        # Wait for loading indicators to disappear
        await logs_page.wait_for_logs_to_load(timeout=60000)

        # Wait for tasks to complete (with early exit if already done)
        await logs_page.wait_for_all_tasks_to_complete(timeout=180000)

    run_async(playwright_event_loop, _wait())


@then(parsers.parse('the logs for task "{task_name}" should contain "{expected_text}"'))
def verify_task_logs_contain_text(
    page: Dict[str, Any], task_name: str, expected_text: str, playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    Verify task logs contain specific expected text.

    Navigates to the specified task and validates that its log output includes the expected content.

    :param Dict[str, Any] page: Page object dictionary containing PipelineRun logs page instance
    :param str task_name: Name of the task whose logs to verify
    :param str expected_text: Text that should be present in the task logs
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :return: None: Raises AssertionError if expected text not found in logs
    """
    logs_page = page["pipelines"].pipelinerun.logs

    async def _verify() -> bool:
        logs_content = await logs_page.get_logs_for_task(task_name)
        return expected_text in logs_content

    assert run_async(playwright_event_loop, _verify()), (
        f"Expected text '{expected_text}' not found in logs for task '{task_name}'"
    )
