"""
UI fixtures for BDD tests.

Uses module-scoped browser/context/page (via sync_playwright) so one browser session
is shared by all scenarios in a feature file. This supports parallel execution
(pytest-xdist) and avoids per-scenario browser startup.
"""

from typing import Dict, Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, SyncPlaywright, sync_playwright
from pytest import FixtureRequest

from framework.config.config import Config
from framework.ui_components.commons.left_navigation_bar import LeftNavigationBar
from framework.ui_components.commons.login_page import LoginPage
from framework.ui_components.overview_page import OverViewPage
from framework.ui_components.pipelines_overview_page import PipelinesOverViewPage
from framework.ui_components.pipelines_page import PipelinesPage
from framework.ui_components.tasks_page import TasksPage
from framework.ui_components.triggers_page import TriggersPage


@pytest.fixture(scope="session")
def config(request: FixtureRequest) -> object:
    """
    Fixture that creates and returns a Config singleton instance.
    Skips the session when CONSOLE_URL, CONSOLE_USERNAME, or CONSOLE_PASSWORD are missing.
    :param FixtureRequest request: Pytest fixture request object
    :return: Config: A singleton Config object containing application configuration.
    """
    try:
        return Config()
    except ValueError as e:
        pytest.skip(str(e))


@pytest.fixture(scope="session")
def browser_context_args(request: FixtureRequest) -> Dict[str, object]:
    """
    Fixture that configures browser context arguments.
    By default, SSL errors are ignored (True). Set --ignore-ssl-errors=false to disable.
    Also sets viewport size (1920x1080). Navigation timeout is set on the context in bdd_context.
    :param FixtureRequest request: Pytest fixture request object (automatically injected).
    :return: Dict[str, Any]: Browser context arguments with SSL and viewport configuration.
    """
    ignore_ssl = request.config.getoption("--ignore-ssl-errors", default=True)
    return {
        "ignore_https_errors": ignore_ssl,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="module")
def bdd_playwright() -> Generator[SyncPlaywright, None, None]:
    """
    Module-scoped Playwright instance. One per test module (feature file).
    """
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="module")
def bdd_browser(bdd_playwright: SyncPlaywright, request: FixtureRequest) -> Generator[Browser, None, None]:
    """
    Module-scoped browser. One per test module (feature file).
    """
    headed = request.config.getoption("--headed", default=False)
    browser = bdd_playwright.chromium.launch(headless=not headed)
    yield browser
    browser.close()


@pytest.fixture(scope="module")
def bdd_context(
    bdd_browser: Browser,
    browser_context_args: Dict[str, object],
    config: Config,
) -> Generator[BrowserContext, None, None]:
    """
    Module-scoped browser context. One per test module (feature file).
    """
    context = bdd_browser.new_context(**browser_context_args)
    context.set_default_navigation_timeout(config.timeout_ms)
    yield context
    context.close()


def _build_page_dict(raw_page: Page, config: Config) -> Dict[str, object]:
    """Build the page object dict. Used by the page fixture."""
    return {
        "raw_page": raw_page,
        "login": LoginPage(raw_page, config),
        "nav": LeftNavigationBar(raw_page, config),
        "overview": OverViewPage(raw_page, config),
        "pipelines_overview": PipelinesOverViewPage(raw_page, config),
        "pipelines": PipelinesPage(raw_page, config),
        "tasks": TasksPage(raw_page, config),
        "triggers": TriggersPage(raw_page, config),
    }


@pytest.fixture(scope="module")
def page(bdd_context: BrowserContext, config: Config) -> Dict[str, object]:
    """
    Module-scoped page dict: one browser session per feature file (test module).
    All scenarios in a feature file share this session. Sets default timeouts
    from framework config (APP_TIMEOUT).
    :return: Dict[str, Any]: Dictionary containing:
        - "raw_page": The raw Playwright Page object.
        - "login": LoginPage instance.
        - "nav": LeftNavigationBar instance.
        - "overview": OverViewPage instance.
        - "pipelines_overview": PipelinesOverViewPage instance.
        - "pipelines": PipelinesPage instance.
        - "tasks": TasksPage instance.
        - "triggers": TriggersPage instance.
    """
    raw_page = bdd_context.new_page()
    raw_page.set_default_timeout(config.timeout_ms)
    return _build_page_dict(raw_page, config)
