"""
Task Navigation Test Steps.

This module contains BDD step definitions for task-specific navigation,
including tab navigation (Tasks, TaskRuns) and page verifications.
Follows Single Responsibility Principle - handles only task domain navigation.
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import scenarios, then, when

from framework.fixtures.async_bridge import run_async

# Register scenarios from tasks_test.feature
scenarios("../features/pipeline_navigation_tasks_and_sub_pages.feature")


@when("the user navigates to Tasks tab")
@then("the user navigates to Tasks tab")
def user_navigates_to_tasks_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to the Tasks tab on the Tasks page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["tasks"].list.navigate_to_tasks_tab()), (
        "Failed to navigate to Tasks tab."
    )
    assert run_async(playwright_event_loop, page["tasks"].list.verify_data_load(tab_name="Tasks tab"))


@when("the user navigates to TaskRuns tab")
@then("the user navigates to TaskRuns tab")
def user_navigates_to_task_runs_tab(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for navigating to the TaskRuns tab on the Tasks page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["tasks"].list.navigate_to_task_runs_tab()), (
        "Failed to navigate to TaskRuns tab."
    )
    assert run_async(playwright_event_loop, page["tasks"].list.verify_data_load(tab_name="TaskRuns tab"))


@then("the tasks page should be visible")
def tasks_page_visible(page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop) -> None:
    """
    step for verifying that the Tasks page is visible.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises AssertionError if Tasks page is not visible, TimeoutError if URL doesn't match.
    """
    assert run_async(playwright_event_loop, page["tasks"].list.verify_on_page()), "Tasks page header not visible."
