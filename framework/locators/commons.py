"""Locators for shared UI components (Login, Navigation, Actions, Favorites, Project Selector)."""


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
    NAV_OVERVIEW_LINK = 'a[href^="/pipelines-overview/ns/"]'
    NAV_PIPELINES_LINK = 'a:has-text("Pipelines")'
    NAV_TASKS_LINK = 'a:has-text("Tasks")'
    NAV_TRIGGERS_LINK = 'a:has-text("Triggers")'


class ActionsMenuLocators:
    """Locators for the Actions dropdown button (common across resource detail pages)."""

    ACTIONS_BUTTON = 'button:has-text("Actions")'


class ProjectSelectorLocators:
    """Locators for the Project Selector dropdown (common across pages)."""

    PROJECT_SELECTOR_BUTTON = 'button:has-text("Project:")'


class FavoritesLocators:
    """Locators for the Favorites button (common across pages)."""

    ADD_TO_FAVORITES_BUTTON = 'button[aria-label="Add to favorites"]'
