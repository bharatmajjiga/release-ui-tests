from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import PipelinePipelineRunsTabPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import PIPELINE_PIPELINERUNS_TAB_URL


class PipelinePipelineRunsTabPage(BasePage):
    """
    Page object for the Pipeline PipelineRuns tab.
    Shows a filtered list of PipelineRuns for a specific Pipeline.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = PipelinePipelineRunsTabPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Pipeline PipelineRuns tab is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINE_PIPELINERUNS_TAB_URL, self.locators.PIPELINE_NAME_HEADING, "Pipeline PipelineRuns tab page"
        )

    async def get_pipeline_name(self) -> str:
        """
        Returns the pipeline name displayed in the h1 heading.
        :return: str: The text content of the pipeline name heading.
        """
        return await self.page.locator(self.locators.PIPELINE_NAME_HEADING).inner_text()

    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.YAML_TAB)

    async def navigate_to_parameters_tab(self) -> bool:
        """
        Switches to the Parameters tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.PARAMETERS_TAB)

    async def navigate_to_metrics_tab(self) -> bool:
        """
        Switches to the Metrics tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.METRICS_TAB)

    async def navigate_to_pipelineruns_tab(self) -> bool:
        """
        Switches to the PipelineRuns tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.PIPELINERUNS_TAB)

    async def click_breadcrumb_pipelines(self) -> bool:
        """
        Clicks the 'Pipelines' breadcrumb link to navigate back to the Pipelines list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.BREADCRUMB_PIPELINES_LINK)

    async def search_by_name(self, search_text: str) -> bool:
        """
        Types text into the 'Search by name...' input field to filter PipelineRuns.
        :param str search_text: The text to search for.
        :return: bool: True if fill succeeds.
        """
        return await self.fill_input(self.locators.SEARCH_INPUT, search_text)

    async def click_filter_button(self) -> bool:
        """
        Clicks the 'Filter' button to open the filter dropdown.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.FILTER_BUTTON)

    async def click_clear_all_filters(self) -> bool:
        """
        Clicks the 'Clear all filters' button to reset all active filters.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CLEAR_ALL_FILTERS_BUTTON)

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

    async def click_kebab_menu(self, index: int = 0) -> bool:
        """
        Clicks the kebab menu button for a specific PipelineRun row to open row actions.
        :param int index: The zero-based index of the row (0 for first row, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.KEBAB_MENU_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def verify_data_load(self) -> bool:
        """
        Verifies that PipelineRun data has finished loading on the PipelineRuns tab.
        :return: bool: True if data grid becomes visible within the timeout.
        :raises AssertionError: If data does not load within the timeout.
        """
        return await self.is_visible(self.locators.DATA_GRID)
