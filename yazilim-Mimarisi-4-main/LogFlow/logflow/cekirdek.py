"""LogFlow çekirdek arayüzleri.

Projenin temel kelime dağarcığı burada tanımlanır:
Emitter, Stage, Source, Sink ve StageException.
Arayüzler bilerek küçük tutulmuştur.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

I = TypeVar("I")  # Girdi tipi
O = TypeVar("O")  # Çıktı tipi
T = TypeVar("T")


class StageException(Exception):
    """Bir aşama (stage) işlem sırasında hata verdiğinde fırlatılır."""


class Emitter(ABC, Generic[T]):
    """Bir aşamanın ürettiği öğeleri bir sonraki adıma ileten bağlayıcı."""

    @abstractmethod
    def emit(self, item: T) -> None:
        ...


class Stage(ABC, Generic[I, O]):
    """İşlem hattındaki tek bir adım.

    process() bir değer döndürmez; çıktıları Emitter üzerinden yayar.
    Neden? Çünkü bir filtre her girdi için sıfır, bir veya birden çok
    çıktı üretebilir. Dönüş değeri bizi 1:1 ilişkiye zorlardı.
    """

    @abstractmethod
    def process(self, input: I, out: Emitter[O]) -> None:
        ...

    def open(self) -> None:
        """Yaşam döngüsü kancası (bu hafta kullanılmıyor)."""

    def close(self) -> None:
        """Yaşam döngüsü kancası (bu hafta kullanılmıyor)."""


class Source(ABC, Generic[O]):
    """İşlem hattının başı: kayıtları üretir."""

    @abstractmethod
    def produce(self, out: Emitter[O]) -> None:
        ...


class Sink(ABC, Generic[I]):
    """İşlem hattının sonu: kayıtları tüketir."""

    @abstractmethod
    def consume(self, item: I) -> None:
        ...
