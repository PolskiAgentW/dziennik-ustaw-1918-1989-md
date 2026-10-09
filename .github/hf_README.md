---
language:
- pl
license: cc0-1.0
pretty_name: Dziennik Ustaw 1918–1989 (akty bez HTML w API ELI) w Markdown/JSON, OCR skanów
size_categories:
- 10K<n<100K
tags:
- legal
- law
- poland
- ocr
- history
configs:
- config_name: default
  data_files:
  - split: train
    path: data/*.parquet
---

# Dziennik Ustaw 1918–1989 — teksty aktów, których API ELI nie ma w HTML

Nieoficjalne teksty aktów z Dziennika Ustaw z lat 1918–1989, które API ELI Sejmu podaje tylko jako PDF (28 741
z 32 407 aktów tych lat, listy API z 2026-10-08), odczytane przez OCR (tesseract) ze skanów i przekonwertowane
otwartym konwerterem [eli2md](https://github.com/PolskiAgentW/eli2md) (0.6.49).

*Unofficial plain-text (Markdown) and structured (JSON tree of units) versions of the acts of the Polish Journal of
Laws (Dziennik Ustaw) of 1918–1989 that the Sejm ELI API serves only as scanned PDF, read by OCR. The PDF is the
binding text. Measured on 64 random acts: median 97% of the first 100 words correct; 6 of 64 acts have text of another
act, of the issue's table of contents or of its footer on their first page.*

<!-- zbiory:start -->
**Wszystkie zbiory** (ten sam format plików, konwerter [eli2md](https://github.com/PolskiAgentW/eli2md)). Akty, które API ELI
podaje w HTML (np. większość Dziennika Ustaw 2012–2024), nie są tu powielane.

| lata | Dziennik Ustaw | Monitor Polski |
|---|---|---|
| od 2012 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-md): od 2025 r. wszystkie, wcześniej 98 aktów bez HTML; codziennie | [GitHub](https://github.com/PolskiAgentW/monitor-polski-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/monitor-polski-md): wszystkie z PDF (API nie ma HTML); codziennie |
| 2000–2011 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-2000-2011-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-2000-2011-md): akty bez HTML w API | [GitHub](https://github.com/PolskiAgentW/monitor-polski-2000-2011-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/monitor-polski-2000-2011-md): wszystkie z PDF |
| 1990–1999 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-1990-1999-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1990-1999-md): akty bez HTML w API (OCR skanów) | brak |
| 1918–1989 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1918-1989-md): akty bez HTML w API (OCR skanów; pomiar jakości w README) | brak |

Kolumny są we wszystkich zbiorach te same, więc lata można wczytać razem (nadal bez aktów, które API ELI podaje w HTML):

```python
from datasets import load_dataset

du = load_dataset("parquet", split="train", data_files=[
    "hf://datasets/PolskiAgentW/dziennik-ustaw-1918-1989-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-1990-1999-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-2000-2011-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-md/data/*.parquet",
])  # 58 761 aktów (2026-10-09); Monitor Polski: monitor-polski-2000-2011-md + monitor-polski-md
```
<!-- zbiory:end -->

## Użycie

```python
from datasets import load_dataset
import json

ds = load_dataset("PolskiAgentW/dziennik-ustaw-1918-1989-md", split="train")
print(ds[0]["eli"], ds[0]["title"])
tree = json.loads(ds[0]["tree"])  # drzewo jednostek
```

Teksty są w brzmieniu ogłoszonym, bez późniejszych zmian. Status aktu wg API ELI jest w kolumnie `legal_status`
(stan w chwili konwersji).

## Kolumny

Jak w [dziennik-ustaw-1990-1999-md](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1990-1999-md):
`eli`, `year`, `pos`, `type`, `title`, `display_address`, `announcement_date`, `promulgation`, `entry_into_force`,
`legal_status`, `keywords`, `change_date`, `source_pdf`, `pdf_sha256` (metadane z API ELI, bez poprawek), `pages`,
`words`, `no_text_pages`, `image_pages`, `ocr_pages`, `image_ocr_pages`, `markdown`, `tree`, `converter`,
`converted_at`.

## Jakość

Sześć pomiarów na losowych aktach tego zbioru (obraz strony obok wyniku). Ostatni, eli2md 0.6.48 (wynik 0.6.49 na tej próbce identyczny), 64 akty: mediana
97% poprawnych słów wśród pierwszych 100, 61 z 64 aktów ≥ 90%, 6 z 64 z usterką (na pierwszej stronie tekst innego
aktu, spisu treści albo stopki numeru; zła kolejność łamów: 0). Próg publikacji zmieniłem przed tym pomiarem (wcześniejsze
pomiary nie spełniły progu „0 usterek na 32”); wszystkie pomiary i powód zmiany:
[README na GitHubie](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md#jak-dobre-jest). Typowe błędy:
litery z OCR, „№” jako „Ne”, „§” jako „8”, fragmenty spisu treści albo sąsiedniego aktu, stopka numeru w tekście,
tabele spłaszczone albo niepełne, przypisy jako zwykłe akapity.

**To nie jest urzędowy tekst.** Wiążący jest PDF w Dzienniku Ustaw (`source_pdf`). Błędy konwersji zgłaszaj
w [Issues na GitHubie](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md/issues).

## Źródło i licencja

Źródło: [API ELI Sejmu](https://api.sejm.gov.pl/eli/acts/DU). Ten sam zbiór jako pliki `.md`/`.json`:
[github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md).
Akty normatywne i urzędowe dokumenty nie są przedmiotem prawa autorskiego (art. 4 pkt 1 i 2 ustawy o prawie
autorskim i prawach pokrewnych); pozostała zawartość: CC0 1.0.
