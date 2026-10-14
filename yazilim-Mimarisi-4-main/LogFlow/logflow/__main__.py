"""Main: sadece üç iş yapar — argümanları oku, hattı kur, run() çağır.

İş mantığı (business logic) burada YOK, bu hafta da sonra da.
"""
import sys

from .asamalar import ParserStage
from .havuzlar import ConsoleSink
from .kaynaklar import FileLineSource
from .pipeline import Pipeline


def main() -> None:
    # Türkçe karakterler (ı, ş, ğ) Windows konsolunda bozulmasın diye UTF-8 çıktı
    sys.stdout.reconfigure(encoding="utf-8")

    # 1) Komut satırı argümanlarını oku
    if len(sys.argv) != 2:
        print("Kullanım: python -m logflow <log-dosyası>")
        sys.exit(1)
    dosya_yolu = sys.argv[1]

    # 2) İşlem hattını kur
    hat = Pipeline(
        source=FileLineSource(dosya_yolu),
        stages=[ParserStage()],
        sink=ConsoleSink(),
    )

    # 3) Çalıştır
    hat.run()


if __name__ == "__main__":
    main()
