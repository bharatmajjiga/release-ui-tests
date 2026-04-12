# Import fixtures from framework
from framework.fixtures.ui_fixtures import *  # noqa: F403, F401

pytest_plugins = ["tests.steps.test_auth_steps", "tests.steps.test_navigation_steps"]
