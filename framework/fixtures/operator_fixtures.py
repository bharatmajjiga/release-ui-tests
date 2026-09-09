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


async def _inspect_subscription(cli: OpenShiftCLI) -> None:
    """Log Subscription state: currentCSV, installedCSV, state, conditions."""
    _, stdout, _ = await cli._run_command(
        [
            "oc", "get", "subscription", "openshift-pipelines-operator",
            "-n", "openshift-operators",
            "-o", "jsonpath={.status.currentCSV}|{.status.installedCSV}|{.status.state}",
        ],
        check=False,
    )
    parts = stdout.split("|") if stdout else []
    current_csv = parts[0] if len(parts) > 0 else "<none>"
    installed_csv = parts[1] if len(parts) > 1 else "<none>"
    state = parts[2] if len(parts) > 2 else "<none>"
    logger.info(
        "[OLM Diag] Subscription: currentCSV=%s installedCSV=%s state=%s",
        current_csv, installed_csv, state,
    )

    _, conds, _ = await cli._run_command(
        [
            "oc", "get", "subscription", "openshift-pipelines-operator",
            "-n", "openshift-operators",
            "-o", 'jsonpath={range .status.conditions[*]}{.type}={.status} ({.reason}: {.message}){"\\n"}{end}',
        ],
        check=False,
    )
    if conds and conds.strip():
        logger.info("[OLM Diag] Subscription conditions:\n%s", conds.strip())


async def _inspect_installplan(cli: OpenShiftCLI) -> None:
    """Log InstallPlan existence, approval, and phase."""
    _, stdout, _ = await cli._run_command(
        [
            "oc", "get", "installplan", "-n", "openshift-operators",
            "-o", 'jsonpath={range .items[*]}{.metadata.name} approved={.spec.approved} phase={.status.phase}{"\\n"}{end}',
        ],
        check=False,
    )
    if stdout and stdout.strip():
        logger.info("[OLM Diag] InstallPlans:\n%s", stdout.strip())
    else:
        logger.warning("[OLM Diag] No InstallPlans found in openshift-operators")


async def _inspect_csv(cli: OpenShiftCLI) -> None:
    """Log CSV phase and conditions for any pipelines-related CSV."""
    _, stdout, _ = await cli._run_command(
        [
            "oc", "get", "csv", "-n", "openshift-operators",
            "-o", "jsonpath={range .items[?(@.spec.displayName=='Red Hat OpenShift Pipelines')]}"
            '{.metadata.name} phase={.status.phase}{"\\n"}'
            '{range .status.conditions[*]}  {.type}={.status} ({.reason}: {.message}){"\\n"}{end}{end}',
        ],
        check=False,
    )
    if stdout and stdout.strip():
        logger.info("[OLM Diag] CSV status:\n%s", stdout.strip())
    else:
        logger.info("[OLM Diag] No OpenShift Pipelines CSV found yet")


async def _dump_olm_diagnostics(cli: OpenShiftCLI) -> None:
    """Dump comprehensive OLM state on timeout for debugging."""
    logger.error("[OLM Diag] ===== TIMEOUT - Dumping full OLM diagnostics =====")

    _, sub_yaml, _ = await cli._run_command(
        ["oc", "get", "subscription", "openshift-pipelines-operator", "-n", "openshift-operators", "-o", "yaml"],
        check=False,
    )
    logger.error("[OLM Diag] Subscription YAML:\n%s", sub_yaml or "<not found>")

    _, ip_yaml, _ = await cli._run_command(
        ["oc", "get", "installplan", "-n", "openshift-operators", "-o", "yaml"],
        check=False,
    )
    logger.error("[OLM Diag] InstallPlans YAML:\n%s", ip_yaml or "<not found>")

    _, csv_yaml, _ = await cli._run_command(
        ["oc", "get", "csv", "-n", "openshift-operators", "-o", "yaml"],
        check=False,
    )
    logger.error("[OLM Diag] CSVs YAML:\n%s", csv_yaml or "<not found>")

    _, og_yaml, _ = await cli._run_command(
        ["oc", "get", "operatorgroup", "-n", "openshift-operators", "-o", "yaml"],
        check=False,
    )
    logger.error("[OLM Diag] OperatorGroups YAML:\n%s", og_yaml or "<not found>")

    _, events, _ = await cli._run_command(
        [
            "oc", "get", "events", "-n", "openshift-operators",
            "--sort-by=.lastTimestamp", "--field-selector=type!=Normal",
        ],
        check=False,
    )
    logger.error("[OLM Diag] Warning/Error events in openshift-operators:\n%s", events or "<none>")

    _, cs_status, _ = await cli._run_command(
        [
            "oc", "get", "catalogsource", "redhat-operators", "-n", "openshift-marketplace",
            "-o", "jsonpath=state={.status.connectionState.lastObservedState} address={.status.connectionState.address}",
        ],
        check=False,
    )
    logger.error("[OLM Diag] CatalogSource redhat-operators: %s", cs_status or "<not found>")

    _, pkg, _ = await cli._run_command(
        [
            "oc", "get", "packagemanifest", "openshift-pipelines-operator-rh",
            "-o", "jsonpath=catalog={.status.catalogSource} channels={.status.channels[*].name}",
        ],
        check=False,
    )
    logger.error("[OLM Diag] PackageManifest: %s", pkg or "<not found>")

    _, olm_logs, _ = await cli._run_command(
        ["oc", "logs", "deploy/olm-operator", "-n", "openshift-operator-lifecycle-manager", "--tail=30"],
        check=False,
    )
    if olm_logs and olm_logs.strip():
        logger.error("[OLM Diag] OLM operator logs (last 30):\n%s", olm_logs.strip())

    _, cat_logs, _ = await cli._run_command(
        ["oc", "logs", "deploy/catalog-operator", "-n", "openshift-operator-lifecycle-manager", "--tail=30"],
        check=False,
    )
    if cat_logs and cat_logs.strip():
        logger.error("[OLM Diag] Catalog operator logs (last 30):\n%s", cat_logs.strip())

    logger.error("[OLM Diag] ===== END OLM diagnostics =====")


