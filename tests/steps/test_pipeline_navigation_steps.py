"""
Pipeline Navigation Test Steps.

This module contains BDD step definitions for pipeline-specific navigation,
including tab navigation (Pipelines, PipelineRuns, Repositories) and page verifications.
Follows Single Responsibility Principle - handles only pipeline domain navigation.
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import scenarios, then, when

from framework.fixtures.async_bridge import run_async

scenarios(
    "../features/pipeline_navigation_pipelines_and_sub_pages.feature",
    "../features/pipelines_navigation_left_navigation.feature",
)


@when("the user navigates to Pipelines tab")
@then("the user navigates to Pipelines tab")
def user_navigates_to_pipelines_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to the Pipelines tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["pipelines"].list.navigate_to_pipelines_tab()), (
        "Failed to navigate to Pipelines tab."
    )
    assert run_async(playwright_event_loop, page["pipelines"].list.verify_data_load(tab_name="Pipelines tab"))


@when("the user navigates to PipelineRuns tab")
@then("the user navigates to PipelineRuns tab")
def user_navigates_to_pipeline_runs_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to the PipelineRuns tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["pipelines"].list.navigate_to_pipeline_runs_tab()), (
        "Failed to navigate to PipelineRuns tab."
    )
    assert run_async(playwright_event_loop, page["pipelines"].list.verify_data_load(tab_name="PipelineRuns tab"))


@when("the user navigates to Repositories tab")
@then("the user navigates to Repositories tab")
def user_navigates_to_repositories_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to the Repositories tab on the Pipelines page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["pipelines"].list.navigate_to_repositories_tab()), (
        "Failed to navigate to Repositories tab."
    )
    assert run_async(playwright_event_loop, page["pipelines"].list.verify_data_load(tab_name="Repositories tab"))


@then("the Pipelines page should be visible")
def pipelines_page_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for verifying that the Pipelines page is visible.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises AssertionError if Pipelines page is not visible, TimeoutError if URL doesn't match.
    """
    assert run_async(playwright_event_loop, page["pipelines"].list.verify_on_page()), (
        "Pipelines page header not visible."
    )
