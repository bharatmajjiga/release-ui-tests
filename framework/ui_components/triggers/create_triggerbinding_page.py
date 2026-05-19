from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.triggers import CreateTriggerBindingPageLocators
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector


class CreateTriggerBindingPage(BasePage):
    """Page object for the Create TriggerBinding YAML editor page."""

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = CreateTriggerBindingPageLocators()
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Create TriggerBinding page is currently displayed by checking URL and header visibility.
        Waits for the URL to contain 'triggers.tekton.dev~v1beta1~TriggerBinding/~new', then checks if the
        Create TriggerBinding header is visible.
        :return: bool: True if URL matches and Create TriggerBinding header is visible.
        :raises AssertionError: With specific message if URL or header check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self.wait_for_url_to_contain(
            "triggers.tekton.dev~v1beta1~TriggerBinding/~new"
        ) and await self.is_visible(self.locators.CREATE_TRIGGERBINDING_HEADER)

    async def is_yaml_editor_visible(self) -> bool:
        """
        Checks whether the Monaco YAML editor is visible on the page.
        :return: bool: True if the editor is visible, False otherwise.
        """
        return await self.is_visible(self.locators.YAML_EDITOR)

    async def click_copy_code(self) -> bool:
        """
        Clicks the 'Copy code to clipboard' toolbar button.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.COPY_CODE_BUTTON)

    async def click_editor_settings(self) -> bool:
        """
        Clicks the 'Editor settings' toolbar button.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.EDITOR_SETTINGS_BUTTON)

    async def click_toggle_fullscreen(self) -> bool:
        """
        Clicks the 'Toggle fullscreen mode' toolbar button.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.TOGGLE_FULLSCREEN_BUTTON)

    async def click_shortcuts(self) -> bool:
        """
        Clicks the 'Shortcuts' button to display keyboard shortcuts.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SHORTCUTS_BUTTON)

    async def click_create(self) -> bool:
        """
        Clicks the 'Create' button to submit the YAML and create the TriggerBinding resource.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CREATE_BUTTON)

    async def click_cancel(self) -> bool:
        """
        Clicks the 'Cancel' button to discard changes and navigate back.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CANCEL_BUTTON)

    async def click_download(self) -> bool:
        """
        Clicks the 'Download' button to download the current YAML content as a file.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.DOWNLOAD_BUTTON)
