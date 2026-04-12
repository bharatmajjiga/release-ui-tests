from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.triggers import EventListenerDetailsPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector
from framework.ui_components.console_url_patterns import EVENTLISTENER_DETAILS_URL


class EventListenerDetailsPage(BasePage):
    """Page object for the EventListener Details page (viewing a specific EventListener resource)."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = EventListenerDetailsPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the EventListener Details page is currently displayed by checking URL and
        the EventListener details heading visibility.
        :return: bool: True if URL matches and EventListener details heading is visible.
        :raises AssertionError: With specific message if URL or heading check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            EVENTLISTENER_DETAILS_URL, self.locators.EVENTLISTENER_DETAILS_HEADING, "EventListener Details page"
        )

    async def get_eventlistener_name(self) -> str:
        """
        Returns the EventListener name displayed in the h1 heading.
        :return: str: The text content of the EventListener name heading.
        """
        return await self.page.locator(self.locators.EVENTLISTENER_NAME_HEADING).inner_text()

    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab to view/edit the EventListener YAML.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.locators.YAML_TAB)

    async def click_breadcrumb_eventlisteners(self) -> bool:
        """
        Clicks the 'EventListeners' breadcrumb link to navigate back to the EventListeners list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.BREADCRUMB_EVENTLISTENERS_LINK)

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

    async def is_conditions_table_visible(self) -> bool:
        """
        Checks whether the Conditions table is visible on the page.
        :return: bool: True if the table is visible, False otherwise.
        """
        return await self.is_visible(self.locators.CONDITIONS_TABLE)
