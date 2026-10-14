"""Sink gerçekleştirmeleri."""
from .cekirdek import Sink
from .kayit import LogRecord


class ConsoleSink(Sink[LogRecord]):
    """Bir LogRecord'u okunabilir, tek satırlık biçimde konsola yazdırır."""

    def consume(self, item: LogRecord) -> None:
        print(
            f"{item.timestamp:%Y-%m-%d %H:%M:%S} | {item.client_ip:<15} | "
            f"{item.method:<6} {item.status} | {item.bytes:>6} bayt | "
            f"{item.path} | {item.user_agent}"
        )
