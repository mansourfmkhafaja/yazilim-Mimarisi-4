"""Source gerçekleştirmeleri."""
from .cekirdek import Emitter, Source


class FileLineSource(Source[str]):
    """Bir dosyayı okur ve her satır için bir String yayar."""

    def __init__(self, dosya_yolu: str):
        self.dosya_yolu = dosya_yolu

    def produce(self, out: Emitter[str]) -> None:
        with open(self.dosya_yolu, encoding="utf-8") as dosya:
            for satir in dosya:
                out.emit(satir.rstrip("\r\n"))
