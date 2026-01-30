"""
Centralized locators file for all UI components.
All locators are organized by page/component for easy maintenance and updates.
"""


class LoginPageLocators:
    """Locators for the OpenShift Login Page"""

    LOGIN_WITH_AUTH = "div.pf-v6-c-login__main-body"
    KUBE_ADMIN_AUTH_LINK = 'a:has-text("kube:admin")'
    HTPASSWD_AUTH_LINK = 'a:has-text("htpasswd")'
    USERNAME_INPUT = '[id="inputUsername"]'
    PASSWORD_INPUT = '[id="inputPassword"]'
    LOGIN_BUTTON = 'button:has-text("Log in")'
    # Alternative locator if needed:
    # LOGIN_BUTTON = "button[id='co-login-button']"


class LeftNavigationBarLocators:
    """Locators for the Left Navigation Bar"""

    PIPELINES_BUTTON = '[data-test="nav-pipelines"]'
    KUBE_ADMIN_MENU = 'button[aria-label="User menu"]'
    # Links under Pipelines button/menu
    NAV_OVERVIEW_LINK = 'a[href="/pipelines-overview/all-namespaces"]'
    NAV_PIPELINES_LINK = 'a:has-text("Pipelines")'
    NAV_TASKS_LINK = 'a:has-text("Tasks")'
    NAV_TRIGGERS_LINK = 'a:has-text("Triggers")'


class PipelinesPageLocators:
    """Locators for the Pipelines Page"""

    PIPELINES_HEADER = 'h1:has-text("Pipelines")'
    # Tabs on Pipelines page
    PIPELINES_TAB = 'a[href="/pipelines/all-namespaces/'
    PIPELINE_RUNS_TAB = 'a[href="/pipelines/all-namespaces/pipeline-runs"]'
    REPOSITORIES_TAB = 'a[href="/pipelines/all-namespaces/repositories"]'
    PIPELINES_DATA_LOAD_CHECK = "table.ReactVirtualized__VirtualGrid"
    PIPELINES_NO_DATA_LOAD_CHECK = "#no-resource-msg"


class OverViewPageLocators:
    """Locators for the Overview Page"""

    OVERVIEW_HEADER = 'h1:has-text("Overview")'
    SKIP_TOUR_BUTTON = 'button:has-text("Skip tour")'


class PipelinesOverViewPageLocators:
    """Locators for the Pipelines Overview Page"""

    OVERVIEW_HEADER = 'h2:has-text("Overview")'


class TasksPageLocators:
    """Locators for the Tasks Page"""

    TASKS_HEADER = 'h1:has-text("Tasks")'
    # Tabs on Tasks page
    TASKS_TAB = 'a[href="/tasks/all-namespaces/'
    TASK_RUNS_TAB = 'a[href="/tasks/all-namespaces/task-runs"]'
    TASKS_DATA_LOAD_CHECK = "table.ReactVirtualized__VirtualGrid"
    TASKS_NO_DATA_LOAD_CHECK = "#no-resource-msg"


class TriggersPageLocators:
    """Locators for the Triggers Page"""

    TRIGGERS_HEADER = 'h1:has-text("Triggers")'
    # Tabs on Triggers page
    EVENT_LISTENERS_TAB = 'a[href="/triggers/all-namespaces/'
    TRIGGER_TEMPLATES_TAB = 'a[href="/triggers/all-namespaces/trigger-templates"]'
    TRIGGER_BINDINGS_TAB = 'a[href="/triggers/all-namespaces/trigger-bindings"]'
    CLUSTER_TRIGGER_BINDINGS_TAB = 'a[href="/triggers/all-namespaces/cluster-trigger-bindings"]'
    TRIGGERS_DATA_LOAD_CHECK = "table.ReactVirtualized__VirtualGrid"
    TRIGGERS_NO_DATA_LOAD_CHECK = "#no-resource-msg"
