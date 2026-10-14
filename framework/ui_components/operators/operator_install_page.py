"""Page object for installing an operator via the OpenShift Console OperatorHub UI."""

import logging

from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from framework.config.config import Config
from framework.locators.operators import (
    InstallOperatorLocators,
    OperatorHubLocators,
    OperatorSidePanelLocators,
)
from framework.ui_components.base_page import BasePage

logger = logging.getLogger(__name__)


class OperatorInstallPage(BasePage):
    def __init__(self, page: Page, config: Config) -> None:
        super().__init__(page, config)

    async def navigate_to_operatorhub(self) -> bool:
        logger.info("[OSP UI] Navigating to OperatorHub...")
        await self.page.goto(f"{self.config.base_url}/operatorhub/all-namespaces")
        await self.page.wait_for_load_state("networkidle")
        return True

    async def search_operator(self, keyword: str = "Red Hat OpenShift Pipelines") -> bool:
        logger.info("[OSP UI] Searching for '%s'...", keyword)
        search_input = self.page.locator(OperatorHubLocators.KEYWORD_FILTER)
        try:
            await search_input.wait_for(state="visible", timeout=15000)
        except PlaywrightTimeoutError:
            search_input = self.page.locator(OperatorHubLocators.KEYWORD_FILTER_ALT)
            await search_input.wait_for(state="visible", timeout=10000)
        await search_input.fill(keyword)
        await self.page.wait_for_timeout(2000)
        return True

    async def is_operator_installed(self) -> bool:
        try:
            badge = self.page.locator(OperatorHubLocators.INSTALLED_BADGE)
            await badge.wait_for(state="visible", timeout=5000)
            logger.info("[OSP UI] Operator already has 'Installed' badge.")
            return True
        except PlaywrightTimeoutError:
            return False

    async def click_operator_card(self, catalog_source: str) -> bool:
        logger.info("[OSP UI] Clicking operator card (catalog=%s)...", catalog_source)
        card = self.page.locator(OperatorHubLocators.osp_card(catalog_source))
        try:
            await card.wait_for(state="visible", timeout=10000)
            await card.click()
        except PlaywrightTimeoutError:
            logger.info("[OSP UI] Primary card locator not found, using fallback...")
            card = self.page.locator(OperatorHubLocators.OSP_CARD_FALLBACK).first
            await card.click()
        await self.page.wait_for_timeout(1000)
        return True

    async def click_install_on_panel(self) -> bool:
        logger.info("[OSP UI] Clicking 'Install' on side panel...")
        btn = self.page.locator(OperatorSidePanelLocators.INSTALL_BUTTON)
        try:
            await btn.wait_for(state="visible", timeout=10000)
            await btn.click()
        except PlaywrightTimeoutError:
            btn = self.page.locator(OperatorSidePanelLocators.INSTALL_BUTTON_ALT).first
            await btn.click()
        return True

    async def _select_channel(self, channel: str) -> bool:
        dropdown = self.page.locator(InstallOperatorLocators.UPDATE_CHANNEL_DROPDOWN)
        try:
            await dropdown.wait_for(state="visible", timeout=5000)
            await dropdown.click()
            option = self.page.locator(InstallOperatorLocators.channel_option(channel))
            await option.wait_for(state="visible", timeout=5000)
            await option.click()
            logger.info("[OSP UI] Selected channel '%s'.", channel)
            return True
        except PlaywrightTimeoutError:
            logger.warning("[OSP UI] Could not select channel '%s', continuing with default.", channel)
            return False

    async def click_install_on_subscribe_page(self, channel: str | None = None) -> bool:
        logger.info("[OSP UI] Waiting for Install Operator page...")
        try:
            await self.page.wait_for_url("**/operatorhub/subscribe**", timeout=15000)
        except PlaywrightTimeoutError:
            logger.warning("[OSP UI] Did not reach subscribe page URL, attempting install anyway.")

        already_sub = self.page.locator(InstallOperatorLocators.ALREADY_SUBSCRIBED)
        try:
            await already_sub.wait_for(state="visible", timeout=3000)
            logger.info("[OSP UI] Operator already has an existing Subscription, skipping install click.")
            return True
        except PlaywrightTimeoutError:
            pass

        if channel:
            await self._select_channel(channel)

        logger.info("[OSP UI] Clicking 'Install' on subscribe page...")
        btn = self.page.locator(InstallOperatorLocators.INSTALL_BUTTON)
        try:
            await btn.wait_for(state="visible", timeout=10000)
            await btn.click()
        except PlaywrightTimeoutError:
            btn = self.page.locator(InstallOperatorLocators.INSTALL_BUTTON_ALT)
            await btn.click()
        return True

    async def install_operator(self, catalog_source: str, channel: str | None = None) -> bool:
        await self.navigate_to_operatorhub()
        await self.search_operator()

        if await self.is_operator_installed():
            logger.info("[OSP UI] Operator already installed in OperatorHub.")
            return True

        await self.click_operator_card(catalog_source)
        await self.click_install_on_panel()
        await self.click_install_on_subscribe_page(channel)
        logger.info("[OSP UI] Install triggered via UI.")
        return True
