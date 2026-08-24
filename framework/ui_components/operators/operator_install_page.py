import logging

from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from framework.config.config import Config
from framework.locators.operators import (
    InstalledOperatorsLocators,
    InstallOperatorLocators,
    OperatorSidePanelLocators,
    SoftwareCatalogLocators,
)
from framework.ui_components.base_page import BasePage


class OperatorInstallPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)
        self.catalog = SoftwareCatalogLocators()
        self.panel = OperatorSidePanelLocators()
        self.subscribe = InstallOperatorLocators()
        self.installed = InstalledOperatorsLocators()
        self.logger = logging.getLogger(__name__)

    async def navigate_to_software_catalog(self) -> bool:
        await self.page.goto(f"{self.config.base_url}/catalog/ns/default")
        await self.page.wait_for_load_state("networkidle")
        return True

    async def search_operator(self, keyword: str) -> bool:
        return await self.fill_input(self.catalog.KEYWORD_FILTER, keyword)

    async def is_operator_installed(self) -> bool:
        try:
            card = self.page.locator(self.catalog.OSP_CARD)
            await card.wait_for(state="visible", timeout=15000)
            badge = card.locator(self.catalog.INSTALLED_BADGE)
            await badge.wait_for(state="visible", timeout=3000)
            return True
        except PlaywrightTimeoutError:
            return False

    async def click_operator_card(self) -> bool:
        return await self.click_element(self.catalog.OSP_CARD)

    async def click_install_on_panel(self) -> bool:
        await self.is_visible(self.panel.INSTALL_BUTTON)
        return await self.click_element(self.panel.INSTALL_BUTTON)

    async def click_install_on_subscribe_page(self) -> bool:
        await self.wait_for_url_to_contain("operatorhub/subscribe")
        await self.is_visible(self.subscribe.HEADING)
        return await self.click_element(self.subscribe.INSTALL_BUTTON)

    async def navigate_to_installed_operators(self) -> bool:
        await self.page.goto(f"{self.config.base_url}/k8s/all-namespaces/operators.coreos.com~v1alpha1~ClusterServiceVersion")
        await self.page.wait_for_load_state("networkidle")
        return True

    async def verify_operator_installed(self, timeout: int = 300000) -> bool:
        await self.is_visible(self.installed.OSP_OPERATOR_LINK, timeout=timeout)
        return await self.is_visible(self.installed.STATUS_SUCCEEDED, timeout=30000)

    async def install_operator(self) -> bool:
        self.logger.info("Checking if OpenShift Pipelines operator is installed...")
        await self.navigate_to_software_catalog()
        await self.search_operator("Red Hat OpenShift Pipelines")

        if await self.is_operator_installed():
            self.logger.info("OpenShift Pipelines operator already installed, verifying...")
        else:
            self.logger.info("OpenShift Pipelines operator not installed, installing...")
            await self.click_operator_card()
            await self.click_install_on_panel()

            already_subscribed = await self.is_visible(
                self.subscribe.ALREADY_SUBSCRIBED_ALERT, timeout=5000
            )
            if already_subscribed:
                self.logger.info("Subscription already exists, skipping install click.")
            else:
                await self.click_install_on_subscribe_page()

        await self.navigate_to_installed_operators()
        assert await self.verify_operator_installed(), (
            "OpenShift Pipelines operator did not reach 'Succeeded' status"
        )
        self.logger.info("OpenShift Pipelines operator verified in Installed Operators.")
        return True
