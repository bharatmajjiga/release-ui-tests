from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.tasks import TasksPageLocators
from framework.ui_components.tasks.tasks_base_page import TasksBasePage


class TasksPage(TasksBasePage):
    """
    Page object for the Tasks tab - listing Task resources.
    Inherits common functionality from TasksBasePage.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TasksPageLocators()

    async def click_name_column_header(self) -> bool:
        """
        Clicks the 'Name' column header to sort Tasks by name.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAME_COLUMN_HEADER)

    async def click_namespace_column_header(self) -> bool:
        """
        Clicks the 'Namespace' column header to sort Tasks by namespace.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAMESPACE_COLUMN_HEADER)

    async def click_created_column_header(self) -> bool:
        """
        Clicks the 'Created' column header to sort Tasks by creation date.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CREATED_COLUMN_HEADER)

    async def verify_tasks_tab_data_load(self) -> bool:
        """
        Verifies that Task data has finished loading on the Tasks tab.
        :return: bool: True if data loads successfully or "no data" message is shown.
        """
        return await self.verify_data_load(tab_name="Tasks tab")
