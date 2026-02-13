import os

import pytest

# Import fixtures from framework
from framework.fixtures.ui_fixtures import *  # noqa: F403, F401

# Register plugins to load step definitions
pytest_plugins = [
    "tests.steps.test_common_steps",
]


def pytest_collection_modifyitems(config, items):
    """
    Assign xdist_group by feature file so each feature file and its scenarios
    run on the same worker. Enables parallel execution with session-per-feature.
    """
    for item in items:
        func = getattr(item, "obj", None)
        if func is None:
            continue
        scenario = getattr(func, "__scenario__", None)
        if scenario is None:
            continue
        feature = getattr(scenario, "feature", None)
        if feature is None:
            continue
        filename = getattr(feature, "filename", None) or getattr(feature, "rel_filename", None)
        if filename:
            group_id = os.path.basename(filename)
            item.add_marker(pytest.mark.xdist_group(group_id))
