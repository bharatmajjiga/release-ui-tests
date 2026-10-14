"""Locators for OperatorHub and Install Operator pages."""


class OperatorHubLocators:
    """Locators for the OperatorHub catalog page."""

    KEYWORD_FILTER = 'input[data-test="search-operatorhub"]'
    KEYWORD_FILTER_ALT = 'input[placeholder="Filter by keyword..."]'
    INSTALLED_BADGE = '[data-test="operator-installed-badge"]'
    OSP_CARD_FALLBACK = 'a:has-text("Red Hat OpenShift Pipelines")'

    @staticmethod
    def osp_card(catalog_source: str) -> str:
        return f'[data-test="openshift-pipelines-operator-rh-{catalog_source}-openshift-marketplace"]'


class OperatorSidePanelLocators:
    """Locators for the operator detail side panel."""

    INSTALL_BUTTON = '[data-test="operatorhub-install-btn"]'
    INSTALL_BUTTON_ALT = 'button:has-text("Install")'


class InstallOperatorLocators:
    """Locators for the Install Operator (subscribe) page."""

    INSTALL_BUTTON = '[data-test="install-operator-btn"]'
    INSTALL_BUTTON_ALT = 'button.pf-m-primary:has-text("Install")'
    ALREADY_SUBSCRIBED = "text=already exists"
    UPDATE_CHANNEL_DROPDOWN = 'button[data-test="dropdown-selectbox"]'

    @staticmethod
    def channel_option(channel: str) -> str:
        return f'[data-test="dropdown-menu-{channel}"]'


class InstalledOperatorsLocators:
    """Locators for the Installed Operators page."""

    OSP_LINK = 'a:has-text("Red Hat OpenShift Pipelines")'
    STATUS_SUCCEEDED = 'td:has-text("Succeeded")'
