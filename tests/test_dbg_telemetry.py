"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

import threading
from pathlib import Path
from opentelemetry.context import get_value
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor

g = SimpleLogRecordProcessor.on_emit.__globals__
key = g.get("_ON_EMIT_RECURSION_COUNT_KEY")
suppress = g.get("_SUPPRESS_INSTRUMENTATION_KEY")


def test_dbg():
    lines = [f"key={key!r} suppress={suppress!r}"]
    lines.append(f"main cnt={get_value(key) if key is not None else 'nokey'}")

    def read_on_thread():
        with open("tests/_dbg_thread.txt", "w") as f:
            f.write(f"child cnt={get_value(key) if key is not None else 'nokey'}")

    t = threading.Thread(target=read_on_thread)
    t.start()
    t.join()
    with open("tests/_dbg_thread.txt") as f:
        lines.append(f.read())
    Path("tests/_dbg_out.txt").write_text("\n".join(lines))
    assert True
