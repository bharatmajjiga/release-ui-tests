from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelineruns import PipelineRunBasePageLocators, PipelineRunTaskRunsPageLocators
from framework.ui_components.console_url_patterns import PIPELINERUN_TASKRUNS_URL
from framework.ui_components.pipelineruns.pipelinerun_base_page import PipelineRunBasePage


class PipelineRunTaskRunsPage(PipelineRunBasePage):
    """
    Page object for the PipelineRun TaskRuns tab.
    Displays TaskRuns that were created by this PipelineRun execution with filtering and sorting capabilities.
    Extends PipelineRunBasePage to inherit common tab navigation and Actions menu functionality.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelineRunBasePageLocators()
        self.locators = PipelineRunTaskRunsPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the PipelineRun TaskRuns page is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINERUN_TASKRUNS_URL, self.base_locators.PIPELINERUN_NAME_HEADING, "PipelineRun TaskRuns page"
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

    # TaskRuns page specific methods
    async def search_by_name(self, search_text: str) -> bool:
        """
        Types text into the 'Search by name...' input field to filter TaskRuns.
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

    async def click_column_management(self) -> bool:
        """
        Clicks the 'Column management' button to open the column management panel.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.COLUMN_MANAGEMENT_BUTTON)

    async def click_clear_all_filters(self) -> bool:
        """
        Clicks the 'Clear all filters' button to reset all active filters.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CLEAR_ALL_FILTERS_BUTTON)

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

    async def click_kebab_menu(self, index: int = 0) -> bool:
        """
        Clicks the kebab menu button for a specific TaskRun row to open row actions.
        :param int index: The zero-based index of the row (0 for first row, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.KEBAB_MENU_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def verify_data_load(self) -> bool:
        """
        Verifies that TaskRun data has finished loading on the TaskRuns tab.
        :return: bool: True if data grid becomes visible within the timeout.
        :raises AssertionError: If data does not load within the timeout.
        """
        return await self.is_visible(self.locators.DATA_GRID)
