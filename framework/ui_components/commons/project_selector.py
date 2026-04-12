from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.commons import ProjectSelectorLocators
from framework.ui_components.base_page import BasePage


class ProjectSelector(BasePage):
    """Shared component for the project selector dropdown that appears across pages."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = ProjectSelectorLocators()

    async def click_project_selector(self) -> bool:
        """
        Clicks the project selector dropdown button to open the project list.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.PROJECT_SELECTOR_BUTTON)

    async def is_project_selector_visible(self) -> bool:
        """
        Checks whether the project selector button is visible on the page.
        :return: bool: True if the project selector is visible, False otherwise.
        """
        return await self.is_visible(self.locators.PROJECT_SELECTOR_BUTTON)
