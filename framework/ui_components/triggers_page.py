from playwright.sync_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.locators import TriggersPageLocators


class TriggersPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = TriggersPageLocators()

    def verify_on_page(self) -> bool:
        """
        Verifies that the Triggers page is currently displayed by checking URL and header visibility.
        First waits for URL to end with "triggers/all-namespaces", then checks if the Triggers
        header is visible. Both conditions must be true for verification to pass.
        :return: bool: True if URL matches and Triggers header is visible.
        Raises AssertionError with specific message if URL or header check fails.
        Raises TimeoutError if URL doesn't match within the timeout.
        """
        return self._verify_page("triggers/all-namespaces", self.locators.TRIGGERS_HEADER, "Triggers page")

    def navigate_to_event_listeners_tab(self) -> bool:
        """
        Navigates to the Event Listeners tab on the Triggers page by clicking on the Event Listeners tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.EVENT_LISTENERS_TAB)

    def navigate_to_trigger_templates_tab(self) -> bool:
        """
        Navigates to the TriggerTemplates tab on the Triggers page by clicking on the TriggerTemplates tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.TRIGGER_TEMPLATES_TAB)

    def navigate_to_trigger_bindings_tab(self) -> bool:
        """
        Navigates to the TriggerBindings tab on the Triggers page by clicking on the TriggerBindings tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.TRIGGER_BINDINGS_TAB)

    def navigate_to_cluster_trigger_bindings_tab(self) -> bool:
        """
        Navigates to the ClusterTriggerBindings tab on the Triggers page by clicking the tab.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if tab click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.CLUSTER_TRIGGER_BINDINGS_TAB)

    def verify_data_load(self, locator: str = None, tab_name: str = None) -> bool:
        """
        Verifies that data has finished loading on the Triggers page or its tabs.
        Uses the base _verify_data_load method with page-specific default values.
        First checks for "no data" state, which is a valid state. If no data element is visible,
        continues with normal data load verification.
        :param str locator: Optional locator string for the data element to verify. If not provided,
            uses default locator from TriggersPageLocators (TRIGGERS_DATA_LOAD_CHECK).
        :param str tab_name: Optional tab name for error messages. If not provided, uses
            "Triggers page" as default.
        :return: bool: True if data element becomes visible within the timeout, or if no data element is visible.
        Raises AssertionError with specific message if data does not load within the timeout.
        Raises TimeoutError if data element doesn't become visible within the timeout.
        """
        default_locator = self.locators.TRIGGERS_DATA_LOAD_CHECK
        data_locator = locator if locator is not None else default_locator
        context = tab_name if tab_name else "Triggers page"
        no_data_locator = self.locators.TRIGGERS_NO_DATA_LOAD_CHECK
        return self._verify_data_load(data_locator, context, no_data_locator)
