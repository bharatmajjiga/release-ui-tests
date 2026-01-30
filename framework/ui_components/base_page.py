from typing import Optional

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from framework.config.config import Config


class BasePage:
    def __init__(self, page: Page, config: Config) -> None:
        self.page = page
        self.config = config
        self.default_timeout = self.config.timeout_ms

    def click_element(self, locator: str, timeout: Optional[int] = None) -> bool:
        """
        Uses locator.click() to click an element. Waits up to the specified timeout (or default
        timeout set on page) for the element to be actionable (visible, enabled, stable).
        The default timeout is configured via page.set_default_timeout() in the fixture using
        framework's APP_TIMEOUT.
        :param str locator: name of the locator
        :param Optional[int] timeout: Optional timeout in milliseconds. If not provided, uses the
            default timeout set on the page.
        :return: bool: True if the element with mentioned locator is clickable, raises TimeoutError otherwise.
        """
        if timeout is not None:
            self.page.locator(locator).click(timeout=timeout)
        else:
            self.page.locator(locator).click()
        return True

    def fill_input(self, locator: str, value: str, timeout: Optional[int] = None) -> bool:
        """
        Uses locator.fill(value) to fill an input element. Waits up to the specified timeout (or
        default timeout set on page) for the element to be fillable (visible, enabled, stable).
        The default timeout is configured via page.set_default_timeout() in the fixture using
        framework's APP_TIMEOUT.
        :param str locator: The locator string to identify the input element.
        :param str value: The text value to fill into the input element.
        :param Optional[int] timeout: Optional timeout in milliseconds. If not provided, uses the
            default timeout set on the page.
        :return: bool: True if the element with mentioned locator is fillable, raises TimeoutError otherwise.
        """
        if timeout is not None:
            self.page.locator(locator).fill(value, timeout=timeout)
        else:
            self.page.locator(locator).fill(value)
        return True

    def is_visible(self, locator: str, timeout: Optional[int] = None) -> bool:
        """
        Uses locator.wait_for(state="visible") to check if an element is visible. Waits up to the
        specified timeout (or default timeout set on page) for the element to become visible.
        The default timeout is configured via page.set_default_timeout() in the fixture using
        framework's APP_TIMEOUT. Returns False if timeout occurs instead of raising an exception.
        :param str locator: The locator string to identify the element.
        :param Optional[int] timeout: Optional timeout in milliseconds. If not provided, uses the
            default timeout set on the page.
        :return: bool: True if the element becomes visible within the timeout, False if timeout occurs.
        """
        try:
            if timeout is not None:
                self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            else:
                self.page.locator(locator).wait_for(state="visible")
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_url_to_endwith(self, page: str, timeout: Optional[int] = None) -> bool:
        """
        Uses page.wait_for_url(pattern) to wait for the URL to match the specified pattern (ending
        with the provided page path). Waits up to the specified timeout (or default timeout set on
        page). The default timeout is configured via page.set_default_timeout() in the fixture using
        framework's APP_TIMEOUT. Raises TimeoutError if URL doesn't match within the timeout.
        :param str page: The page path that the URL should end with (e.g., "pipelines/all-namespaces").
        :param Optional[int] timeout: Optional timeout in milliseconds. If not provided, uses the
            default timeout set on the page.
        :return: bool: True if URL matches within timeout, raises TimeoutError otherwise.
        """
        if timeout is not None:
            self.page.wait_for_url(f"**/{page}", timeout=timeout)
        else:
            self.page.wait_for_url(f"**/{page}")
        return True

    def wait_for_url_to_contain(self, page: str, timeout: Optional[int] = None) -> bool:
        """
        Uses page.wait_for_function() to wait for a JavaScript function to return a truthy value,
        checking if the current URL contains the specified page string. Waits up to the specified
        timeout (or default timeout set on page). The default timeout is configured via
        page.set_default_timeout() in the fixture using framework's APP_TIMEOUT. Raises
        TimeoutError if condition isn't met within the timeout.
        :param str page: The page string that should be contained in the URL (e.g., "oauth").
        :param Optional[int] timeout: Optional timeout in milliseconds. If not provided, uses the
            default timeout set on the page.
        :return: bool: True if URL contains the specified page string within timeout, raises TimeoutError otherwise.
        """
        if timeout is not None:
            self.page.wait_for_function(f"() => window.location.href.includes('{page}')", timeout=timeout)
        else:
            self.page.wait_for_function(f"() => window.location.href.includes('{page}')")
        return True

    def _verify_page(self, expected_url_suffix: str, header_locator: str, page_name: str) -> bool:
        """
        Common verification method for page objects. Verifies that a page is currently displayed
        by checking URL pattern and header visibility
        :param str expected_url_suffix: The URL suffix that the page URL should end with
            (e.g., "dashboards", "pipelines/all-namespaces").
        :param str header_locator: The locator string for the page header element to verify visibility.
        :param str page_name: The name of the page for error messages (e.g., "Overview page",
            "Pipelines page").
        :return: bool: True if both URL and header checks pass.
        :raises AssertionError: With specific message if URL or header check fails.
        :raises TimeoutError: If URL doesn't match within the timeout.
        """
        if not self.wait_for_url_to_endwith(expected_url_suffix):
            raise AssertionError(
                f"{page_name} verification failed: URL does not end with '{expected_url_suffix}'. "
                f"Current URL: {self.page.url}"
            )
        if not self.is_visible(header_locator):
            raise AssertionError(
                f"{page_name} verification failed: Header element ({header_locator}) is not visible on the page."
            )
        return True

    def _verify_data_load(self, locator: str, tab_name: str, no_data_locator: str = None) -> bool:
        """
        Common verification method for page objects to verify that data has finished loading.
        Waits until data is loaded by checking if the specified locator is visible.
        This method implements the Template Method pattern to avoid code duplication.
        First checks if a "no data" element is visible (if provided), which is a valid state.
        If no data element is visible, returns True immediately. Otherwise, continues with
        normal data load verification.
        :param str locator: Locator string for the data element to verify.
        :param str tab_name: Tab or page name for error messages (e.g., "Pipelines tab",
            "PipelineRuns tab", "Pipelines Overview page").
        :param str no_data_locator: Optional locator string for the "no data" element.
            If provided and visible, method returns True immediately (no data is a valid state).
            Uses a 10-second timeout for this check.
        :return: bool: True if data element becomes visible within the timeout, or if no data element is visible.
        :raises AssertionError: With specific message if data does not load within the timeout.
        :raises TimeoutError: If data element doesn't become visible within the timeout.
        """
        # First check if "no data" element is visible (valid state) with 10-second timeout
        if no_data_locator is not None:
            try:
                self.page.locator(no_data_locator).wait_for(state="visible", timeout=10000)
                return True
            except PlaywrightTimeoutError:
                pass  # No data element not visible, continue with normal verification

        # Continue with normal data load verification
        if not self.is_visible(locator):
            raise AssertionError(
                f"Data load verification failed for {tab_name}: Data element ({locator}) "
                f"did not become visible within the timeout."
            )
        return True
