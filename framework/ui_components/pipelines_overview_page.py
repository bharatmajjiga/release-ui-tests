from playwright.sync_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.locators import PipelinesOverViewPageLocators


class PipelinesOverViewPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = PipelinesOverViewPageLocators()

    def verify_on_page(self) -> bool:
        """
        Verifies that the Pipelines Overview page is currently displayed by checking URL and header visibility.
        First waits for URL to end with "pipelines-overview/all-namespaces", then checks if the Overview
        header is visible. Both conditions must be true for verification to pass.
        :return: bool: True if URL matches and Overview header is visible.
        Raises AssertionError with specific message if URL or header check fails.
        Raises TimeoutError if URL doesn't match within the timeout.
        """
        return self._verify_page(
            "pipelines-overview/all-namespaces", self.locators.OVERVIEW_HEADER, "Pipelines Overview page"
        )
