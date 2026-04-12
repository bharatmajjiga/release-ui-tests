from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelineruns import PipelineRunBasePageLocators, PipelineRunParametersPageLocators
from framework.ui_components.console_url_patterns import PIPELINERUN_PARAMETERS_URL
from framework.ui_components.pipelineruns.pipelinerun_base_page import PipelineRunBasePage


class PipelineRunParametersPage(PipelineRunBasePage):
    """
    Page object for the PipelineRun Parameters tab.
    Displays read-only parameters that were used when the PipelineRun was executed.
    Extends PipelineRunBasePage to inherit common tab navigation and Actions menu functionality.

    Note: PipelineRun parameters are immutable after creation, so this page is read-only.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelineRunBasePageLocators()
        self.locators = PipelineRunParametersPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the PipelineRun Parameters page is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINERUN_PARAMETERS_URL, self.base_locators.PIPELINERUN_NAME_HEADING, "PipelineRun Parameters page"
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

    # Parameters page specific methods
    async def get_parameter_names(self) -> list[str]:
        """
        Returns a list of all parameter names displayed on the page.
        :return: list[str]: List of parameter names.
        """
        name_textboxes = await self.page.locator(self.locators.PARAMETER_NAME_TEXTBOX).all()
        names = []
        for textbox in name_textboxes:
            value = await textbox.input_value()
            if value:
                names.append(value)
        return names

    async def get_parameter_values(self) -> list[str]:
        """
        Returns a list of all parameter values displayed on the page.
        :return: list[str]: List of parameter values.
        """
        value_textboxes = await self.page.locator(self.locators.PARAMETER_VALUE_TEXTBOX).all()
        values = []
        for textbox in value_textboxes:
            value = await textbox.input_value()
            if value:
                values.append(value)
        return values

    async def get_parameters(self) -> dict[str, str]:
        """
        Returns a dictionary of all parameters (name -> value mapping).
        :return: dict[str, str]: Dictionary mapping parameter names to values.
        """
        names = await self.get_parameter_names()
        values = await self.get_parameter_values()

        # Create dictionary by pairing names with values
        return dict(zip(names, values))

    async def is_parameter_displayed(self, parameter_name: str) -> bool:
        """
        Checks if a parameter with the given name is displayed on the page.
        :param str parameter_name: The name of the parameter to check.
        :return: bool: True if the parameter is visible.
        """
        names = await self.get_parameter_names()
        return parameter_name in names
