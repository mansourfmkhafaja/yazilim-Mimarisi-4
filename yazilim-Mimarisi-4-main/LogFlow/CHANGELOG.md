# Değişiklik Günlüğü (Change Log)

## v2 — Tipli Kayıtlar ve İlk Gerçek Filtre

**Yeni dosyalar**
- `logflow/kayit.py` — değişmez `LogRecord` (attributes genişleme noktası ile)
- `logflow/asamalar.py` — CLF için `ParserStage` (hatalı satırları atlar ve sayar)
- `tests/toplayici_emitter.py` — ToplayiciEmitter test dublörü
- `tests/test_parser_stage.py` — ParserStage için 12 birim testi
- `CHANGELOG.md`

**Değiştirilen dosyalar**
- `logflow/__main__.py` — hatta `ParserStage` eklendi; Türkçe karakterler için UTF-8 çıktı
- `logflow/havuzlar.py` — `ConsoleSink` artık `LogRecord`'u tek satırda yazdırıyor
- `README.md`, `ARCHITECTURE.md`, `logflow/__init__.py` — belgeler güncellendi

**Değişmeyen dosyalar**
- `logflow/cekirdek.py`, `logflow/pipeline.py`, `logflow/kaynaklar.py`

## v1 — İskelet İşlem Hattı

- Arayüzler (`Stage`, `Emitter`, `Source`, `Sink`), `FileLineSource`, `ConsoleSink`,
  `Pipeline`, `Main`, örnek günlük dosyası.
