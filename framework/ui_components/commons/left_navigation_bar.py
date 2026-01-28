from playwright.sync_api import Page

from framework.config.config import Config
from framework.ui_components.base_page import BasePage
from framework.ui_components.locators import LeftNavigationBarLocators


class LeftNavigationBar(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.locators = LeftNavigationBarLocators()

    def verify_pipelines_button_visible(self) -> bool:
        """
        Verifies that the Pipelines button is visible in the left navigation bar.
        Uses is_visible() which waits up to the configured timeout for the element to become visible.
        Returns False if the button is not visible within the timeout.
        :return: bool: True if Pipelines button is visible, False if not visible within timeout.
        """
        return self.is_visible(self.locators.PIPELINES_BUTTON)

    def verify_link_available_under_pipelines_button(self, link_name: str) -> bool:
        """
        Verifies that a specific link is available under the Pipelines button in the left navigation bar.
        Maps the link name to the appropriate locator and checks if the link is visible.
        :param str link_name: The name of the link to verify (e.g., "Overview", "Pipelines", "Tasks", "Triggers").
        :return: bool: True if the link is visible, False if not visible within timeout.
        Raises AssertionError if an invalid link name is provided.
        """
        link_locator_map = {
            "Overview": self.locators.NAV_OVERVIEW_LINK,
            "Pipelines": self.locators.NAV_PIPELINES_LINK,
            "Tasks": self.locators.NAV_TASKS_LINK,
            "Triggers": self.locators.NAV_TRIGGERS_LINK,
        }

        if link_name not in link_locator_map:
            raise AssertionError(
                f"Invalid link name '{link_name}' provided. Valid options: {list(link_locator_map.keys())}"
            )

        return self.is_visible(link_locator_map[link_name])

    def click_pipelines_button(self) -> bool:
        """
        Expand Pipelines sectoin by clicking the Pipelines button
        Uses click_element() for both actions, which waits up to the configured timeout for elements
        to be clickable. This is a two-step navigation process. Returns True only if both clicks succeed.
        :return: bool: True if both navigation clicks succeed, False if any click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.PIPELINES_BUTTON)

    def navigate_to_pipelines(self) -> bool:
        """
        Navigates to the Pipelines page by clicking on the Pipelines link.
        Uses click_element() for both actions, which waits up to the configured timeout for elements
        to be clickable. This is a two-step navigation process. Returns True only if both clicks succeed.
        :return: bool: True if both navigation clicks succeed, False if any click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.NAV_PIPELINES_LINK)

    def navigate_to_overview(self) -> bool:
        """
        Navigates to the Pipelines Overview page by clicking on the Overview link.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if navigation click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.NAV_OVERVIEW_LINK)

    def navigate_to_tasks(self) -> bool:
        """
        Navigates to the Tasks page by clicking on the Tasks link.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if navigation click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.NAV_TASKS_LINK)

    def navigate_to_triggers(self) -> bool:
        """
        Navigates to the Triggers page by clicking on the Triggers link.
        Uses click_element() which waits up to the configured timeout for the element to be clickable.
        :return: bool: True if navigation click succeeds, False if click fails or raises TimeoutError.
        """
        return self.click_element(self.locators.NAV_TRIGGERS_LINK)
