from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.commons import ActionsMenuLocators
from framework.ui_components.base_page import BasePage


class ActionsMenu(BasePage):
    """Shared component for the Actions dropdown button that appears on resource detail pages."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = ActionsMenuLocators()

    async def click_actions_button(self) -> bool:
        """
        Clicks the 'Actions' dropdown button to reveal available actions for the resource.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ACTIONS_BUTTON)

    async def is_actions_button_visible(self) -> bool:
        """
        Checks whether the 'Actions' button is visible on the page.
        :return: bool: True if the button is visible, False otherwise.
        """
        return await self.is_visible(self.locators.ACTIONS_BUTTON)
