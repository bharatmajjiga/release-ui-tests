import logging

from pytest import Parser

logger = logging.getLogger(__name__)


def pytest_addoption(parser: Parser) -> None:
    """
    Registers CLI options used by fixtures (e.g. --headed, --ignore-ssl-errors).
    :param Parser parser: Pytest argument parser object
    :return: None
    """
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode (default: headless).",
    )
    parser.addoption(
        "--ignore-ssl-errors",
        action="store",
        type=lambda x: x.lower() in ("true", "1", "yes", "on"),
        default=True,
        help="Ignore SSL certificate errors (default: True). Set to false to disable.",
    )
