from typing import Any, Dict

from pytest_bdd import scenarios, then

scenarios("pipelines_smoke.feature")


@then("the Pipelines page should be visible")
def pipelines_page_visible(shared_browser_page: Dict[str, Any]) -> None:
    """
    step for verifying that the Pipelines page is visible.
    :param Dict[str, Any] shared_browser_page: Dictionary containing Page Object instances (from shared_browser_page fixture).
    :return: None: Raises AssertionError if Pipelines page is not visible, TimeoutError if URL doesn't match.
    """
    assert shared_browser_page["pipelines"].verify_on_page(), "Pipelines page header not visible."
