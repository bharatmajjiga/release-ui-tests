from playwright.async_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.console_url_patterns import PIPELINES_OVERVIEW_URL
from framework.ui_components.locators import PipelinesOverViewPageLocators


class PipelinesOverViewPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = PipelinesOverViewPageLocators()

    async def verify_on_page(self) -> bool:
        """
        Verifies that the Pipelines Overview page is currently displayed by checking URL and header visibility.
        Waits for the URL to match pipelines-overview/all-namespaces or pipelines-overview/ns/<namespace>,
        then checks if the Overview header is visible.
        :return: bool: True if URL matches and Overview header is visible.
        Raises AssertionError with specific message if URL or header check fails.
        Raises TimeoutError if URL doesn't match within the timeout.
        """
        return await self._verify_page_regex(
            PIPELINES_OVERVIEW_URL, self.locators.OVERVIEW_HEADER, "Pipelines Overview page"
        )
