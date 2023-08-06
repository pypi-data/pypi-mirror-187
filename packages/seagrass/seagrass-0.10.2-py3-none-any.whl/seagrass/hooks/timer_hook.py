# A hook that measures the amount of time spent in various events.

import logging
import time
import seagrass._typing as t
from collections import defaultdict
from seagrass.base import ProtoHook
from ._utils import HookContext


class TimerHook(ProtoHook[float]):

    # Relatively high prehook/posthook priority so that TimerHook gets
    # called soon before and after a wrapped function.
    priority: int = 8

    event_times: t.DefaultDict[str, float]

    def __init__(self) -> None:
        self.event_times = defaultdict(float)

    def prehook(
        self, event_name: str, args: t.Tuple[t.Any, ...], kwargs: t.Dict[str, t.Any]
    ) -> float:
        # Return the current time so that it can be used by posthook()
        return time.time()

    def posthook(self, event_name: str, result: t.Any, context: float) -> None:
        # The context stores the time when the prehook was called. We can calculate the
        # total time spent in the event as roughly (not accounting for other hooks) equal
        # to the current time minus the time returned by prehook().
        current_time = time.time()
        self.event_times[event_name] += current_time - context

    def reset(self) -> None:
        self.event_times.clear()

    def log_results(self, logger: logging.Logger) -> None:
        for event in sorted(self.event_times):
            hook_ctx = {"event": event, "time": self.event_times[event]}
            with HookContext("TimerHook", hook_ctx):
                logger.info("TimerHook results")
