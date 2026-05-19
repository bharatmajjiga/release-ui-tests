from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelineruns import PipelineRunBasePageLocators, PipelineRunYamlPageLocators
from framework.ui_components.console_url_patterns import PIPELINERUN_YAML_URL
from framework.ui_components.pipelineruns.pipelinerun_base_page import PipelineRunBasePage


class PipelineRunYamlPage(PipelineRunBasePage):
    """
    Page object for the PipelineRun YAML editor tab.
    Allows viewing and editing the YAML definition of a PipelineRun resource (read-only for completed runs).
    Extends PipelineRunBasePage to inherit common tab navigation and Actions menu functionality.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelineRunBasePageLocators()
        self.locators = PipelineRunYamlPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the PipelineRun YAML editor page is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINERUN_YAML_URL, self.base_locators.PIPELINERUN_NAME_HEADING, "PipelineRun YAML page"
        )

    async def get_pipelinerun_name(self) -> str:
        """
        Returns the PipelineRun name displayed in the h1 heading.
        :return: str: The text content of the PipelineRun name heading.
        """
        return await self.page.locator(self.base_locators.PIPELINERUN_NAME_HEADING).inner_text()

    async def click_breadcrumb_pipelineruns(self) -> bool:
        """
        Clicks the 'PipelineRuns' breadcrumb link to navigate back to the PipelineRuns list page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.base_locators.BREADCRUMB_PIPELINERUNS_LINK)

    # Tab navigation methods (implementing base class interface)
    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.DETAILS_TAB)

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.YAML_TAB)

    async def navigate_to_parameters_tab(self) -> bool:
        """
        Switches to the Parameters tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.PARAMETERS_TAB)

    async def navigate_to_logs_tab(self) -> bool:
        """
        Switches to the Logs tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.LOGS_TAB)

    async def navigate_to_events_tab(self) -> bool:
        """
        Switches to the Events tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.EVENTS_TAB)

    async def navigate_to_approval_tasks_tab(self) -> bool:
        """
        Switches to the ApprovalTasks tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.APPROVAL_TASKS_TAB)

    async def navigate_to_output_tab(self) -> bool:
        """
        Switches to the Output tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.OUTPUT_TAB)

    async def navigate_to_task_runs_tab(self) -> bool:
        """
        Switches to the TaskRuns tab.
        :return: bool: True if tab click succeeds.
        """
        return await self.click_element(self.base_locators.TASK_RUNS_TAB)

    # Actions menu methods (implementing base class interface)
    async def click_actions_rerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Rerun' to rerun the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        return await self.actions_menu.click_actions_button() and await self.click_element(
            self.base_locators.ACTIONS_RERUN_MENU_ITEM
        )

    async def click_actions_delete_pipelinerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Delete PipelineRun' to delete the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        return await self.actions_menu.click_actions_button() and await self.click_element(
            self.base_locators.ACTIONS_DELETE_PIPELINERUN_MENU_ITEM
        )

    # YAML page specific methods
    async def click_reload(self) -> bool:
        """
        Clicks the 'Reload' button to reload the YAML from the server.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.RELOAD_BUTTON)

    async def click_cancel(self) -> bool:
        """
        Clicks the 'Cancel' button to discard changes.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.CANCEL_BUTTON)

    async def click_download(self) -> bool:
        """
        Clicks the 'Download' button to download the YAML file.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.DOWNLOAD_BUTTON)

    async def click_copy_code(self) -> bool:
        """
        Clicks the 'Copy code to clipboard' button.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.COPY_CODE_BUTTON)

    async def click_editor_settings(self) -> bool:
        """
        Clicks the 'Editor settings' button to open editor configuration.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.EDITOR_SETTINGS_BUTTON)

    async def click_toggle_fullscreen(self) -> bool:
        """
        Clicks the 'Toggle fullscreen mode' button.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.TOGGLE_FULLSCREEN_BUTTON)

    async def click_toggle_sidebar(self) -> bool:
        """
        Clicks the sidebar toggle button to show/hide the schema sidebar.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.TOGGLE_SIDEBAR_BUTTON)

    async def click_shortcuts(self) -> bool:
        """
        Clicks the 'Shortcuts' button to view keyboard shortcuts.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.SHORTCUTS_BUTTON)

    async def is_yaml_editor_visible(self) -> bool:
        """
        Checks if the YAML editor (Monaco editor) is visible.
        :return: bool: True if editor is visible.
        """
        return await self.is_visible(self.locators.YAML_EDITOR)
