# LogFlow — Artım 2: Tipli Kayıtlar ve İlk Gerçek Filtre (v2)

İşlem hattı artık düz dizgi (string) değil, bir **alan modeli** (`LogRecord`) taşıyor.
`ParserStage`, Ortak Günlük Biçimi (CLF) satırlarını ayrıştırır; hatalı satırlar
bu hafta yalnızca **atlanır ve sayılır** (doğru ele alınmaları 5. haftada gelecek).

## Çalıştırma

```
cd LogFlow
python -m logflow data/access-small.log
```

Çıktı: her kayıt tek satırda yazdırılır, en sonda `Hatalı satır sayısı: 6` görünür.

## Testler

```
cd LogFlow
python -m unittest -v
```

Testler Python'un yerleşik `unittest` modülüyle yazılmıştır (Java'daki JUnit 5'in karşılığı).
Aşama testleri dosya okumaz: `ParserStage` oluşturulur, ona bir dizgi verilir ve çıktılar
`tests/toplayici_emitter.py` içindeki **ToplayiciEmitter** (collecting emitter) test dublörü ile yakalanır.

ParserStage için 12 test: geçerli satır, eksik alan, hatalı zaman damgası, hatalı durum kodu,
boş satır, fazladan boşluk, boşluk içeren tırnaklı user agent, sorgu dizesi + 4 ek test.

## Satır kapsama (line coverage)

`coverage` aracı ile ölçülmüştür (`pip install coverage`):

```
python -m coverage run --source=logflow -m unittest
python -m coverage report
```

| Modül | Kapsama |
|---|---|
| `asamalar.py` (ParserStage) | **%100** |
| `kayit.py` (LogRecord) | %100 |
| `cekirdek.py` | %100 |
| `pipeline.py`, `kaynaklar.py`, `havuzlar.py`, `__main__.py` | %0 (henüz test yok) |
| **Toplam** | **%49** |

## Demo soruları

**Ayrıştırıcıyı eklemek için mevcut dosyalardan hangilerini değiştirdiniz?**
Yalnızca `__main__.py` (hatta yeni aşamayı eklemek için tek satır) ve `havuzlar.py`
(görev 3: ConsoleSink artık LogRecord yazdırıyor). `Pipeline`, `FileLineSource` ve
arayüzler **hiç değişmedi** — yeni aşama hattın ortasına takıldı.

**Ayrıştırıcı testiniz bir dosya okumuyor — bu nasıl mümkün ve neden önemli?**
`ParserStage` dosyayı bilmez; sadece bir dizgi alır ve bir `Emitter`'a yayar. Testte
gerçek emitter yerine `ToplayiciEmitter` verilir. Böylece testler hızlı, tekrarlanabilir
ve dosya sisteminden bağımsızdır; aşama tek başına (izole) test edilir.
