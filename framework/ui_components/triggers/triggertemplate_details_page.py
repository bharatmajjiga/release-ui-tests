from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.triggers import TriggerTemplateDetailsPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import TRIGGERTEMPLATE_DETAILS_URL


class TriggerTemplateDetailsPage(BasePage):
    """Page object for the TriggerTemplate Details page (viewing a specific TriggerTemplate resource)."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TriggerTemplateDetailsPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the TriggerTemplate Details page is currently displayed by checking URL and
        the TriggerTemplate details heading visibility.
        :return: bool: True if URL matches and TriggerTemplate details heading is visible.
        :raises AssertionError: With specific message if URL or heading check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            TRIGGERTEMPLATE_DETAILS_URL, self.locators.TRIGGERTEMPLATE_DETAILS_HEADING, "TriggerTemplate Details page"
        )

    async def get_triggertemplate_name(self) -> str:
        """
        Returns the TriggerTemplate name displayed in the h1 heading.
        :return: str: The text content of the TriggerTemplate name heading.
        """
        return await self.page.locator(self.locators.TRIGGERTEMPLATE_NAME_HEADING).inner_text()

    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab to view/edit the TriggerTemplate YAML.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.YAML_TAB)

    async def click_breadcrumb_triggertemplates(self) -> bool:
        """
        Clicks the 'TriggerTemplates' breadcrumb link to navigate back to the TriggerTemplates list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.BREADCRUMB_TRIGGERTEMPLATES_LINK)

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
