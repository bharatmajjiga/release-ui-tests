"""
Common Test Steps.

This module contains BDD step definitions for user authentication and login scenarios.
Follows Single Responsibility Principle - handles only authentication-related steps.
"""

import asyncio
from typing import Any, Dict

from pytest_bdd import parsers, when

from framework.fixtures.async_bridge import run_async
from framework.helpers.yaml_loader import YamlLoader


@when(parsers.parse('the user creates a pipelinerun from YAML file "{yaml_file}"'))
def create_pipelinerun_from_yaml(
    page: Dict[str, Any], yaml_file: str, playwright_event_loop: asyncio.AbstractEventLoop, config: object
) -> None:
    """
    Create a PipelineRun by loading YAML from test data and submitting via UI.

    Always navigates to PipelineRuns page first to ensure consistent starting state
    (browser session is shared between scenarios, so we don't know which page we're on).

    :param Dict[str, Any] page: Page object dictionary
    :param str yaml_file: Name of YAML file in test_data/pipelineruns/
    :param asyncio.AbstractEventLoop playwright_event_loop: Event loop for async execution
    :param object config: Config object for timeout values
    :return: None: Raises AssertionError if creation fails
    """

    async def _step() -> None:
        # Load YAML content using helper
        yaml_content = YamlLoader.load_pipelinerun_yaml(yaml_file)

        # Wait for PipelineRuns tab data to load
        data_loaded = await page["pipelines"].runs.verify_pipeline_runs_tab_data_load()
        assert data_loaded, "PipelineRuns tab failed to load before creating PipelineRun"

        # Click Create button and select PipelineRun from dropdown (combo method)
        create_clicked = await page["pipelines"].list.click_create_pipeline_run()
        assert create_clicked, "Failed to open Create dropdown and click PipelineRun option"

        # Wait for Create PipelineRun page to load
        await page["raw_page"].wait_for_timeout(1000)

        # Verify we're on the Create PipelineRun page
        on_create_page = await page["pipelines"].create_run.verify_on_page()
        assert on_create_page, "Failed to navigate to Create PipelineRun page"

        # Fill YAML editor using MonacoEditor component directly
        yaml_filled = await page["pipelines"].create_run.monaco_editor.set_content(yaml_content)
        assert yaml_filled, f"Failed to fill YAML editor with content from '{yaml_file}'"

        # Wait a moment for YAML validation
        await page["raw_page"].wait_for_timeout(1000)

        # Click Create button to submit
        create_submitted = await page["pipelines"].create_run.click_create()
        assert create_submitted, "Failed to click Create button to submit PipelineRun YAML"

        # Wait for redirect to PipelineRun details page
        await page["raw_page"].wait_for_load_state("networkidle", timeout=config.timeout_ms)

        # Debug: Log current URL after submission
        import logging

        logger = logging.getLogger(__name__)
        current_url = page["raw_page"].url
        logger.info(f"[DEBUG] Current URL after Create click: {current_url}")

    run_async(playwright_event_loop, _step())
