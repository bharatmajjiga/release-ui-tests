# Import fixtures from framework
from framework.fixtures.ui_fixtures import *  # noqa: F403, F401

# Register step definition plugins
# test_shared_steps contains steps used across multiple feature files
pytest_plugins = ["tests.steps.test_auth_steps", "tests.steps.test_navigation_steps", "tests.steps.test_shared_steps"]
