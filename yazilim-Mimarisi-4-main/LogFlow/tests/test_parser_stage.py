"""ParserStage birim testleri.

Testler dosya okumaz: aşamayı oluşturur, ona bir dizgi verir ve
yaydığı çıktıları ToplayiciEmitter ile yakalar.
"""
import io
import unittest
from contextlib import redirect_stdout
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone

from logflow.asamalar import ParserStage
from tests.toplayici_emitter import ToplayiciEmitter

GECERLI_SATIR = (
    '192.168.1.5 - - [01/Oct/2026:09:15:30 +0300] '
    '"GET /index.html HTTP/1.1" 200 1234 "-" "curl/8.4.0"'
)


class ParserStageTestleri(unittest.TestCase):
    def setUp(self):
        self.parser = ParserStage()
        self.cikti = ToplayiciEmitter()

    def calistir(self, satir):
        self.parser.process(satir, self.cikti)
        return self.cikti.ogeler

    # 1) Geçerli satır
    def test_gecerli_satir(self):
        kayitlar = self.calistir(GECERLI_SATIR)
        self.assertEqual(len(kayitlar), 1)
        k = kayitlar[0]
        self.assertEqual(k.client_ip, "192.168.1.5")
        self.assertEqual(k.method, "GET")
        self.assertEqual(k.path, "/index.html")
        self.assertEqual(k.status, 200)
        self.assertEqual(k.bytes, 1234)
        self.assertEqual(k.user_agent, "curl/8.4.0")
        self.assertEqual(k.raw, GECERLI_SATIR)
        self.assertEqual(
            k.timestamp,
            datetime(2026, 10, 1, 9, 15, 30, tzinfo=timezone(timedelta(hours=3))),
        )
        self.assertEqual(self.parser.hatali_satir_sayisi, 0)

    # 2) Eksik alan (durum ve bayt yok)
    def test_eksik_alan(self):
        satir = '192.168.1.5 - - [01/Oct/2026:09:15:30 +0300] "GET / HTTP/1.1"'
        self.assertEqual(self.calistir(satir), [])
        self.assertEqual(self.parser.hatali_satir_sayisi, 1)

    # 3) Hatalı zaman damgası
    def test_hatali_zaman_damgasi(self):
        satir = '192.168.1.5 - - [99/Xyz/2026:25:61:00 +0300] "GET / HTTP/1.1" 200 10'
        self.assertEqual(self.calistir(satir), [])
        self.assertEqual(self.parser.hatali_satir_sayisi, 1)

    # 4) Hatalı durum kodu
    def test_hatali_durum_kodu(self):
        for durum in ("abc", "999", "42"):
            satir = f'192.168.1.5 - - [01/Oct/2026:09:15:30 +0300] "GET / HTTP/1.1" {durum} 10'
            self.calistir(satir)
        self.assertEqual(self.cikti.ogeler, [])
        self.assertEqual(self.parser.hatali_satir_sayisi, 3)

    # 5) Boş satır
    def test_bos_satir(self):
        self.calistir("")
        self.calistir("   ")
        self.assertEqual(self.cikti.ogeler, [])
        self.assertEqual(self.parser.hatali_satir_sayisi, 2)

    # 6) Fazladan boşluk
    def test_fazladan_bosluk(self):
        satir = ('   192.168.1.5   -  -   [01/Oct/2026:09:15:30 +0300]   '
                 '"GET   /index.html   HTTP/1.1"   200    1234   ')
        kayitlar = self.calistir(satir)
        self.assertEqual(len(kayitlar), 1)
        self.assertEqual(kayitlar[0].path, "/index.html")
        self.assertEqual(kayitlar[0].bytes, 1234)

    # 7) Boşluk içeren tırnaklı user agent
    def test_bosluklu_user_agent(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
        satir = ('10.0.0.1 - - [01/Oct/2026:09:15:30 +0300] '
                 f'"POST /login HTTP/1.1" 302 0 "-" "{ua}"')
        kayitlar = self.calistir(satir)
        self.assertEqual(len(kayitlar), 1)
        self.assertEqual(kayitlar[0].user_agent, ua)
        self.assertEqual(kayitlar[0].method, "POST")

    # 8) Sorgu dizesi (query string) içeren satır
    def test_sorgu_dizesi(self):
        satir = ('10.0.0.1 - - [01/Oct/2026:09:15:30 +0300] '
                 '"GET /api/orders?id=42&sort=desc HTTP/1.1" 200 512')
        kayitlar = self.calistir(satir)
        self.assertEqual(len(kayitlar), 1)
        self.assertEqual(kayitlar[0].path, "/api/orders?id=42&sort=desc")

    # Ek: bayt alanı "-" ise 0 kabul edilir
    def test_bayt_tire(self):
        satir = '10.0.0.1 - - [01/Oct/2026:09:15:30 +0300] "GET / HTTP/1.1" 304 -'
        self.assertEqual(self.calistir(satir)[0].bytes, 0)

    # Ek: bayt alanı sayı değilse satır hatalıdır
    def test_hatali_bayt(self):
        satir = '10.0.0.1 - - [01/Oct/2026:09:15:30 +0300] "GET / HTTP/1.1" 200 xyz'
        self.assertEqual(self.calistir(satir), [])
        self.assertEqual(self.parser.hatali_satir_sayisi, 1)

    # Ek: close() toplam hatalı satır sayısını yazdırır
    def test_close_toplami_yazdirir(self):
        self.calistir("bozuk")
        with redirect_stdout(io.StringIO()) as tampon:
            self.parser.close()
        self.assertIn("Hatalı satır sayısı: 1", tampon.getvalue())

    # Ek: LogRecord değişmez (immutable)
    def test_kayit_degismez(self):
        k = self.calistir(GECERLI_SATIR)[0]
        with self.assertRaises(FrozenInstanceError):
            k.status = 500
        with self.assertRaises(TypeError):
            k.attributes["yeni"] = "deger"


if __name__ == "__main__":
    unittest.main()
