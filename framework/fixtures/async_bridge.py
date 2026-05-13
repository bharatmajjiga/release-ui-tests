import asyncio
from typing import Any, Coroutine, TypeVar

T = TypeVar("T")


def run_async(loop: asyncio.AbstractEventLoop, coro: Coroutine[Any, Any, T]) -> T:
    """Run a Playwright async coroutine from a synchronous pytest-bdd step."""
    return loop.run_until_complete(coro)
