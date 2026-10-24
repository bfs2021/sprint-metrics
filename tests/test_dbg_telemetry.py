"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

import inspect
from pathlib import Path

from opentelemetry._logs import SeverityNumber
from opentelemetry.sdk._logs import Logger
from opentelemetry.sdk._logs._internal import LogRecord
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor

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


def test_dbg_log_export(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4317")
    exporter = _InMemoryLogExporter()
    init_telemetry(log_exporter=exporter)
    logger = get_logger()
    lines = [f"logger={id(logger)} type={type(logger)}"]
    lines.append(f"logger attrs: {[(k, v) for k, v in vars(logger).items()]}")
    lines.append("=== Logger.emit source ===")
    try:
        lines.append(inspect.getsource(Logger.emit))
    except Exception as exc:  # noqa: BLE001
        lines.append(f"no emit source {exc!r}")
    lines.append("=== SimpleLogRecordProcessor source ===")
    try:
        lines.append(inspect.getsource(SimpleLogRecordProcessor))
    except Exception as exc:  # noqa: BLE001
        lines.append(f"no processor source {exc!r}")
    record = LogRecord(
        timestamp=0,
        observed_timestamp=None,
        severity_number=SeverityNumber.ERROR,
        severity_text="ERROR",
        body="frobnicated",
        event_name=None,
        attributes={},
    )
    logger.emit(record)
    lines.append(f"immediately={len(exporter.get_finished_logs())}")
    Path("tests/_dbg_out.txt").write_text("\n".join(lines))
    assert True
