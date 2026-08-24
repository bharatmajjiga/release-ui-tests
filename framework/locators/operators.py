"""Locators for Operator installation pages (Software Catalog, Install Operator, Installed Operators)."""


class SoftwareCatalogLocators:
    """Locators for the Software Catalog / OperatorHub page."""

    KEYWORD_FILTER = 'input[placeholder="Filter by keyword..."]'
    OSP_CARD = 'role=gridcell[name=/Red Hat OpenShift Pipelines/]'
    INSTALLED_BADGE = 'text=Installed'


class OperatorSidePanelLocators:
    """Locators for the operator detail side panel (modal dialog)."""

    INSTALL_BUTTON = 'button:has-text("Install")'
    CLOSE_BUTTON = 'button:has-text("Close")'


class InstallOperatorLocators:
    """Locators for the Install Operator subscription page."""

    HEADING = 'h1:has-text("Install Operator")'
    INSTALL_BUTTON = '.pf-v6-c-page__main-body button:has-text("Install")'
    ALREADY_SUBSCRIBED_ALERT = 'text=A Subscription for this Operator already exists'


class InstalledOperatorsLocators:
    """Locators for the Installed Operators list page."""

    OSP_OPERATOR_LINK = 'a:has-text("Red Hat OpenShift Pipelines")'
    STATUS_SUCCEEDED = 'text=Succeeded'
