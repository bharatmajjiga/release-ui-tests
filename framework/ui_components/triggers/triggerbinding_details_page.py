from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.triggers import TriggerBindingDetailsPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import TRIGGERBINDING_DETAILS_URL


class TriggerBindingDetailsPage(BasePage):
    """Page object for the TriggerBinding Details page (viewing a specific TriggerBinding resource)."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TriggerBindingDetailsPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the TriggerBinding Details page is currently displayed by checking URL and
        the TriggerBinding details heading visibility.
        :return: bool: True if URL matches and TriggerBinding details heading is visible.
        :raises AssertionError: With specific message if URL or heading check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            TRIGGERBINDING_DETAILS_URL, self.locators.TRIGGERBINDING_DETAILS_HEADING, "TriggerBinding Details page"
        )

    async def get_triggerbinding_name(self) -> str:
        """
        Returns the TriggerBinding name displayed in the h1 heading.
        :return: str: The text content of the TriggerBinding name heading.
        """
        return await self.page.locator(self.locators.TRIGGERBINDING_NAME_HEADING).inner_text()

    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab to view/edit the TriggerBinding YAML.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.YAML_TAB)

    async def click_breadcrumb_triggerbindings(self) -> bool:
        """
        Clicks the 'TriggerBindings' breadcrumb link to navigate back to the TriggerBindings list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.BREADCRUMB_TRIGGERBINDINGS_LINK)

    async def click_namespace_link(self) -> bool:
        """
        Clicks the namespace link in the details section to navigate to the namespace page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAMESPACE_LINK)

    async def click_edit_labels(self) -> bool:
        """
        Clicks the 'Edit' button next to Labels to open the labels editor.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.EDIT_LABELS_BUTTON)

    async def click_annotations(self) -> bool:
        """
        Clicks the annotations button to view/edit annotations.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ANNOTATIONS_BUTTON)
