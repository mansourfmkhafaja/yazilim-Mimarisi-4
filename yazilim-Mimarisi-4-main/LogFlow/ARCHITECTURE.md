# LogFlow Mimarisi — v2

## Diyagram

```
+-----------------+  String  +---------------+  LogRecord  +---------------+
| FileLineSource  | -------> |  ParserStage  | ----------> |  ConsoleSink  |
| Source<String>  | Emitter  | Stage<String, | Emitter     | Sink<LogRecord>|
+-----------------+          |    LogRecord> |             +---------------+
                             +---------------+
                               hatalı satır: atla + say
```

## v1'den farklar

- Hat artık bir **alan modeli** (`LogRecord`) taşıyor, düz dizgi değil.
- `ParserStage` hattın ortasına eklendi; komşu aşamalar (`FileLineSource`) ve
  `Pipeline` **değişmedi**. Bu, bileşen/bağlayıcı ayrımının ilk somut kazancıdır.

## LogRecord ve genişleme noktası

`LogRecord` değişmezdir (`frozen dataclass`, `attributes` salt okunur `MappingProxyType`).
`attributes` eşlemi 5–7. haftaların dayanacağı genişleme noktasıdır: sonraki aşamalar,
bugünkü ayrıştırıcının bilmediği verileri kayda ekleyecektir. Kayıt biçimi bu yüzden
genişletmeye açık tutulmuştur.

## Sorumlulukların ayrılması

| Bileşen | Tek sorumluluğu |
|---|---|
| FileLineSource | Dosyadan satır okumak |
| ParserStage | Satırı LogRecord'a çevirmek |
| ConsoleSink | Kaydı göstermek |
| Pipeline | Bileşenleri bağlamak ve yaşam döngüsünü yönetmek |
