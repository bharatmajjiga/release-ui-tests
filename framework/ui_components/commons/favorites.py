from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.commons import FavoritesLocators
from framework.ui_components.base_page import BasePage


class Favorites(BasePage):
    """Shared component for the favorites button that appears across pages."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = FavoritesLocators()

    async def click_add_to_favorites(self) -> bool:
        """
        Clicks the 'Add to favorites' button to favorite the current page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_TO_FAVORITES_BUTTON)

    async def is_add_to_favorites_visible(self) -> bool:
        """
        Checks whether the 'Add to favorites' button is visible on the page.
        :return: bool: True if the button is visible, False otherwise.
        """
        return await self.is_visible(self.locators.ADD_TO_FAVORITES_BUTTON)
