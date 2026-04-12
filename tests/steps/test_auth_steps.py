"""
Authentication and Login Test Steps.

This module contains BDD step definitions for user authentication and login scenarios.
Follows Single Responsibility Principle - handles only authentication-related steps.
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import given, parsers, when

from framework.config.config import Config
from framework.fixtures.async_bridge import run_async


@given("the user is logged into openshift console with auth kube:admin")
def user_logged_into_openshift_kube_admin(
    page: Dict[str, Any],
    config: Config,
    playwright_event_loop: asyncio.AbstractEventLoop,
    bdd_openshift_console_session: Dict[str, Any],
) -> None:
    """
    Logs in once per feature file (module-scoped browser + session flag).

    For the first scenario, performs full login. For subsequent scenarios in the same feature,
    checks if session is still valid (not on oauth page) and continues from current page
    without unnecessary navigation. This optimizes test execution by avoiding page reloads.

    Session sharing benefits:
    - First scenario: Full login → lands on page
    - Subsequent scenarios: No navigation → continues from where previous scenario left off
    - Only navigates if session expired (detected by oauth redirect)
    """

    async def _ensure_logged_in() -> None:
        # First scenario in feature - perform full login
        if not bdd_openshift_console_session.get("kube_admin_logged_in"):
            assert await page["login"].goto()
            assert await page["login"].verify_successful_navigation_to_login_page()
            assert await page["login"].choose_login_auth_type("kube:admin")
            assert await page["login"].login()
            assert await page["overview"].verify_on_page()
            bdd_openshift_console_session["kube_admin_logged_in"] = True
            return

        # Subsequent scenarios - check if session is still valid without navigation
        # Only navigate if session expired (oauth redirect detected)
        current_url = page["raw_page"].url
        if "oauth" in current_url.lower():
            # Session expired - perform full login again
            bdd_openshift_console_session["kube_admin_logged_in"] = False
            await _ensure_logged_in()
            return

        # Session still valid - continue from current page (no navigation, no reload)
        # Each scenario picks up where the previous one left off

    run_async(playwright_event_loop, _ensure_logged_in())


@given("the user is on the OpenShift login page")
def user_on_login_page(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to and verifying the OpenShift login page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if navigation or verification fails.
    """

    async def _step() -> None:
        assert await page["login"].goto() and await page["login"].verify_successful_navigation_to_login_page()

    run_async(playwright_event_loop, _step())


@when(parsers.parse("user chooses to login with {auth_type}"))
def user_to_chose_login_auth_type(
    page: Dict[str, Any], auth_type: str, playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    step for choosing the authentication type.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :param str auth_type: the type of authentication user chosen for login
    :return: None: Raises AssertionError if login verification fails, TimeoutError if operations timeout.
    """
    run_async(playwright_event_loop, page["login"].choose_login_auth_type(auth_type))


@when("the user logs in with valid credentials")
def user_logs_in(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for performing login with valid credentials.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises AssertionError if login verification fails, TimeoutError if operations timeout.
    """

    async def _step() -> None:
        await page["login"].login()
        await page["overview"].verify_on_page()

    run_async(playwright_event_loop, _step())
