"""Toplayıcı emitter (collecting emitter) test dublörü.

Aşamanın yaydığı tüm çıktıları bir listede toplar. Böylece aşama testleri
dosya sistemine dokunmadan yazılabilir. Her hafta yeniden kullanılacak.
"""
from logflow.cekirdek import Emitter


class ToplayiciEmitter(Emitter):
    def __init__(self):
        self.ogeler = []

    def emit(self, item) -> None:
        self.ogeler.append(item)
