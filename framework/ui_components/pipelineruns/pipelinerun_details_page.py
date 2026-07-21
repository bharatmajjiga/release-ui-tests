from playwright.async_api import Page

from framework.config.config import Config
from framework.locators.pipelineruns import PipelineRunBasePageLocators, PipelineRunDetailsPageLocators
from framework.ui_components.console_url_patterns import PIPELINERUN_DETAILS_URL
from framework.ui_components.pipelineruns.pipelinerun_base_page import PipelineRunBasePage


class PipelineRunDetailsPage(PipelineRunBasePage):
    """
    Page object for the PipelineRun Details page.
    Shows detailed information about a specific PipelineRun resource including status, conditions, and metadata.
    Extends PipelineRunBasePage to inherit common tab navigation and Actions menu functionality.
    """

    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.base_locators = PipelineRunBasePageLocators()
        self.locators = PipelineRunDetailsPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the PipelineRun Details page is currently displayed by checking URL.
        :return: bool: True if URL matches the pattern.
        :raises AssertionError: With specific message if URL check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINERUN_DETAILS_URL, self.base_locators.PIPELINERUN_NAME_HEADING, "PipelineRun Details page"
        )

    async def verify_pipelinerun_details_sub_heading(self) -> bool:

        if not await self.is_visible(self.locators.PIPELINERUN_DETAILS_HEADING):
            raise AssertionError("Pipeline run details page sub header is not loaded.")
        return True

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

    # Details page specific methods
    async def click_namespace_link(self) -> bool:
        """
        Clicks the namespace link to navigate to the namespace details page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.NAMESPACE_LINK)

    async def click_edit_labels(self) -> bool:
        """
        Clicks the 'Edit' button next to Labels to open the labels editor.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.EDIT_LABELS_BUTTON)

    async def click_annotations(self) -> bool:
        """
        Clicks the annotations button to expand/view annotations.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ANNOTATIONS_BUTTON)

    async def click_pipeline_link(self) -> bool:
        """
        Clicks the Pipeline link in the status section to navigate to the Pipeline details page.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.PIPELINE_LINK)

    async def click_zoom_in(self) -> bool:
        """
        Clicks the 'Zoom in' button on the pipeline visualization.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ZOOM_IN_BUTTON)

    async def click_zoom_out(self) -> bool:
        """
        Clicks the 'Zoom out' button on the pipeline visualization.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.ZOOM_OUT_BUTTON)

    async def click_fit_to_screen(self) -> bool:
        """
        Clicks the 'Fit to screen' button on the pipeline visualization.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.FIT_TO_SCREEN_BUTTON)

    async def click_reset_view(self) -> bool:
        """
        Clicks the 'Reset view' button on the pipeline visualization.
        :return: bool: True if click succeeds.
        """
        return await self.click_element(self.locators.RESET_VIEW_BUTTON)

    async def is_pipelinerun_details_heading_visible(self) -> bool:
        """
        Checks if the 'PipelineRun details' heading is visible.
        :return: bool: True if heading is visible.
        """
        return await self.is_visible(self.locators.PIPELINERUN_DETAILS_HEADING)

    async def is_conditions_heading_visible(self) -> bool:
        """
        Checks if the 'Conditions' heading is visible.
        :return: bool: True if heading is visible.
        """
        return await self.is_visible(self.locators.CONDITIONS_HEADING)

    async def is_conditions_table_visible(self) -> bool:
        """
        Checks if the Conditions table is visible.
        :return: bool: True if table is visible.
        """
        return await self.is_visible(self.locators.CONDITIONS_TABLE)
