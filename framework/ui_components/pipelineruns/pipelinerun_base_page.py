from playwright.async_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.commons.actions_menu import ActionsMenu
from framework.ui_components.commons.favorites import Favorites
from framework.ui_components.commons.project_selector import ProjectSelector


class PipelineRunBasePage(BasePage):
    """
    Abstract base class for PipelineRun Details and YAML pages.
    Contains shared UI elements and behaviors common to both pages.
    Follows Template Method Pattern for extensibility.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.project_selector = ProjectSelector(page, config)
        self.favorites = Favorites(page, config)
        self.actions_menu = ActionsMenu(page, config)

    async def get_pipelinerun_name(self) -> str:
        """
        Returns the PipelineRun name displayed in the h1 heading.
        :return: str: The text content of the PipelineRun name heading.
        """
        # Implemented in concrete classes with their specific locators
        raise NotImplementedError("Subclass must implement get_pipelinerun_name()")

    async def click_breadcrumb_pipelineruns(self) -> bool:
        """
        Clicks the 'PipelineRuns' breadcrumb link to navigate back to the PipelineRuns list page.
        :return: bool: True if click succeeds.
        """
        # Implemented in concrete classes with their specific locators
        raise NotImplementedError("Subclass must implement click_breadcrumb_pipelineruns()")

    # Tab navigation methods (common to all PipelineRun pages)
    async def navigate_to_details_tab(self) -> bool:
        """
        Switches to the Details tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_details_tab()")

    async def navigate_to_yaml_tab(self) -> bool:
        """
        Switches to the YAML tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_yaml_tab()")

    async def navigate_to_parameters_tab(self) -> bool:
        """
        Switches to the Parameters tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_parameters_tab()")

    async def navigate_to_logs_tab(self) -> bool:
        """
        Switches to the Logs tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_logs_tab()")

    async def navigate_to_events_tab(self) -> bool:
        """
        Switches to the Events tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_events_tab()")

    async def navigate_to_approval_tasks_tab(self) -> bool:
        """
        Switches to the ApprovalTasks tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_approval_tasks_tab()")

    async def navigate_to_output_tab(self) -> bool:
        """
        Switches to the Output tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_output_tab()")

    async def navigate_to_task_runs_tab(self) -> bool:
        """
        Switches to the TaskRuns tab.
        :return: bool: True if tab click succeeds.
        """
        raise NotImplementedError("Subclass must implement navigate_to_task_runs_tab()")

    # Actions menu methods (common to all PipelineRun pages)
    async def click_actions_rerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Rerun' to rerun the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        raise NotImplementedError("Subclass must implement click_actions_rerun()")

    async def click_actions_delete_pipelinerun(self) -> bool:
        """
        Opens the Actions menu and clicks 'Delete PipelineRun' to delete the PipelineRun.
        :return: bool: True if both clicks succeed.
        """
        raise NotImplementedError("Subclass must implement click_actions_delete_pipelinerun()")
