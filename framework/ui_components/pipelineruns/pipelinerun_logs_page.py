from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelineruns import PipelineRunBasePageLocators, PipelineRunLogsPageLocators
from framework.ui_components.console_url_patterns import PIPELINERUN_LOGS_URL
from framework.ui_components.pipelineruns.pipelinerun_base_page import PipelineRunBasePage


class PipelineRunLogsPage(PipelineRunBasePage):
    """
    Page object for the PipelineRun Logs tab.
    Displays logs from all tasks in the PipelineRun execution with navigation and download options.
    Extends PipelineRunBasePage to inherit common tab navigation and Actions menu functionality.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelineRunBasePageLocators()
        self.locators = PipelineRunLogsPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the PipelineRun Logs page is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINERUN_LOGS_URL, self.base_locators.PIPELINERUN_NAME_HEADING, "PipelineRun Logs page"
        )

    async def get_pipelinerun_name(self) -> str:
        """
        Returns the PipelineRun name displayed in the h1 heading.
        :return: str: The text content of the PipelineRun name heading.
        """
        return await self.page.locator(self.base_locators.PIPELINERUN_NAME_HEADING).inner_text()

    async def click_breadcrumb_pipelineruns(self) -> bool:
        """
        Clicks the 'PipelineRuns' breadcrumb link to navigate back to the PipelineRuns list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.BREADCRUMB_PIPELINERUNS_LINK)

    # Tab navigation methods (implementing base class interface)
    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.YAML_TAB)

    async def navigate_to_parameters_tab(self) -> bool:
        """
        Switches to the Parameters tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.PARAMETERS_TAB)

    async def navigate_to_logs_tab(self) -> bool:
        """
        Switches to the Logs tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.LOGS_TAB)

    async def navigate_to_events_tab(self) -> bool:
        """
        Switches to the Events tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.EVENTS_TAB)

    async def navigate_to_approval_tasks_tab(self) -> bool:
        """
        Switches to the ApprovalTasks tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.APPROVAL_TASKS_TAB)

    async def navigate_to_output_tab(self) -> bool:
        """
        Switches to the Output tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.OUTPUT_TAB)

    async def navigate_to_task_runs_tab(self) -> bool:
        """
        Switches to the TaskRuns tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.TASK_RUNS_TAB)

    # Actions menu methods (implementing base class interface)
    async def click_actions_rerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Rerun' to rerun the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        return await self.actions_menu.click_actions_button() and await self.click_element(
            self.base_locators.ACTIONS_RERUN_MENU_ITEM
        )

    async def click_actions_delete_pipelinerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Delete PipelineRun' to delete the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        return await self.actions_menu.click_actions_button() and await self.click_element(
            self.base_locators.ACTIONS_DELETE_PIPELINERUN_MENU_ITEM
        )

    # Logs page specific methods
    async def click_task_link(self, task_name: str) -> bool:
        """
        Clicks a task link in the navigation to view that task's logs.
        :param str task_name: The name of the task to view logs for.
        :return: bool: True if click succeeds.
        """
        locator = f'{self.locators.TASK_LINK}:has-text("{task_name}")'
        return await self.click_element(locator)

    async def get_available_tasks(self) -> list[str]:
        """
        Returns a list of task names available in the logs navigation.
        :return: list[str]: List of task names.
        """
        task_links = await self.page.locator(self.locators.TASK_LINK).all()
        task_names = []
        for link in task_links:
            text = await link.inner_text()
            # Remove any whitespace and extract just the task name
            task_name = text.strip()
            if task_name:
                task_names.append(task_name)
        return task_names

    async def click_download(self) -> bool:
        """
        Clicks the 'Download' button to download the current task's logs.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.DOWNLOAD_BUTTON)

    async def click_download_all(self) -> bool:
        """
        Clicks the 'Download all task logs' button to download logs from all tasks.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.DOWNLOAD_ALL_BUTTON)

    async def click_expand(self) -> bool:
        """
        Clicks the 'Expand' button to expand/collapse the logs view.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.EXPAND_BUTTON)

    async def is_logs_container_visible(self) -> bool:
        """
        Checks if the logs content container is visible.
        :return: bool: True if logs container is visible.
        """
        return await self.is_visible(self.locators.LOGS_CONTAINER)

    async def is_task_navigation_visible(self) -> bool:
        """
        Checks if the task navigation sidebar is visible.
        :return: bool: True if task navigation is visible.
        """
        return await self.is_visible(self.locators.TASK_NAVIGATION)

    async def get_task_status(self, task_name: str) -> str:
        """
        Gets the status of a specific task by checking status icons in the task navigation.
        :param str task_name: The name of the task.
        :return: str: Status of the task - 'success', 'failed', 'running', 'pending', or 'unknown'.
        """
        task_link = f'{self.locators.TASK_LINK}:has-text("{task_name}")'
        task_element = self.page.locator(task_link)

        if await task_element.locator(self.locators.TASK_SUCCESS_ICON).count() > 0:
            return "success"
        elif await task_element.locator(self.locators.TASK_FAILURE_ICON).count() > 0:
            return "failed"
        elif await task_element.locator(self.locators.TASK_RUNNING_ICON).count() > 0:
            return "running"
        elif await task_element.locator(self.locators.TASK_PENDING_ICON).count() > 0:
            return "pending"
        else:
            return "unknown"

    async def get_all_task_statuses(self) -> dict[str, str]:
        """
        Gets the status of all tasks in the pipeline run.
        :return: dict[str, str]: Dictionary mapping task names to their statuses.
        """
        tasks = await self.get_available_tasks()
        task_statuses = {}
        for task in tasks:
            status = await self.get_task_status(task)
            task_statuses[task] = status
        return task_statuses

    async def validate_all_tasks_displayed(self, expected_tasks: list[str]) -> bool:
        """
        Validates that all expected tasks are displayed in the task navigation.
        :param list[str] expected_tasks: List of expected task names.
        :return: bool: True if all expected tasks are displayed.
        :raises AssertionError: If any expected task is missing.
        """
        available_tasks = await self.get_available_tasks()
        missing_tasks = [task for task in expected_tasks if task not in available_tasks]

        if missing_tasks:
            raise AssertionError(
                f"Expected tasks are missing from the logs page. "
                f"Missing tasks: {missing_tasks}. "
                f"Available tasks: {available_tasks}"
            )
        return True

    async def validate_all_tasks_successful(self) -> bool:
        """
        Validates that all tasks in the pipeline run have succeeded.
        :return: bool: True if all tasks are successful.
        :raises AssertionError: If any task is not successful.
        """
        task_statuses = await self.get_all_task_statuses()
        failed_tasks = {name: status for name, status in task_statuses.items() if status != "success"}

        if failed_tasks:
            raise AssertionError(
                f"Not all tasks are successful. Failed/Non-successful tasks: {failed_tasks}. "
                f"All task statuses: {task_statuses}"
            )
        return True

    async def get_current_task_logs(self) -> str:
        """
        Gets the log text content for the currently displayed task.
        :return: str: The log text content.
        """
        try:
            log_element = self.page.locator(self.locators.LOGS_TEXT_CONTENT).first
            return await log_element.inner_text()
        except Exception:
            return ""

    async def get_logs_for_task(self, task_name: str) -> str:
        """
        Gets the log content for a specific task by navigating to it.
        :param str task_name: The name of the task.
        :return: str: The log text content for the task.
        """
        await self.click_task_link(task_name)
        # Wait longer for logs to load (they may be streamed)
        await self.page.wait_for_timeout(5000)
        return await self.get_current_task_logs()

    async def validate_logs_present_for_task(self, task_name: str, min_length: int = 10) -> bool:
        """
        Validates that logs are present for a specific task.
        :param str task_name: The name of the task.
        :param int min_length: Minimum expected length of log content (default: 10 characters).
        :return: bool: True if logs are present and meet minimum length.
        :raises AssertionError: If logs are missing or too short.
        """
        logs = await self.get_logs_for_task(task_name)
        if len(logs) < min_length:
            raise AssertionError(
                f"Logs for task '{task_name}' are missing or insufficient. "
                f"Log length: {len(logs)}, expected minimum: {min_length}"
            )
        return True

    async def validate_logs_present_for_all_tasks(self, min_length: int = 10) -> bool:
        """
        Validates that logs are present for all tasks in the pipeline run.
        :param int min_length: Minimum expected length of log content per task.
        :return: bool: True if all tasks have logs.
        :raises AssertionError: If any task is missing logs.
        """
        tasks = await self.get_available_tasks()
        tasks_without_logs = []

        for task in tasks:
            logs = await self.get_logs_for_task(task)
            if len(logs) < min_length:
                tasks_without_logs.append(task)

        if tasks_without_logs:
            raise AssertionError(
                f"The following tasks have missing or insufficient logs: {tasks_without_logs}. "
                f"Minimum expected log length: {min_length} characters"
            )
        return True

    async def get_active_task_name(self) -> str:
        """
        Gets the name of the currently active/selected task in the navigation.
        :return: str: The name of the active task.
        """
        try:
            active_link = self.page.locator(self.locators.TASK_LINK_ACTIVE).first
            return await active_link.inner_text()
        except Exception:
            return ""

    async def is_loading(self) -> bool:
        """
        Checks if logs are currently loading.
        :return: bool: True if loading indicator is visible.
        """
        return await self.is_visible(self.locators.LOADING_INDICATOR) or await self.is_visible(
            self.locators.SKELETON_LOADER
        )

    async def wait_for_logs_to_load(self, timeout: int = 30000) -> bool:
        """
        Waits for logs to finish loading.
        :param int timeout: Maximum time to wait in milliseconds (default: 30000ms).
        :return: bool: True if logs loaded within timeout.
        """
        try:
            await self.page.wait_for_selector(
                f"{self.locators.LOADING_INDICATOR}, {self.locators.SKELETON_LOADER}",
                state="hidden",
                timeout=timeout,
            )
            return True
        except Exception:
            return await self.is_logs_container_visible()

    async def wait_for_all_tasks_to_complete(self, timeout: int = 180000, poll_interval: int = 5000) -> bool:
        """
        Waits for all tasks to complete (reach 'success' or 'failed' status).
        Polls task statuses until all are complete or timeout is reached.
        :param int timeout: Maximum time to wait in milliseconds (default: 180000ms).
        :param int poll_interval: Time between status checks in milliseconds (default: 5000ms).
        :return: bool: True if all tasks completed within timeout.
        :raises TimeoutError: If tasks don't complete within timeout.
        """
        import asyncio

        start_time = asyncio.get_event_loop().time()
        end_time = start_time + (timeout / 1000)

        while asyncio.get_event_loop().time() < end_time:
            task_statuses = await self.get_all_task_statuses()
            incomplete_tasks = {
                name: status for name, status in task_statuses.items() if status not in ("success", "failed")
            }

            if not incomplete_tasks:
                return True

            await self.page.wait_for_timeout(poll_interval)

        raise TimeoutError(
            f"Tasks did not complete within {timeout}ms. Current statuses: {await self.get_all_task_statuses()}"
        )

    async def validate_task_logs_contain_text(self, task_name: str, expected_text: str) -> bool:
        """
        Validates that logs for a specific task contain expected text.
        :param str task_name: The name of the task.
        :param str expected_text: Text that should be present in the logs.
        :return: bool: True if expected text is found in logs.
        :raises AssertionError: If expected text is not found.
        """
        logs = await self.get_logs_for_task(task_name)
        if expected_text not in logs:
            raise AssertionError(
                f"Expected text '{expected_text}' not found in logs for task '{task_name}'. "
                f"Log preview: {logs[:200]}..."
            )
        return True

    async def get_task_count(self) -> int:
        """
        Gets the total number of tasks displayed in the navigation.
        :return: int: Number of tasks.
        """
        return await self.page.locator(self.locators.TASK_LINK).count()

    async def validate_pipeline_run_success(self) -> bool:
        """
        Comprehensive validation that ensures the pipeline run is fully successful.
        Checks that:
        - Task navigation is visible
        - All tasks are displayed
        - All tasks have 'success' status
        - All tasks have logs present
        :return: bool: True if all validations pass.
        :raises AssertionError: If any validation fails with detailed error message.
        """
        if not await self.is_task_navigation_visible():
            raise AssertionError("Task navigation is not visible on the logs page")

        tasks = await self.get_available_tasks()
        if len(tasks) == 0:
            raise AssertionError("No tasks found in the pipeline run")

        await self.validate_all_tasks_successful()
        await self.validate_logs_present_for_all_tasks()

        return True
