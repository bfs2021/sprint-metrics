"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

from pathlib import Path

from opentelemetry._logs import SeverityNumber
from opentelemetry.sdk._logs._internal import LogRecord

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
    lines = []
    lines.append(f"logger={id(logger)} type={type(logger)}")
    record = LogRecord(
        timestamp=0,
        observed_timestamp=None,
        severity_number=SeverityNumber.ERROR,
        severity_text="ERROR",
        body="frobnicated",
        event_name=None,
        attributes={},
    )
    try:
        logger.emit(record)
        lines.append("emit: ok")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"emit raised {exc!r}")
    lines.append(f"immediately={len(exporter.get_finished_logs())}")
    try:
        logger.flush()
        lines.append("flush: ok")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"flush raised {exc!r}")
    lines.append(f"after_flush={len(exporter.get_finished_logs())}")
    import time

    time.sleep(0.5)
    lines.append(f"after_sleep={len(exporter.get_finished_logs())}")
    (Path("tests/_dbg_out.txt")).write_text("\n".join(lines))
    assert True
