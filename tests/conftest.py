# Import fixtures from framework (page is overridden below to beat pytest-playwright)
from typing import Any, Dict

import pytest
from playwright.sync_api import BrowserContext

from framework.config.config import Config
from framework.fixtures.ui_fixtures import *  # noqa: F403, F401
from framework.fixtures.ui_fixtures import _build_page_dict


@pytest.fixture(scope="module")
def page(bdd_context: BrowserContext, config: Config) -> Dict[str, Any]:
    """Override: use our sync page dict so pytest-playwright's async page is not used with -n auto."""
    raw_page = bdd_context.new_page()
    raw_page.set_default_timeout(config.timeout_ms)
    return _build_page_dict(raw_page, config)


# Register plugins: framework options (--headed, --ignore-ssl-errors) and step definitions
pytest_plugins = [
    "framework.config.pytest_args_options_fixture",
    "tests.steps.test_common_steps",
]
