"""Pipeline: kaynaktan (source) havuza (sink) kayıtları iten sıralı aşama listesi."""
from typing import List, Optional

from .cekirdek import Emitter, Sink, Source, Stage


class _SinkEmitter(Emitter):
    """Zincirin son halkası: gelen her öğeyi sink'e verir."""

    def __init__(self, sink: Sink):
        self._sink = sink

    def emit(self, item) -> None:
        self._sink.consume(item)


class _StageEmitter(Emitter):
    """Gelen öğeyi bir aşamadan geçirip sonucu bir sonraki emitter'a verir."""

    def __init__(self, stage: Stage, sonraki: Emitter):
        self._stage = stage
        self._sonraki = sonraki

    def emit(self, item) -> None:
        self._stage.process(item, self._sonraki)


class Pipeline:
    def __init__(self, source: Source, sink: Sink, stages: Optional[List[Stage]] = None):
        self.source = source
        self.sink = sink
        self.stages: List[Stage] = list(stages or [])

    def add_stage(self, stage: Stage) -> "Pipeline":
        """Hattın sonuna (sink'ten önce) yeni bir aşama ekler."""
        self.stages.append(stage)
        return self

    def run(self) -> None:
        # Emitter zincirini sondan başa doğru kur: stage1 -> stage2 -> ... -> sink
        zincir: Emitter = _SinkEmitter(self.sink)
        for stage in reversed(self.stages):
            zincir = _StageEmitter(stage, zincir)

        for stage in self.stages:
            stage.open()
        try:
            self.source.produce(zincir)
        finally:
            for stage in self.stages:
                stage.close()
