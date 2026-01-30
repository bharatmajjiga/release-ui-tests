from playwright.sync_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.locators import OverViewPageLocators

# Flag to track if tour has been skipped across test sessions
# This avoids unnecessary wait time in test execution
# TODO: When parallel test execution is implemented, make this thread-safe by:
#       1. Import threading module
#       2. Add _tour_skipped_lock = threading.Lock()
#       3. Wrap the flag check and modification in: with _tour_skipped_lock:
#       4. Use double-check locking pattern for optimal performance
_tour_skipped = False


class OverViewPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = OverViewPageLocators()

    def verify_on_page(self) -> bool:
        """
        Verifies that the Overview page is currently displayed by checking URL and header visibility.
        First checks for and dismisses the "Skip tour" popup if present (for first-time login).
        Uses a flag to avoid unnecessary wait time - once the tour is skipped (or determined to not
        be present), subsequent calls skip this check entirely. Then waits for URL to end with
        "dashboards", and checks if the Overview header is visible. Both conditions must be true
        for verification to pass.
        Note: Flag is not thread-safe currently. See TODO comment for thread-safe implementation
        when parallel test execution is added.
        :return: bool: True if URL matches and Overview header is visible.
        Raises AssertionError with specific message if URL or header check fails.
        Raises TimeoutError if URL doesn't match within the timeout.
        """
        global _tour_skipped

        # Only check for tour popup if it hasn't been skipped yet
        # TODO: When parallel execution is implemented, wrap this block in:
        #       with _tour_skipped_lock:
        #           if not _tour_skipped:
        #               ... (existing logic)
        if not _tour_skipped:
            if self.is_visible(self.locators.SKIP_TOUR_BUTTON):
                self.click_element(self.locators.SKIP_TOUR_BUTTON)
            # Set flag to True whether popup was found or not to skip future checks
            _tour_skipped = True

        return self._verify_page("dashboards", self.locators.OVERVIEW_HEADER, "Overview page")
