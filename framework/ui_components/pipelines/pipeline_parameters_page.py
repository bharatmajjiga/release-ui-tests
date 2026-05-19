from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import PipelineParametersPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import PIPELINE_PARAMETERS_URL


class PipelineParametersPage(BasePage):
    """Page object for the Pipeline Parameters tab - allows editing pipeline parameters."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = PipelineParametersPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Pipeline Parameters tab is currently displayed by checking URL.
        :return: bool: True if URL matches the parameters pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINE_PARAMETERS_URL, self.locators.PIPELINE_NAME_HEADING, "Pipeline Parameters page"
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

    async def fill_parameter_name(self, name: str, index: int = 0) -> bool:
        """
        Fills the parameter name input field for a specific parameter row.
        :param str name: The parameter name to enter.
        :param int index: The zero-based index of the parameter row (0 for first row, 1 for second, etc.).
        :return: bool: True if fill succeeds.
        """
        locator = f"{self.locators.PARAMETER_NAME_INPUT} >> nth={index}"
        return await self.fill_input(locator, name)

    async def fill_parameter_description(self, description: str, index: int = 0) -> bool:
        """
        Fills the parameter description input field for a specific parameter row.
        :param str description: The parameter description to enter.
        :param int index: The zero-based index of the parameter row (0 for first row, 1 for second, etc.).
        :return: bool: True if fill succeeds.
        """
        locator = f"{self.locators.PARAMETER_DESCRIPTION_INPUT} >> nth={index}"
        return await self.fill_input(locator, description)

    async def fill_parameter_default_value(self, default_value: str, index: int = 0) -> bool:
        """
        Fills the parameter default value input field for a specific parameter row.
        :param str default_value: The default value to enter.
        :param int index: The zero-based index of the parameter row (0 for first row, 1 for second, etc.).
        :return: bool: True if fill succeeds.
        """
        locator = f"{self.locators.PARAMETER_DEFAULT_VALUE_INPUT} >> nth={index}"
        return await self.fill_input(locator, default_value)

    async def click_remove_parameter(self, index: int = 0) -> bool:
        """
        Clicks the 'Remove' button for a specific parameter row to delete it.
        :param int index: The zero-based index of the parameter row to remove (0 for first row, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.REMOVE_PARAMETER_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def click_add_parameter(self) -> bool:
        """
        Clicks the 'Add Pipeline parameter' button to add a new parameter row.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_PARAMETER_BUTTON)

    async def click_save(self) -> bool:
        """
        Clicks the 'Save' button to save parameter changes.
        Note: This button is disabled until changes are made.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SAVE_BUTTON)

    async def click_reload(self) -> bool:
        """
        Clicks the 'Reload' button to discard local changes and reload parameters from the server.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.RELOAD_BUTTON)

    async def is_save_button_enabled(self) -> bool:
        """
        Checks if the Save button is enabled (parameters have been modified).
        :return: bool: True if Save button is enabled.
        """
        return await self.is_element_enabled(self.locators.SAVE_BUTTON)
