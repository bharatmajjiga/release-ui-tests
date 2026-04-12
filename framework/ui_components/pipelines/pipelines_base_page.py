from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import PipelinesBasePageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import PIPELINES_NS_URL


class PipelinesBasePage(BasePage):
    """
    Abstract base class for Pipelines, PipelineRuns, and Repositories pages.
    Contains shared UI elements and behaviors common to all three tabs.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelinesBasePageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Pipelines page is currently displayed by checking URL and header visibility.
        Waits for the URL to match /pipelines/ns/<namespace>, then checks if the Pipelines header is visible.
        :return: bool: True if URL matches and Pipelines header is visible.
        :raises AssertionError: With specific message if URL or header check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(PIPELINES_NS_URL, self.base_locators.PIPELINES_HEADER, "Pipelines page")

    async def click_setup_github_app(self) -> bool:
        """
        Clicks the 'Setup GitHub App' link to navigate to the GitHub App configuration page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.SETUP_GITHUB_APP_LINK)

    async def search_by_name(self, search_text: str) -> bool:
        """
        Types text into the 'Search by name...' input field to filter resources.
        :param str search_text: The text to search for.
        :return: bool: True if fill succeeds.
        """
        return await self.fill_input(self.base_locators.SEARCH_INPUT, search_text)

    async def click_filter_button(self) -> bool:
        """
        Clicks the 'Filter' button to open the filter dropdown.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.FILTER_BUTTON)

    async def click_clear_all_filters(self) -> bool:
        """
        Clicks the 'Clear all filters' button to reset all active filters.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.CLEAR_ALL_FILTERS_BUTTON)

    async def click_kebab_menu(self, index: int = 0) -> bool:
        """
        Clicks the kebab menu button for a specific row to open row actions.
        :param int index: The zero-based index of the row (0 for first row, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.base_locators.KEBAB_MENU_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def click_create_button(self) -> bool:
        """
        Clicks the 'Create' button to open the create dropdown menu.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.CREATE_BUTTON)

    async def click_create_pipeline(self) -> bool:
        """
        Opens the Create dropdown and clicks 'Pipeline' to navigate to the Create Pipeline form.
        :return: bool: True if both clicks succeed.
        """
        return await self.click_element(self.base_locators.CREATE_BUTTON) and await self.click_element(
            self.base_locators.CREATE_PIPELINE_MENU_ITEM
        )

    async def click_create_pipeline_run(self) -> bool:
        """
        Opens the Create dropdown and clicks 'PipelineRun' to navigate to the Create PipelineRun form.
        :return: bool: True if both clicks succeed.
        """
        return await self.click_element(self.base_locators.CREATE_BUTTON) and await self.click_element(
            self.base_locators.CREATE_PIPELINE_RUN_MENU_ITEM
        )

    async def click_create_repository(self) -> bool:
        """
        Opens the Create dropdown and clicks 'Repository' to navigate to the Create Repository form.
        :return: bool: True if both clicks succeed.
        """
        return await self.click_element(self.base_locators.CREATE_BUTTON) and await self.click_element(
            self.base_locators.CREATE_REPOSITORY_MENU_ITEM
        )

    async def navigate_to_pipelines_tab(self) -> bool:
        """
        Navigates to the Pipelines tab by clicking on the Pipelines tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.PIPELINES_TAB)

    async def navigate_to_pipeline_runs_tab(self) -> bool:
        """
        Navigates to the PipelineRuns tab by clicking on the PipelineRuns tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.PIPELINE_RUNS_TAB)

    async def navigate_to_repositories_tab(self) -> bool:
        """
        Navigates to the Repositories tab by clicking on the Repositories tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.REPOSITORIES_TAB)

    async def verify_data_load(self, tab_name: str = "Pipelines page") -> bool:
        """
        Verifies that data has finished loading on the Pipelines, PipelineRuns, or Repositories tab.
        First checks for 'no data' state, which is a valid state. If no data element is visible,
        continues with normal data load verification.
        :param str tab_name: Tab name for error messages (e.g., "Pipelines tab", "PipelineRuns tab").
        :return: bool: True if data element becomes visible within the timeout, or if no data element is visible.
        :raises AssertionError: If data does not load within the timeout.
        """
        return await self._verify_data_load(self.base_locators.DATA_GRID, tab_name, self.base_locators.NO_DATA_MESSAGE)
