from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.overview import RepositoriesPageLocators
from framework.ui_components.pipelines.pipelines_base_page import PipelinesBasePage


class RepositoriesPage(PipelinesBasePage):
    """
    Page object for the Repositories tab - listing Repository resources.
    Inherits common functionality from PipelinesBasePage.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = RepositoriesPageLocators()

    async def click_name_column_header(self) -> bool:
        """
        Clicks the 'Name' column header to sort Repositories by name.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAME_COLUMN_HEADER)

    async def verify_repositories_tab_data_load(self) -> bool:
        """
        Verifies that Repository data has finished loading on the Repositories tab.
        :return: bool: True if data loads successfully or "no data" message is shown.
        """
        return await self.verify_data_load(tab_name="Repositories tab")
