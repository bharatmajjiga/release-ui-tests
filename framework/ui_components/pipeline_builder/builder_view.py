from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import BuilderViewLocators
from framework.ui_components.base_page import BasePage


class BuilderView(BasePage):
    """
    View object for Pipeline Builder's visual form interface.
    Handles builder-specific UI elements and interactions.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = BuilderViewLocators()

    async def fill_pipeline_name(self, name: str) -> bool:
        """
        Fills the pipeline name input field.
        :param str name: The name for the pipeline.
        :return: bool: True if fill succeeds.
        """
        return await self.fill_input(self.locators.PIPELINE_NAME_INPUT, name)

    async def click_add_task(self) -> bool:
        """
        Clicks the 'Add task' button to open the quick search dialog for adding tasks.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_TASK_BUTTON)

    async def click_add_finally_task(self) -> bool:
        """
        Clicks the 'Add finally task' button to add tasks that run after pipeline completion.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_FINALLY_TASK_BUTTON)

    async def click_add_parameter(self) -> bool:
        """
        Clicks the 'Add parameter' button to add a new parameter to the pipeline.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_PARAMETER_BUTTON)

    async def click_add_workspace(self) -> bool:
        """
        Clicks the 'Add workspace' button to add a new workspace to the pipeline.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_WORKSPACE_BUTTON)

    async def search_task(self, search_text: str) -> bool:
        """
        Types text into the quick search bar to search for tasks.
        :param str search_text: The text to search for.
        :return: bool: True if fill succeeds.
        """
        return await self.fill_input(self.locators.QUICK_SEARCH_INPUT, search_text)

    async def click_add_task_from_search(self) -> bool:
        """
        Clicks the 'Add' button in the task search results to add the selected task.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ADD_TASK_FROM_SEARCH_BUTTON)
