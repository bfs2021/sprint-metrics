"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

import inspect
from pathlib import Path

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs._internal import _LoggerConfig

from sprint_metrics.telemetry import get_logger, init_telemetry


class _InMemoryLogExporter:
    def __init__(self):
        self._logs = []

    def export(self, logs):
        self._logs.extend(logs)

    def flush(self):
        pass

    def shutdown(self):
        pass

    def get_finished_logs(self):
        return list(self._logs)


def test_dbg(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4317")
    exporter = _InMemoryLogExporter()
    init_telemetry(log_exporter=exporter)
    logger = get_logger()
    lines = [f"logger={id(logger)}"]
    lines.append(f"_logger_config={vars(logger._logger_config)}")
    lines.append("=== get_logger source ===")
    try:
        lines.append(inspect.getsource(LoggerProvider.get_logger))
    except Exception as exc:  # noqa: BLE001
        lines.append(f"err {exc!r}")
    lines.append("=== _LoggerConfig source ===")
    try:
        lines.append(inspect.getsource(_LoggerConfig))
    except Exception as exc:  # noqa: BLE001
        lines.append(f"err {exc!r}")
    lines.append(f"Logger MRO: {[c.__name__ for c in type(logger).__mro__]}")
    Path("tests/_dbg_out.txt").write_text("\n".join(lines))
    assert True
