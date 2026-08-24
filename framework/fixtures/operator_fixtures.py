"""Session-scoped fixture to ensure OpenShift Pipelines operator is installed via UI."""

import asyncio
import logging
import os
from typing import Any, Dict

import pytest
from playwright.async_api import Browser

from framework.config.config import Config
from framework.fixtures.async_bridge import run_async
from framework.ui_components.commons.login_page import LoginPage
from framework.ui_components.operators.operator_install_page import OperatorInstallPage
from framework.ui_components.overview_page import OverViewPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def ensure_osp_installed(
    browser: Browser,
    browser_context_args: Dict[str, Any],
    config: Config,
    playwright_event_loop: asyncio.AbstractEventLoop,
) -> None:
    async def _install() -> None:
        context = await browser.new_context(**browser_context_args)
        page = await context.new_page()
        page.set_default_timeout(config.timeout_ms)
        try:
            login = LoginPage(page, config)
            overview = OverViewPage(page, config)
            installer = OperatorInstallPage(page, config)

            assert await login.goto()
            assert await login.perform_login(config.auth_type)
            assert await overview.verify_on_page()
            assert await installer.install_operator()
        finally:
            await page.close()
            await context.close()

    run_async(playwright_event_loop, _install())
