"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

import opentelemetry.sdk._logs._internal as _internal
import threading
from pathlib import Path
from opentelemetry.context import get_value


def test_dbg():
    # find the recursion-count contextvar key
    key = getattr(_internal, "_ON_EMIT_RECURSION_COUNT_KEY", None)
    lines = [f"key type={type(key)} name={getattr(key, 'name', None)}"]
    lines.append(f"main-thread cnt={get_value(key) if key is not None else 'nokey'}")

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
