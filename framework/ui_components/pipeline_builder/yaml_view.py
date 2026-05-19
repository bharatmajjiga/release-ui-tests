from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelines import YamlViewLocators
from framework.ui_components.base_page import BasePage


class YamlView(BasePage):
    """
    View object for Pipeline Builder's YAML editor interface.
    Handles YAML editor-specific UI elements and interactions.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = YamlViewLocators()

    async def fill_yaml_editor(self, yaml_content: str) -> bool:
        """
        Fills the YAML editor with the provided YAML content.
        :param str yaml_content: The YAML content to insert.
        :return: bool: True if fill succeeds.
        """
        return await self.fill_input(self.locators.YAML_EDITOR, yaml_content)

    async def get_yaml_content(self) -> str:
        """
        Gets the current content from the YAML editor.
        :return: str: The YAML content from the editor.
        """
        return await self.get_element_text(self.locators.YAML_EDITOR)

    async def click_sidebar_close(self) -> bool:
        """
        Clicks the Close button to close the sidebar panel.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SIDEBAR_CLOSE_BUTTON)

    async def click_samples_tab(self) -> bool:
        """
        Clicks the 'Samples' tab in the sidebar to view sample pipelines.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SAMPLES_TAB)

    async def click_snippets_tab(self) -> bool:
        """
        Clicks the 'Snippets' tab in the sidebar to view YAML snippets.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SNIPPETS_TAB)

    async def click_sample_try_it(self, index: int = 0) -> bool:
        """
        Clicks the 'Try it' button for a specific sample pipeline.
        :param int index: The zero-based index of the sample (0 for first, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.SAMPLE_TRY_IT_BUTTON} >> nth={index}"
        return await self.click_element(locator)

    async def click_sample_download_yaml(self, index: int = 0) -> bool:
        """
        Clicks the 'Download YAML' button for a specific sample pipeline.
        :param int index: The zero-based index of the sample (0 for first, 1 for second, etc.).
        :return: bool: True if click succeeds.
        """
        locator = f"{self.locators.SAMPLE_DOWNLOAD_YAML_BUTTON} >> nth={index}"
        return await self.click_element(locator)
