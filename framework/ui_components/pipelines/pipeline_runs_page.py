from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import PipelineRunsPageLocators
from framework.ui_components.pipelines.pipelines_base_page import PipelinesBasePage


class PipelineRunsPage(PipelinesBasePage):
    """
    Page object for the PipelineRuns tab - listing PipelineRun resources.
    Inherits common functionality from PipelinesBasePage.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = PipelineRunsPageLocators()

    async def click_name_column_header(self) -> bool:
        """
        Clicks the 'Name' column header to sort PipelineRuns by name.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAME_COLUMN_HEADER)

    async def click_vulnerabilities_column_header(self) -> bool:
        """
        Clicks the 'Vulnerabilities' column header to sort PipelineRuns by vulnerabilities.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.VULNERABILITIES_COLUMN_HEADER)

    async def click_status_column_header(self) -> bool:
        """
        Clicks the 'Status' column header to sort PipelineRuns by status.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.STATUS_COLUMN_HEADER)

    async def click_task_status_column_header(self) -> bool:
        """
        Clicks the 'Task status' column header to sort PipelineRuns by task status.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.TASK_STATUS_COLUMN_HEADER)

    async def click_started_column_header(self) -> bool:
        """
        Clicks the 'Started' column header to sort PipelineRuns by start time.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.STARTED_COLUMN_HEADER)

    async def click_duration_column_header(self) -> bool:
        """
        Clicks the 'Duration' column header to sort PipelineRuns by duration.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.DURATION_COLUMN_HEADER)

    async def click_view_logs(self, index: int = 0) -> bool:
        """
        Clicks the 'View logs' button for a specific PipelineRun row.
        :param int index: The zero-based index of the row (0 for first row, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.VIEW_LOGS_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def verify_pipeline_runs_tab_data_load(self) -> bool:
        """
        Verifies that PipelineRun data has finished loading on the PipelineRuns tab.
        :return: bool: True if data loads successfully or "no data" message is shown.
        """
        return await self.verify_data_load(tab_name="PipelineRuns tab")
