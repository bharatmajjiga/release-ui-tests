"""
Trigger Navigation Test Steps.

This module contains BDD step definitions for trigger-specific navigation,
including tab navigation (EventListeners, TriggerTemplates, TriggerBindings, ClusterTriggerBindings)
and page verifications.
Follows Single Responsibility Principle - handles only trigger domain navigation.
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import scenarios, then, when

from framework.fixtures.async_bridge import run_async

scenarios("../features/pipeline_navigation_triggers_and_sub_pages.feature")


@when("the user navigates to EventListeners tab")
@then("the user navigates to EventListeners tab")
def user_navigates_to_event_listeners_tab(
    page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    step for navigating to the EventListeners tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["triggers"].list.navigate_to_event_listeners_tab()), (
        "Failed to navigate to EventListeners tab."
    )
    assert run_async(playwright_event_loop, page["triggers"].list.verify_data_load(tab_name="EventListeners tab"))


@when("the user navigates to TriggerTemplates tab")
@then("the user navigates to TriggerTemplates tab")
def user_navigates_to_trigger_templates_tab(
    page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    step for navigating to the TriggerTemplates tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["triggers"].list.navigate_to_trigger_templates_tab()), (
        "Failed to navigate to TriggerTemplates tab."
    )
    assert run_async(playwright_event_loop, page["triggers"].list.verify_data_load(tab_name="TriggerTemplates tab"))


@when("the user navigates to TriggerBindings tab")
@then("the user navigates to TriggerBindings tab")
def user_navigates_to_trigger_bindings_tab(
    page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    step for navigating to the TriggerBindings tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["triggers"].list.navigate_to_trigger_bindings_tab()), (
        "Failed to navigate to TriggerBindings tab."
    )
    assert run_async(playwright_event_loop, page["triggers"].list.verify_data_load(tab_name="TriggerBindings tab"))


@when("the user navigates to ClusterTriggerBindings tab")
@then("the user navigates to ClusterTriggerBindings tab")
def user_navigates_to_cluster_trigger_bindings_tab(
    page: Dict[str, Any], playwright_event_loop: asyncio.AbstractEventLoop
) -> None:
    """
    step for navigating to the ClusterTriggerBindings tab on the Triggers page.
    :param Dict[str, Any] page: Dictionary containing Page Object instances (from page fixture).
    :return: None: Raises TimeoutError if tab element is not clickable within the timeout.
    Raises AssertionError if navigation fails.
    """
    assert run_async(playwright_event_loop, page["triggers"].list.navigate_to_cluster_trigger_bindings_tab()), (
        "Failed to navigate to ClusterTriggerBindings tab."
    )
    assert run_async(
        playwright_event_loop, page["triggers"].list.verify_data_load(tab_name="ClusterTriggerBindings tab")
    )
