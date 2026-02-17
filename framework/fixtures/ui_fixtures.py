from typing import Any, Dict

import pytest
from playwright.sync_api import Browser, Page
from pytest import FixtureRequest

from framework.config.config import Config
from framework.ui_components.commons.left_navigation_bar import LeftNavigationBar
from framework.ui_components.commons.login_page import LoginPage
from framework.ui_components.overview_page import OverViewPage
from framework.ui_components.pipelines_overview_page import PipelinesOverViewPage
from framework.ui_components.pipelines_page import PipelinesPage
from framework.ui_components.tasks_page import TasksPage
from framework.ui_components.triggers_page import TriggersPage


def _build_page_dict(page: Page, config: Config) -> Dict[str, Any]:
    """
    Builds the application page objects dictionary for a given Playwright page.
    Shared by both function-scoped and module-scoped page fixtures.
    """
    page.set_default_timeout(config.timeout_ms)
    page.context.set_default_navigation_timeout(config.timeout_ms)
    return {
        "raw_page": page,
        "login": LoginPage(page, config),
        "nav": LeftNavigationBar(page, config),
        "overview": OverViewPage(page, config),
        "pipelines_overview": PipelinesOverViewPage(page, config),
        "pipelines": PipelinesPage(page, config),
        "tasks": TasksPage(page, config),
        "triggers": TriggersPage(page, config),
    }


@pytest.fixture(scope="module")
def shared_browser_page(
    browser: Browser,
    browser_context_args: Dict[str, Any],
    config: Config,
) -> Dict[str, Any]:
    """
    One browser context and page per feature file (test module).
    Use this fixture in BDD step definitions so all scenarios in a feature share
    the same session. The first scenario performs login; subsequent scenarios
    reuse the logged-in session (steps are idempotent).
    """
    context = browser.new_context(**browser_context_args)
    page = context.new_page()
    try:
        yield _build_page_dict(page, config)
    finally:
        context.close()


@pytest.fixture(scope="session")
def config(request: FixtureRequest) -> object:
    """
    fixture that creates and returns a Config singleton instance.
    :param FixtureRequest request: Pytest fixture request object
    :return: Config: A singleton Config object with application configuration.
    """
    return Config()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any], request: FixtureRequest) -> Dict[str, Any]:
    """
    fixture that configures browser context arguments,
    By default, SSL errors are ignored (True). Set --ignore-ssl-errors=false to disable.
    Also maximizes the browser window by setting a large viewport size (1920x1080).
    Note: Navigation timeout is set separately in the context fixture since it's not a valid
    parameter for browser.new_context().
    :param Dict[str, Any] browser_context_args: Default browser context arguments from Playwright.
    :param FixtureRequest request: Pytest fixture request object (automatically injected).
    :return: Dict[str, Any]: Updated browser context arguments with SSL and viewport configuration.
    """
    ignore_ssl = request.config.getoption("--ignore-ssl-errors", default=True)

    return {
        **browser_context_args,
        "ignore_https_errors": ignore_ssl,
        "viewport": {"width": 1920, "height": 1080},  # Maximize browser window
    }


@pytest.fixture(scope="function")
def page(page: Page, config: Config) -> Dict[str, Any]:
    """
    Fixture that injects custom application Page Objects (function scope).
    Sets default timeout for all page actions and navigation to use framework's
    APP_TIMEOUT. For BDD feature files, prefer shared_browser_page (module scope)
    so one browser session is reused across all scenarios in the feature.
    :param Page page: Raw page object from Playwright
    :param Config config: Config object containing application configuration
    :return: Dict[str, Any]: Dictionary of page object instances (login, nav, overview, etc.)
    """
    return _build_page_dict(page, config)
