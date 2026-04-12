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