async def _wait_for_csv(cli: OpenShiftCLI, timeout_seconds: int = 300, poll_interval: int = 15) -> bool:
    elapsed = 0
    while elapsed < timeout_seconds:
        if await _is_osp_installed(cli):
            return True
        logger.info(
            "[OSP Setup] [2/5 Install] Waiting for CSV to reach Succeeded... (%ds/%ds)",
            elapsed,
            timeout_seconds,
        )
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
    return False


async def _is_console_plugin_enabled(cli: OpenShiftCLI) -> bool:
    exit_code, stdout, _ = await cli._run_command(
        ["oc", "get", "console.operator.openshift.io", "cluster", "-o", "jsonpath={.spec.plugins}"],
        check=False,
    )
    return exit_code == 0 and "pipelines-console-plugin" in stdout


async def _enable_console_plugin(cli: OpenShiftCLI, timeout_seconds: int = 60, poll_interval: int = 5) -> None:
    if await _is_console_plugin_enabled(cli):
        logger.info("[OSP Setup] [3/5 Console Plugin] Already enabled, skipping.")
        return

    elapsed = 0
    while elapsed < timeout_seconds:
        exit_code, _, _ = await cli._run_command(
            ["oc", "get", "consoleplugin", "pipelines-console-plugin"],
            check=False,
        )
        if exit_code == 0:
            break
        logger.info(
            "[OSP Setup] [3/5 Console Plugin] Waiting for consoleplugin resource to be created... (%ds/%ds)",
            elapsed,
            timeout_seconds,
        )
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    logger.info("[OSP Setup] [3/5 Console Plugin] Enabling pipelines-console-plugin...")
    exit_code, _, _ = await cli._run_command(
        [
            "oc",
            "patch",
            "console.operator.openshift.io",
            "cluster",
            "--type",
            "json",
            "-p",
            '[{"op":"add","path":"/spec/plugins/-","value":"pipelines-console-plugin"}]',
        ],
        check=False,
    )
    if exit_code != 0:
        await cli._run_command(
            [
                "oc",
                "patch",
                "console.operator.openshift.io",
                "cluster",
                "--type",
                "merge",
                "-p",
                '{"spec":{"plugins":["pipelines-console-plugin"]}}',
            ],
            check=True,
        )
    logger.info("[OSP Setup] [3/5 Console Plugin] Enabled successfully.")


async def _wait_for_tektonconfig(cli: OpenShiftCLI, timeout_seconds: int = 300, poll_interval: int = 15) -> bool:
    elapsed = 0
    while elapsed < timeout_seconds:
        exit_code, stdout, _ = await cli._run_command(
            ["oc", "get", "tektonconfig", "config", "-o", 'jsonpath={.status.conditions[?(@.type=="Ready")].status}'],
            check=False,
        )
        if exit_code == 0 and "True" in stdout:
            return True
        logger.info(
            "[OSP Setup] [4/5 TektonConfig] Waiting for Ready=True... (%ds/%ds)",
            elapsed,
            timeout_seconds,
        )
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
    return False


