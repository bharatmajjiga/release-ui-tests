from typing import Any, Dict, Tuple

import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from pytest import FixtureRequest

from framework.config.config import Config
from framework.ui_components.commons.left_navigation_bar import LeftNavigationBar
from framework.ui_components.commons.login_page import LoginPage
from framework.ui_components.overview_page import OverViewPage
from framework.ui_components.pipelines_overview_page import PipelinesOverViewPage
from framework.ui_components.pipelines_page import PipelinesPage
from framework.ui_components.tasks_page import TasksPage
from framework.ui_components.triggers_page import TriggersPage


def get_feature_file_path(request: FixtureRequest) -> str | None:
    """
    Return the absolute feature file path for the current test if it is a pytest-bdd scenario.
    This allows scoping browser session per feature file without one step file per feature.
    """
    node = getattr(request, "node", None)
    if node is None:
        return None
    func = getattr(node, "obj", None) or getattr(node, "function", None)
    if func is None:
        return None
    scenario = getattr(func, "__scenario__", None)
    if scenario is None:
        return None
    feature = getattr(scenario, "feature", None)
    if feature is None:
        return None
    return getattr(feature, "filename", None)


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


@pytest.fixture(scope="session")
def feature_browser_sessions(
    browser: Browser,
    browser_context_args: Dict[str, Any],
    config: Config,
) -> Dict[str, Tuple[BrowserContext, Page]]:
    """
    Session-scoped cache: one (context, page) per feature file path.
    Key = absolute feature filename from pytest-bdd. All contexts are closed at session teardown.
    """
    cache: Dict[str, Tuple[BrowserContext, Page]] = {}

    yield cache

    for context, _ in cache.values():
        context.close()


@pytest.fixture
def page(
    request: FixtureRequest,
    feature_browser_sessions: Dict[str, Tuple[BrowserContext, Page]],
    browser: Browser,
    browser_context_args: Dict[str, Any],
    config: Config,
) -> Dict[str, Any]:
    """
    One browser session per feature file. All scenarios from the same .feature file
    share the same browser context and page; scenarios from another .feature file
    get a different session. No need for a separate step file per feature—bind
    multiple features in one step module via scenarios("a.feature"), scenarios("b.feature").
    """
    feature_path = get_feature_file_path(request)
    if feature_path is None:
        # Fallback for non–pytest-bdd tests: one session per test module (nodeid prefix)
        feature_path = request.node.nodeid.split("::")[0]

    if feature_path not in feature_browser_sessions:
        context = browser.new_context(**browser_context_args)
        raw_page = context.new_page()
        raw_page.set_default_timeout(config.timeout_ms)
        context.set_default_navigation_timeout(config.timeout_ms)
        feature_browser_sessions[feature_path] = (context, raw_page)
        _login_once_for_feature(raw_page, config)

    _, raw_page = feature_browser_sessions[feature_path]

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


def _login_once_for_feature(raw_page: Page, config: Config) -> None:
    """
    Run login once when a feature file's browser session is first created.
    Navigates to console, chooses auth type from config, and verifies Overview.
    """
    login_page = LoginPage(raw_page, config)
    overview_page = OverViewPage(raw_page, config)
    assert login_page.goto() and login_page.verify_successful_navigation_to_login_page()
    login_page.choose_login_auth_type(config.auth_type)
    login_page.login()
    overview_page.verify_on_page()
