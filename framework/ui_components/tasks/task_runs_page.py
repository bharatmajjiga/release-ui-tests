from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.tasks import TaskRunsPageLocators
from framework.ui_components.tasks.tasks_base_page import TasksBasePage


class TaskRunsPage(TasksBasePage):
    """
    Page object for the TaskRuns tab - listing TaskRun resources.
    Inherits common functionality from TasksBasePage.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TaskRunsPageLocators()

    async def click_name_column_header(self) -> bool:
        """
        Clicks the 'Name' column header to sort TaskRuns by name.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAME_COLUMN_HEADER)

    async def click_pipeline_column_header(self) -> bool:
        """
        Clicks the 'Pipeline' column header to sort TaskRuns by pipeline.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.PIPELINE_COLUMN_HEADER)

    async def click_task_column_header(self) -> bool:
        """
        Clicks the 'Task' column header to sort TaskRuns by task.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.TASK_COLUMN_HEADER)

    async def click_pod_column_header(self) -> bool:
        """
        Clicks the 'Pod' column header to sort TaskRuns by pod.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.POD_COLUMN_HEADER)

    async def click_status_column_header(self) -> bool:
        """
        Clicks the 'Status' column header to sort TaskRuns by status.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.STATUS_COLUMN_HEADER)

    async def click_started_column_header(self) -> bool:
        """
        Clicks the 'Started' column header to sort TaskRuns by start time.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.STARTED_COLUMN_HEADER)

    async def verify_task_runs_tab_data_load(self) -> bool:
        """
        Verifies that TaskRun data has finished loading on the TaskRuns tab.
        :return: bool: True if data loads successfully or "no data" message is shown.
        """
        return await self.verify_data_load(tab_name="TaskRuns tab")
