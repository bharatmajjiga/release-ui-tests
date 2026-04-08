from playwright.async_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.console_url_patterns import TASKS_URL
from framework.ui_components.locators import TasksPageLocators


class TasksPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TasksPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Tasks page is currently displayed by checking URL and header visibility.
        Waits for the URL to match tasks/all-namespaces or tasks/ns/<namespace>, then checks if the
        Tasks header is visible.
        :return: bool: True if URL matches and Tasks header is visible.
        Raises AssertionError with specific message if URL or header check fails.
        Raises TimeoutError if URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(TASKS_URL, self.locators.TASKS_HEADER, "Tasks page")

    async def navigate_to_tasks_tab(self) -> bool:
        """
        Navigates to the Tasks tab on the Tasks page by clicking on the Tasks tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return await self.click_element(self.locators.TASKS_TAB)

    async def navigate_to_task_runs_tab(self) -> bool:
        """
        Navigates to the TaskRuns tab on the Tasks page by clicking on the TaskRuns tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return await self.click_element(self.locators.TASK_RUNS_TAB)

    async def verify_data_load(self, locator: str = None, tab_name: str = None) -> bool:
        """
        Verifies that data has finished loading on the Tasks page or its tabs.
        Uses the base _verify_data_load method with page-specific default values.
        First checks for "no data" state, which is a valid state. If no data element is visible,
        continues with normal data load verification.
        :param str locator: Optional locator string for the data element to verify. If not provided,
            uses default locator from TasksPageLocators (TASKS_DATA_LOAD_CHECK).
        :param str tab_name: Optional tab name for error messages. If not provided, uses
            "Tasks page" as default.
        :return: bool: True if data element becomes visible within the timeout, or if no data element is visible.
        Raises AssertionError with specific message if data does not load within the timeout.
        Raises TimeoutError if data element doesn't become visible within the timeout.
        """
        default_locator = self.locators.TASKS_DATA_LOAD_CHECK
        data_locator = locator if locator is not None else default_locator
        context = tab_name if tab_name else "Tasks page"
        no_data_locator = self.locators.TASKS_NO_DATA_LOAD_CHECK
        return await self._verify_data_load(data_locator, context, no_data_locator)
