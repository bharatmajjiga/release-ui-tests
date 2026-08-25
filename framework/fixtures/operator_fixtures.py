"""Session-scoped fixture to ensure OpenShift Pipelines operator is installed via CLI."""

import asyncio
import logging

import pytest

from framework.cli.openshift_cli import OpenShiftCLI
from framework.config.config import Config

logger = logging.getLogger(__name__)

SUBSCRIPTION_YAML = """\
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-pipelines-operator
  namespace: openshift-operators
spec:
  channel: {channel}
  name: openshift-pipelines-operator-rh
  source: redhat-operators
  sourceNamespace: openshift-marketplace
"""


async def _is_osp_installed(cli: OpenShiftCLI) -> bool:
    exit_code, stdout, _ = await cli._run_command(
        [
            "oc",
            "get",
            "csv",
            "-n",
            "openshift-operators",
            "-o",
            "jsonpath={.items[?(@.spec.displayName=='Red Hat OpenShift Pipelines')].status.phase}",
        ],
        check=False,
    )
    return exit_code == 0 and "Succeeded" in stdout


async def _wait_for_csv(cli: OpenShiftCLI, timeout_seconds: int = 300, poll_interval: int = 15) -> bool:
    elapsed = 0
    while elapsed < timeout_seconds:
        if await _is_osp_installed(cli):
            return True
        logger.info(
            "Waiting for OpenShift Pipelines CSV to reach Succeeded... (%ds/%ds)",
            elapsed,
            timeout_seconds,
        )
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
    return False


async def _ensure_osp(cli: OpenShiftCLI, channel: str) -> None:
    if await _is_osp_installed(cli):
        logger.info("OpenShift Pipelines operator already installed and Succeeded.")
        return

    logger.info("OpenShift Pipelines operator not found, creating Subscription (channel=%s)...", channel)
    yaml_content = SUBSCRIPTION_YAML.format(channel=channel)
    success = await cli.apply_yaml(yaml_content)
    if not success:
        raise RuntimeError("Failed to apply OpenShift Pipelines Subscription YAML")

    logger.info("Subscription created. Waiting for CSV to reach Succeeded...")
    if not await _wait_for_csv(cli):
        raise RuntimeError("OpenShift Pipelines operator did not reach 'Succeeded' status within timeout")
    logger.info("OpenShift Pipelines operator installed and verified.")


@pytest.fixture(scope="session")
def ensure_osp_installed(
    openshift_cli: OpenShiftCLI,
    config: Config,
    playwright_event_loop: asyncio.AbstractEventLoop,
) -> None:
    from framework.cli.openshift_cli import derive_api_url_from_console_url
    from framework.fixtures.async_bridge import run_async

    async def _setup() -> None:
        api_url = derive_api_url_from_console_url(config.base_url)
        assert api_url, f"Could not derive API URL from {config.base_url}"
        assert await openshift_cli.login_with_credentials(
            api_url=api_url, username=config.username, password=config.password
        ), "CLI login failed"
        await _ensure_osp(openshift_cli, config.osp_channel)

    run_async(playwright_event_loop, _setup())
