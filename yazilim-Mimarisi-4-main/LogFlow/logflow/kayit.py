"""Alan kaydı (domain record): LogRecord."""
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class LogRecord:
    """Değişmez (immutable) günlük kaydı.

    attributes eşlemi genişleme noktasıdır: sonraki haftalardaki aşamalar,
    bugünkü ayrıştırıcının hiçbir şey bilmediği verileri kayda ekleyecektir.
    Bu yüzden kayıt biçimi genişletmeye açık olmalıdır.
    """

    timestamp: datetime
    client_ip: str
    method: str
    path: str
    status: int
    bytes: int
    user_agent: str
    attributes: Mapping[str, str] = field(default_factory=dict)
    raw: str = ""

    def __post_init__(self):
        # attributes'u salt okunur hale getir (dışarıdan değiştirilemesin)
        object.__setattr__(self, "attributes", MappingProxyType(dict(self.attributes)))
