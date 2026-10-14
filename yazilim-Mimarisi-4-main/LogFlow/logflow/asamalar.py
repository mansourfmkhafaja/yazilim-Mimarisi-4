"""Stage gerçekleştirmeleri."""
import re
from datetime import datetime

from .cekirdek import Emitter, Stage
from .kayit import LogRecord

# Ortak Günlük Biçimi (CLF), isteğe bağlı referer ve user agent ile (Combined):
# host ident authuser [tarih] "METOT YOL PROTOKOL" durum bayt ["referer" "user-agent"]
CLF_DESENI = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<zaman>[^\]]+)\]\s+'
    r'"(?P<metot>[A-Z]+)\s+(?P<yol>\S+)(?:\s+\S+)?"\s+'
    r'(?P<durum>\S+)\s+'
    r'(?P<bayt>\S+)'
    r'(?:\s+"(?P<referer>[^"]*)"\s+"(?P<ua>[^"]*)")?$'
)
ZAMAN_BICIMI = "%d/%b/%Y:%H:%M:%S %z"


class ParserStage(Stage[str, LogRecord]):
    """Ham CLF satırını LogRecord nesnesine dönüştürür.

    Hatalı satırlar: bu hafta yalnızca ATLANIR ve SAYILIR.
    Doğru biçimde ele alınmaları 5. haftada gelecek (mimari katman katman inşa ediliyor).
    """

    def __init__(self):
        self.hatali_satir_sayisi = 0

    def process(self, input: str, out: Emitter[LogRecord]) -> None:
        kayit = self._ayristir(input)
        if kayit is None:
            self.hatali_satir_sayisi += 1
        else:
            out.emit(kayit)

    def close(self) -> None:
        print(f"Hatalı satır sayısı: {self.hatali_satir_sayisi}")

    def _ayristir(self, satir: str):
        eslesme = CLF_DESENI.match(satir.strip())
        if eslesme is None:
            return None
        try:
            zaman = datetime.strptime(eslesme["zaman"], ZAMAN_BICIMI)
        except ValueError:
            return None

        durum = eslesme["durum"]
        if not durum.isdigit() or not 100 <= int(durum) <= 599:
            return None

        bayt = eslesme["bayt"]
        if bayt == "-":
            bayt = "0"
        if not bayt.isdigit():
            return None

        return LogRecord(
            timestamp=zaman,
            client_ip=eslesme["ip"],
            method=eslesme["metot"],
            path=eslesme["yol"],
            status=int(durum),
            bytes=int(bayt),
            user_agent=eslesme["ua"] or "-",
            attributes={},
            raw=satir,
        )
