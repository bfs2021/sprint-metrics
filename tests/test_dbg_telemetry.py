"""Temporary diagnostic for log export behaviour (delete me)."""

from __future__ import annotations


class _InMemoryLogExporter:
    def __init__(self):
        self._logs = []

    def export(self, logs):
        print(f"DBG export called len={len(list(logs))}", flush=True)
        self._logs.extend(logs)

    def flush(self):
        pass

    def shutdown(self):
        pass

    def get_finished_logs(self):
        return list(self._logs)


def test_dbg_log_export(monkeypatch):
    from opentelemetry._logs import SeverityNumber
    from opentelemetry.sdk._logs._internal import LogRecord

    from sprint_metrics.telemetry import get_logger, init_telemetry

    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4317")
    exporter = _InMemoryLogExporter()
    init_telemetry(log_exporter=exporter)
    logger = get_logger()
    import sys

    print(f"DBG logger={id(logger)} type={type(logger)}", file=sys.stderr)
    print(f"DBG logger provider={getattr(logger, '_logger', None) and id(getattr(logger, '_logger', None))}", file=sys.stderr)
    try:
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
    except Exception as exc:  # noqa: BLE001
        print(f"DBG emit raised {exc!r}", file=sys.stderr)
    import time

    time.sleep(0.2)
    print(f"DBG finished={len(exporter.get_finished_logs())}", file=sys.stderr)
    assert len(exporter.get_finished_logs()) >= 1
