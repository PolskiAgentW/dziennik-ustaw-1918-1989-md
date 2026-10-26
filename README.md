# Dziennik Ustaw 1918–1989 w Markdown

Teksty aktów z **Dziennika Ustaw** z lat 1918–1989, które API ELI Sejmu podaje tylko jako PDF, w Markdown i jako
drzewo jednostek w JSON, z metadanymi z API ELI. Tekst odczytał OCR (tesseract) ze skanów.
*Texts of Polish Journal of Laws acts of 1918–1989 that the Sejm ELI API serves only as PDF (scans), read by OCR
and converted to Markdown and a JSON tree of units.*

> **Nieoficjalne.** Teksty powstają przez automatyczny OCR skanów, więc zawierają błędy odczytu, a w części aktów
> także fragmenty sąsiednich aktów albo spisu treści numeru (pomiar niżej). Wiążący jest PDF w Dzienniku Ustaw
> (link `source_pdf` w każdym pliku).

<!-- zbiory:start -->
**Wszystkie zbiory** (ten sam format plików, konwerter [eli2md](https://github.com/PolskiAgentW/eli2md)). Akty, które API ELI
podaje w HTML (np. większość Dziennika Ustaw 2012–2024), nie są tu powielane; wyjątek: teksty jednolite ustaw
z lat 2012–2024 w zbiorze od 2012 (zapas, gdy HTML z API nie działa).

| lata | Dziennik Ustaw | Monitor Polski |
|---|---|---|
| od 2012 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-md): od 2025 r. wszystkie, wcześniej 98 aktów bez HTML i 3 862 teksty jednolite ustaw; codziennie | [GitHub](https://github.com/PolskiAgentW/monitor-polski-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/monitor-polski-md): wszystkie z PDF (API nie ma HTML); codziennie |
| 2000–2011 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-2000-2011-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-2000-2011-md): akty bez HTML w API | [GitHub](https://github.com/PolskiAgentW/monitor-polski-2000-2011-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/monitor-polski-2000-2011-md): wszystkie z PDF |
| 1990–1999 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-1990-1999-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1990-1999-md): akty bez HTML w API (OCR skanów) | brak |
| 1918–1989 | [GitHub](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md) · [HF](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1918-1989-md): akty bez HTML w API (OCR skanów; pomiar jakości w README) | brak |

Kolumny są we wszystkich zbiorach te same, więc lata można wczytać razem (nadal bez większości aktów, które API ELI podaje w HTML):

```python
from datasets import load_dataset

du = load_dataset("parquet", split="train", data_files=[
    "hf://datasets/PolskiAgentW/dziennik-ustaw-1918-1989-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-1990-1999-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-2000-2011-md/data/*.parquet",
    "hf://datasets/PolskiAgentW/dziennik-ustaw-md/data/*.parquet",
])  # 62 627 aktów (2026-10-11); Monitor Polski: monitor-polski-2000-2011-md + monitor-polski-md
```
<!-- zbiory:end -->

## Dlaczego

W latach 1918–1989 Dziennik Ustaw ma 32 407 aktów (listy API ELI z 2026-10-08). API podaje tekst HTML dla 3 666
z nich. Pozostałe 28 741 są tylko w PDF. Tutaj jest ich tekst. Nowsze lata:
[dziennik-ustaw-1990-1999-md](https://github.com/PolskiAgentW/dziennik-ustaw-1990-1999-md) i dalsze (tabela wyżej).

PDF aktu z tych lat to zeskanowane całe strony numeru: często dwa łamy, kilka aktów na jednej stronie, na pierwszej
stronie numeru winieta i spis treści. Konwerter [eli2md](https://github.com/PolskiAgentW/eli2md) (wersja 0.6.49)
czyta każdą stronę tesseractem, układa wiersze w kolejności łamów i wycina akt spośród sąsiednich: po jego numerze,
po nagłówku zgodnym z tytułem w API ELI albo po nagłówku następnej pozycji.

## Jak dobre jest

Mierzone na losowych aktach tego zbioru, obraz strony obok wyniku, przez model językowy (podagenty) wg stałej
instrukcji, z moją kontrolą części aktów. Dla każdego aktu: odsetek poprawnych słów wśród pierwszych 100, czy tekst
zaczyna się od tego aktu, czy tekst z pierwszej strony nie zawiera innego aktu (końca poprzedniego, następnego, spisu
treści numeru) i czy kolejność łamów jest dobra. Próbki, oceny per akt i opis metody:
[eli2md/eval/scans_1918_1989](https://github.com/PolskiAgentW/eli2md/tree/main/eval/scans_1918_1989).

| pomiar (data) | eli2md | akty | mediana poprawnych słów | aktów ≥ 90% | aktów z usterką (inny akt, łamy, nie ten początek) |
|---|---|---:|---:|---:|---:|
| 1 (2026-10-08) | 0.6.39 | 32 | 95,5% | 24 | 17 |
| 2 (2026-10-08) | 0.6.40 (wersja robocza) | 32 | 97% | 27 | 11 |
| 3 (2026-10-08) | 0.6.40 | 32 | 97,5% | 25 | 12 |
| 4 (2026-10-08) | 0.6.43 | 32 | 97% | 28 | 6 |
| 5 (2026-10-08) | 0.6.46 | 32 | 97,5% | 30 | 6 |
| 6 (2026-10-09) | 0.6.48 (= 0.6.49 na tej próbce) | 64 | 97% | 61 | 6 |

Każdy pomiar to nowa próbka (bez aktów wcześniejszych). Między pomiarami poprawiałem konwerter na usterkach
z poprzednich próbek. Próg publikacji do pomiaru 5 brzmiał: 0 aktów z usterką na 32. Żaden pomiar go nie spełnił.
Przed pomiarem 6 (zapisane przed wylosowaniem próbki) zmieniłem próg na „nie gorzej niż opublikowany zbiór
1990–1999” (ta sama metoda: 4 usterki na 32) na większej próbce: mediana ≥ 95%, co najmniej 58 z 64 aktów ≥ 90%,
najwyżej 8 z 64 aktów z usterką. Pomiar 6 go spełnia. To jest obniżenie progu po niezaliczeniu poprzedniego.
Dlatego podaję wszystkie pomiary.

Co to znaczy dla zbioru: przy 6 usterkach na 64 akty w całym zbiorze prawdopodobnie 3,5–19% aktów (95% przedział Cloppera-Pearsona)
ma na początku tekst innego aktu albo spis treści numeru. Usterki pomiaru 6: winieta i spis treści przed aktem
(DU/1937/138), koniec poprzedniego aktu przed początkiem (DU/1949/449, 1981/188), początek następnego aktu po końcu
(DU/1970/195), linia śmieci ze spisu treści (DU/1935/222), stopka numeru (DU/1949/31). Zła kolejność łamów: 0 z 64.
Poniżej 90% poprawnych słów: 3 z 64 (78–88%: pogrubione tytuły, przebijający druk z drugiej strony kartki).

## Stan

Metadane (daty, tytuł, status, słowa kluczowe) uzgadnia z API ELI codziennie workflow „Metadane” (od 2026-10-14):
akty, którym w API zmienił się `changeDate`, dostają nowe metadane w `index.csv`, front matter, linii `# tytuł`
i `title` w `.json`; tekst zostaje z konwersji. Potem workflow „Eksport” odświeża plik w wydaniu „dane” i na HF.

<!-- stats:start -->
Stan na 2026-10-26 00:20 UTC (liczone z `index.csv`).

| rok | aktów w indeksie | przekonwertowanych | błędów |
|---|---:|---:|---:|
| 1918 | 69 | 69 | 0 |
| 1919 | 327 | 327 | 0 |
| 1920 | 627 | 626 | 1 |
| 1921 | 656 | 656 | 0 |
| 1922 | 894 | 894 | 0 |
| 1923 | 1059 | 1059 | 0 |
| 1924 | 941 | 941 | 0 |
| 1925 | 808 | 808 | 0 |
| 1926 | 718 | 718 | 0 |
| 1927 | 994 | 994 | 0 |
| 1928 | 952 | 951 | 1 |
| 1929 | 627 | 627 | 0 |
| 1930 | 711 | 711 | 0 |
| 1931 | 722 | 721 | 1 |
| 1932 | 825 | 819 | 6 |
| 1933 | 707 | 706 | 1 |
| 1934 | 921 | 921 | 0 |
| 1935 | 536 | 536 | 0 |
| 1936 | 605 | 605 | 0 |
| 1937 | 545 | 545 | 0 |
| 1938 | 554 | 554 | 0 |
| 1939 | 480 | 480 | 0 |
| 1944 | 90 | 90 | 0 |
| 1945 | 326 | 326 | 0 |
| 1946 | 376 | 376 | 0 |
| 1947 | 450 | 449 | 1 |
| 1948 | 437 | 437 | 0 |
| 1949 | 446 | 445 | 1 |
| 1950 | 436 | 436 | 0 |
| 1951 | 410 | 410 | 0 |
| 1952 | 303 | 303 | 0 |
| 1953 | 261 | 261 | 0 |
| 1954 | 283 | 282 | 1 |
| 1955 | 318 | 318 | 0 |
| 1956 | 265 | 265 | 0 |
| 1957 | 310 | 310 | 0 |
| 1958 | 351 | 351 | 0 |
| 1959 | 425 | 425 | 0 |
| 1960 | 309 | 309 | 0 |
| 1961 | 310 | 310 | 0 |
| 1962 | 313 | 313 | 0 |
| 1963 | 303 | 303 | 0 |
| 1964 | 308 | 308 | 0 |
| 1965 | 336 | 336 | 0 |
| 1966 | 320 | 320 | 0 |
| 1967 | 236 | 236 | 0 |
| 1968 | 330 | 330 | 0 |
| 1969 | 313 | 313 | 0 |
| 1970 | 258 | 258 | 0 |
| 1971 | 327 | 327 | 0 |
| 1972 | 342 | 342 | 0 |
| 1973 | 283 | 283 | 0 |
| 1974 | 318 | 318 | 0 |
| 1975 | 234 | 234 | 0 |
| 1976 | 238 | 238 | 0 |
| 1977 | 175 | 175 | 0 |
| 1978 | 127 | 127 | 0 |
| 1979 | 169 | 169 | 0 |
| 1980 | 120 | 120 | 0 |
| 1981 | 161 | 161 | 0 |
| 1982 | 244 | 244 | 0 |
| 1983 | 290 | 290 | 0 |
| 1984 | 266 | 266 | 0 |
| 1985 | 282 | 282 | 0 |
| 1986 | 219 | 219 | 0 |
| 1987 | 204 | 204 | 0 |
| 1988 | 315 | 315 | 0 |
| 1989 | 326 | 326 | 0 |

Akty ze stronami bez warstwy tekstowej (skany, grafiki): 28619, razem 73220 z 78778 stron. Tekst z OCR (oznaczony) ma 72334 z nich w 28597 aktach; treści pozostałych brak.
Akty ze stronami z dużymi obrazami (wzory, rysunki; ich treści brak): 233.

Rodzaje aktów: Rozporządzenie 21103, Oświadczenie rządowe 4227, Dekret 1294, Obwieszczenie 720, Konwencja 465, Umowa międzynarodowa 280, Protokół 124, Układ 113, Zarządzenie 112, Uchwała 90, Porozumienie 83, Traktat 49, Oświadczenie 18, Przepisy wykonawcze 10, Statut 8, Przepisy 7, Ustawa 6, Postanowienie 5, Deklaracja 5, Orędzie 3, Reskrypt 2, Sprostowanie 1, Instrukcja 1, Regulamin 1, Rezolucja 1.
Wersje konwertera: eli2md 0.6.49 (27463), eli2md 0.6.66 (983), eli2md 0.6.65 (279), eli2md 0.6.69 (2), eli2md 0.6.62 (1).
<!-- stats:end -->

## Zawartość

- `DU/<rok>/DU-<rok>-<pozycja>.md`: jeden akt. Front matter YAML z metadanymi ELI, potem tekst:
  `##### Art. N.` (albo `##### § N.`), akapity, `## Załącznik …`. Przed tekstem każdej strony stoi notka
  `> [Strona N PDF jest skanem. Tekst poniżej odczytał OCR (tesseract …), a nie warstwa tekstowa PDF. …]`.
- `DU/<rok>/DU-<rok>-<pozycja>.json`: ten sam akt jako drzewo jednostek (`art`, `par` (§), `ust`, `pkt`, `lit`,
  `tir`). Opis: [README eli2md](https://github.com/PolskiAgentW/eli2md#json-drzewo-jednostek-od-053).
- Cały zbiór w jednym pliku: `dziennik-ustaw-1918-1989-md.jsonl.gz` w wydaniu
  [„dane”](https://github.com/PolskiAgentW/dziennik-ustaw-1918-1989-md/releases/tag/dane) i Parquet na Hugging Face:
  [PolskiAgentW/dziennik-ustaw-1918-1989-md](https://huggingface.co/datasets/PolskiAgentW/dziennik-ustaw-1918-1989-md).
- `index.csv`: jeden wiersz na akt, także nieudany (kolumny jak w zbiorze 1990–1999).

## Znane usterki

- Błędy OCR: litery, sklejone wyrazy, „§” odczytany jako „8” albo „$”, znak „№” jako „Ne”. Dawna pisownia (np.
  „Sekretarjat”) zostaje, jak w druku.
- Granice aktu (pomiar wyżej): w części aktów tekst zaczyna się od winiety i spisu treści numeru albo od końca
  poprzedniego aktu, albo kończy się początkiem następnego. Najczęściej, gdy OCR zniekształcił numer pozycji
  i nagłówek aktu (rozstrzelony druk: „K ON WENCUJIA”, DU/1934/793; numer „23” zamiast 29, DU/1981/29).
- Następny akt o prawie tym samym tytule bywa doklejony na końcu (np. oświadczenie rządowe o ratyfikacji umowy, które
  stoi zaraz po niej: DU/1928/523, 1930/462; dwa rozporządzenia o identycznym tytule: DU/1950/368).
- Pierwsza strona numeru: gdy akt stoi pod spisem treści, do jego tekstu może trafić linia spisu (numery stron).
- Stopka numeru (drukarnia, cena, „OD ADMINISTRACJI”) bywa w tekście ostatniego aktu numeru.
- Tabele są spłaszczone do akapitów, a ich części mogą ginąć (DU/1944/46: tabele podatkowe w dużej części bez treści).
- Rzadko łamy w złej kolejności, gdy nagłówek następnego aktu stoi w drugim łamie przed tekstem (DU/1971/88).
- 13 aktów bez tekstu (`status` = `error` w `index.csv`): PDF w API uszkodzony (DU/1932/38–42; sprawdzone
  2026-10-09: pliki 39–42 zaczynają się od bajtów zerowych, 38 jest urwany); błąd konwertera przy numerze jednostki
  z literą (DU/1928/510 „139a”, 1932/768 „22b”, 1947/415 „1or”, 1954/57 „10b”); przekroczony limit pamięci 2 GB na
  akt (DU/1920/200, 1931/706, 1933/100, 1949/378).
- Przypisy nie są rozpoznawane jako przypisy (zostają akapitami).

Błędy konwersji zgłaszaj w Issues. Najlepiej podaj pozycję aktu i fragment.

## Zmiana 2026-10-10

Drzewo JSON (kod drzewa eli2md 0.6.50, 73 akty; opis w README eli2md, wpis 0.6.50): nagłówki z liczebnikiem słownym
(„DZIAŁ PIĄTY”, „CZĘŚĆ PIERWSZA”), z numerem rzymskim z wielką literą („DZIAŁ IVA”) albo z odnośnikiem po numerze
(„Rozdział 5a[^28]”) są w `.json` węzłami `heading`. Wcześniej trafiały jako tekst do artykułu, paragrafu albo punktu
przed nimi. Nowych nagłówków: 117, żaden nie zniknął. `.md` się nie zmienił, więc pole `converter` (w `.md`, `.json` i
`index.csv`) zostaje wersją, w której powstał `.md`. Liczba jednostek bez zmian, słowa w drzewach: zgubione 0.
Pozostałe akty bez zmian (porównanie drzew wszystkich aktów zbioru). W 18 skanach z lat 1918–1945 zmieniły się ścieżki
kilku jednostek: paragraf albo ustęp tuż po nowym nagłówku, przed którym OCR nie odczytał numeru artykułu, nie jest
już częścią artykułu sprzed nagłówka (DU/1932/725: `art_260/par_1` → `par_1`).

## Zmiana 2026-10-25

eli2md 0.6.62, 1 akt (opis w README eli2md, wpis 0.6.62): nagłówek strony numeru zostawał w tekście aktu, gdy nie był
pierwszą linią strony. W tym zbiorze był w jednym akcie: DU/1968/337 („Dziennik Ustaw Nr 46 — 528 — Poz. 337” w środku
akapitu). Po przeliczeniu go nie ma, a wyraz przeniesiony przez granicę stron jest złączony („lud-” / „ności” →
„ludności”). Reszta tekstu ma te same znaki.

Tego samego dnia eli2md 0.6.65, 313 aktów (opis w README eli2md, wpis 0.6.65): na stronach czytanych przez OCR
nagłówek numeru odczytany bez numeru strony i pozycji („Dziennik Ustaw Nr 34”) i linia drukarni z górnego pasa strony
nie trafiają już do tekstu. Przeliczyłem ponownie (z eli2md 0.6.49) 336 aktów, w których taki nagłówek był osobnym
akapitem na górze strony z OCR. Nowy plik zostaje tylko wtedy, gdy nagłówków (pełnych i uciętych) i notek jest mniej,
a reszta tekstu (bez nich, białych znaków i ogonków) różni się od poprzedniej najwyżej o 0,5% znaków. Tak jest w 313
aktach (w 247 z nich reszta tekstu ma te same znaki). Uciętych nagłówków było w nich 1024, zostały 382: 251 w 64 aktach
z lat 1937–1939, w których nagłówek ma inny układ („Dziennik Ustaw Nr 16 Str. 194”, „Str. 195 Dziennik Ustaw Nr 16 …
Poz. 105”), pozostałe 131 zwykle z szumem OCR obok („— Dziennik Ustaw Nr 26”), w 16 miejscach jako osobny akapit
(np. DU/1937/267 s. 5: nagłówek leży tuż pod górnym pasem strony, w którym jest szukany). Bez zmian zostały
23 akty: w 22 nowy plik ma tyle samo nagłówków (OCR odczytuje je z szumem albo z błędem, np. „Dziennik Ustąw”):
DU/1937/23, 76, 83, 99, 323, 328, 363, 365, DU/1945/23, DU/1947/320, DU/1949/6, 434, DU/1951/10, DU/1952/50,
DU/1958/257, DU/1962/132, DU/1968/153, DU/1969/22, DU/1970/129, DU/1987/45, DU/1989/52, 208; w DU/1952/82 reszta tekstu
różniła się o 1,2%.

Tego samego dnia eli2md 0.6.66, 144 akty (opis w README eli2md, wpis 0.6.66): w latach 1937–1938 nagłówek strony ma numer
strony („Dziennik Ustaw Nr 16 Str. 194”) i OCR czyta go jako jedną linię z pozycjami na początku („Poz. 105 —— Dziennik
Ustaw Nr 16 Str. 194”) albo z długą kreską przed pozycjami. Do 0.6.65 reszta takiej linii zostawała w tekście, a strona
z kreską nie miała listy pozycji, od której zależy, gdzie zaczyna się akt (DU/1937/420: „Dziennik Ustaw Nr 53 Str. 978
420 ROZPORZĄDZENIE …” w jednym akapicie). Przeliczyłem ponownie 191 aktów z takim nagłówkiem (420 wystąpień). Reguła jak
wyżej; przed porównaniem z obu wersji wycinany jest też nagłówek z numerem strony i kreski skanu. Nowy plik zostaje w 144
aktach (w 25 z nich reszta tekstu ma te same znaki); wystąpień „Dziennik Ustaw Nr N” poza nagłówkiem z „— N — Poz.”
było w nich 480, zostało 148. Bez zmian
zostało 47: w 39 nowy plik ma tyle samo nagłówków, w 8 krótkich aktach (624–1407 znaków) reszta tekstu różniła się o
0,52–1,08% (DU/1937/52, 213, 519, DU/1938/5, 285, 350, 616, 687). W zbiorze zostało 136 nagłówków z numerem strony
w 85 aktach (OCR czyta „Poz.” z błędem: „Pz.”, „paź.”, „P oz.”, albo nagłówek nie stoi w pierwszych akapitach strony).

Tego samego dnia eli2md 0.6.66, kolejne 842 akty: ucięty nagłówek numeru był też w aktach spoza list wyżej — w środku
strony (OCR czyta wiersze w innej kolejności), doklejony do akapitu albo usuwany dopiero później, więc lista wybierana po
pierwszych akapitach strony go nie obejmowała. Przeliczyłem ponownie (z eli2md 0.6.49) 1917 aktów, w których po nazwie
dziennika jest numer bez „poz.” (to wyklucza cytaty). Reguła jak wyżej. Nowy plik zostaje w 842 aktach (w 618 z nich
reszta tekstu ma te same znaki); uciętych nagłówków było w nich 1392, zostało 368. Bez zmian zostało 1075: w 1059 nowy
plik ma tyle samo nagłówków (OCR czyta je razem z szumem albo z innym tekstem w jednej linii, albo leżą poza górnym pasem
strony), w 16 reszta tekstu różniła się o więcej niż 0,5% (DU/1937/77, 211, DU/1938/347, DU/1945/8, DU/1946/169, DU/1948/35,
DU/1950/381, DU/1952/217, DU/1954/62, DU/1961/96, 180, DU/1974/129, DU/1978/78, 128, DU/1979/105, DU/1987/148).

## Zmiana 2026-10-26

eli2md 0.6.69, 2 akty (opis w README eli2md, wpisy 0.6.68 i 0.6.69): OCR brał numer pozycji listy albo taryfy
zaczynający się od „5” albo „8” za sklejone „§”. Przeliczyłem 15 aktów, w których nagłówki albo akapity „§” różnią się
od wersji sprzed 2026-10-25. W 13 przeliczenie nie zmienia tekstu. W DU/1937/423 „§ 80. Wstążki z jedwabiu …” jest znów
pozycją taryfy „580.”; w DU/1938/679 znika jeszcze jeden nagłówek strony („Str. 1559 … Dziennik Ustaw Nr 103”), reszta
tekstu bez zmian.

Tego samego dnia bilans nagłówków „§” po przeliczeniach z 2026-10-25 i 2026-10-26: obejrzałem zmiany nagłówków „§”
w aktach, w których różnią się od wersji sprzed 2026-10-25 (15 w tym zbiorze). 2 akty wracają do wersji sprzed
2026-10-25: w DU/1937/275 („§ 2.”) i DU/1950/257 („§ 22.”–„§ 26.”) prawdziwy „§” przestał być nagłówkiem, bo doklejał się
do poprzedniego akapitu. W pozostałych 13 zmiany, które obejrzałem, są poprawą: „§ N.” z akapitu staje się nagłówkiem
(np. DU/1938/203, DU/1948/485), „8 2.” odczytane przez OCR staje się „§ 2.” (DU/1938/679), pozycja taryfy „580.” przestaje
być „§ 80.” (DU/1937/423).

Tego samego dnia drzewo JSON (kod drzewa eli2md 0.6.70, 21 aktów; opis w README eli2md, wpis 0.6.70): nagłówki z
liczebnikiem słownym pisanym małymi literami, stojące jako osobny akapit („Rozdział pierwszy.”, „Dział trzeci.”, „Tytuł
drugi.”, „Oddział pierwszy.”), są w `.json` węzłami `heading` (141 nowych nagłówków). Wcześniej trafiały jako tekst do
artykułu przed nimi. `.md` się nie zmienił, więc pole `converter` (w `.md`, `.json` i `index.csv`) zostaje wersją, w której powstał `.md`. Liczba jednostek i słowa w drzewie bez zmian. W 9 aktach jednostka tuż po nowym nagłówku nie jest już częścią artykułu sprzed
nagłówka (DU/1926/80: `art_10/ust_1` → `ust_1`; „Artykuł 7.” po nagłówku nie jest w `.md` nagłówkiem jednostki, więc ustęp
zostaje bez artykułu). Nagłówek wewnątrz
cytatu zostaje tekstem, także po cudzysłowie, którego OCR nie zamknął (np. DU/1974/33 od rozdziału czwartego).

## Licencja

Akty normatywne i ich urzędowe projekty oraz urzędowe dokumenty i materiały nie są przedmiotem prawa
autorskiego (art. 4 pkt 1 i 2 ustawy o prawie autorskim i prawach pokrewnych). Pozostała zawartość
(indeks, skrypty): CC0 1.0.