async def _wait_for_deployment_rollout(
    cli: OpenShiftCLI,
    deployment: str,
    namespace: str,
    timeout_seconds: int = 120,
    poll_interval: int = 10,
) -> bool:
    elapsed = 0
    while elapsed < timeout_seconds:
        exit_code, _, _ = await cli._run_command(
            ["oc", "rollout", "status", f"deployment/{deployment}", "-n", namespace, f"--timeout={poll_interval}s"],
            check=False,
        )
        if exit_code == 0:
            return True
        logger.info(
            "[OSP Setup] [5/5 Pod Readiness] Waiting for %s/%s rollout... (%ds/%ds)",
            namespace,
            deployment,
            elapsed,
            timeout_seconds,
        )
        elapsed += poll_interval
    return False


async def _ensure_osp(cli: OpenShiftCLI, channel: str) -> None:
    logger.info("[OSP Setup] ===== Starting OpenShift Pipelines operator setup =====")

    # Step 1: Check if operator is already installed
    logger.info("[OSP Setup] [1/5 Check] Checking if operator is already installed...")
    if await _is_osp_installed(cli):
        logger.info("[OSP Setup] [1/5 Check] Operator already installed with CSV Succeeded.")
    else:
        # Step 2: Install operator
        logger.info("[OSP Setup] [2/5 Install] Operator not found, creating Subscription (channel=%s)...", channel)
        yaml_content = SUBSCRIPTION_YAML.format(channel=channel)
        success = await cli.apply_yaml(yaml_content)
        if not success:
            raise RuntimeError("Failed to apply OpenShift Pipelines Subscription YAML")
        logger.info("[OSP Setup] [2/5 Install] Subscription created, waiting for CSV...")
        if not await _wait_for_csv(cli):
            raise RuntimeError("OpenShift Pipelines operator did not reach 'Succeeded' within timeout")
        logger.info("[OSP Setup] [2/5 Install] CSV reached Succeeded.")

    # Step 3: Enable console plugin
    logger.info("[OSP Setup] [3/5 Console Plugin] Checking console plugin status...")
    await _enable_console_plugin(cli)

    # Step 4: Wait for TektonConfig
    logger.info("[OSP Setup] [4/5 TektonConfig] Checking TektonConfig readiness...")
    if not await _wait_for_tektonconfig(cli):
        raise RuntimeError("TektonConfig did not reach Ready state within timeout")
    logger.info("[OSP Setup] [4/5 TektonConfig] Ready.")

    # Step 5: Wait for console pods
    logger.info("[OSP Setup] [5/5 Pod Readiness] Checking console deployments...")

    logger.info("[OSP Setup] [5/5 Pod Readiness] Waiting for openshift-console/console...")
    if not await _wait_for_deployment_rollout(cli, "console", "openshift-console"):
        raise RuntimeError("openshift-console deployment did not roll out within timeout")
    logger.info("[OSP Setup] [5/5 Pod Readiness] openshift-console/console is ready.")

    logger.info("[OSP Setup] [5/5 Pod Readiness] Waiting for openshift-pipelines/pipelines-console-plugin...")
    if not await _wait_for_deployment_rollout(cli, "pipelines-console-plugin", "openshift-pipelines"):
        raise RuntimeError("pipelines-console-plugin deployment did not roll out within timeout")
    logger.info("[OSP Setup] [5/5 Pod Readiness] openshift-pipelines/pipelines-console-plugin is ready.")

    logger.info("[OSP Setup] ===== OpenShift Pipelines operator setup complete =====")


@pytest.fixture(scope="session")
def ensure_osp_installed(
    openshift_cli: OpenShiftCLI,
    config: Config,
    playwright_event_loop: asyncio.AbstractEventLoop,
) -> None:
    from framework.cli.openshift_cli import derive_api_url_from_console_url
    from framework.fixtures.async_bridge import run_async

    async def _setup() -> None:
        import os

        logger.info("[OSP Setup] [0/5 Login] Checking CLI authentication...")

        # 1. Check if already logged in via existing KUBECONFIG (CI/Prow)
        if await openshift_cli.is_logged_in():
            logger.info("[OSP Setup] [0/5 Login] Already authenticated via existing KUBECONFIG.")
        else:
            # 2. Try API_URL env var if set (explicit override)
            api_url = os.getenv("API_URL")
            if api_url:
                logger.info("[OSP Setup] [0/5 Login] Using API_URL env var: %s", api_url)
            else:
                # 3. Derive from CONSOLE_URL
                api_url = derive_api_url_from_console_url(config.base_url)
                assert api_url, f"Could not derive API URL from {config.base_url}"
                logger.info("[OSP Setup] [0/5 Login] Derived API URL: %s", api_url)

            assert await openshift_cli.login_with_credentials(
                api_url=api_url, username=config.username, password=config.password
            ), f"CLI login failed against {api_url}"
            logger.info("[OSP Setup] [0/5 Login] Logged in successfully.")

        await _ensure_osp(openshift_cli, config.osp_channel)

    run_async(playwright_event_loop, _setup())
