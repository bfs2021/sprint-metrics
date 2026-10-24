"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations

import threading

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


def test_dbg_log_export_on_thread(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4317")
    exporter = _InMemoryLogExporter()
    init_telemetry(log_exporter=exporter)
    logger = get_logger()
    lines = [f"logger={id(logger)}"]

    def emit_on_thread():
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
        except Exception as exc:  # noqa: BLE001
            lines.append(f"thread emit raised {exc!r}")

    t = threading.Thread(target=emit_on_thread)
    t.start()
    t.join()
    lines.append(f"after_thread={len(exporter.get_finished_logs())}")
    from pathlib import Path

    Path("tests/_dbg_out.txt").write_text("\n".join(lines))
    assert True
