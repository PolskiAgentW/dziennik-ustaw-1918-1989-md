"""Rewrite the stats section of README.md from index.csv."""
import csv
import datetime as dt
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(open("index.csv", encoding="utf-8")))
ok = [r for r in rows if r["status"] == "ok"]
years = sorted({r["year"] for r in rows})
lines = [f"Stan na {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC "
         f"(liczone z `index.csv`).", "",
         "| rok | aktów w indeksie | przekonwertowanych | błędów |", "|---|---:|---:|---:|"]
for y in years:
    ry = [r for r in rows if r["year"] == y]
    lines.append(f"| {y} | {len(ry)} | {sum(r['status'] == 'ok' for r in ry)} | "
                 f"{sum(r['status'] != 'ok' for r in ry)} |")
nt = [r for r in ok if int(r.get("no_text_pages") or 0) > 0]
ocr = [r for r in ok if int(r.get("ocr_pages") or 0) > 0]
lines += ["", f"Akty ze stronami bez warstwy tekstowej (skany, grafiki): {len(nt)}, "
              f"razem {sum(int(r['no_text_pages']) for r in nt)} z {sum(int(r['pages'] or 0) for r in ok)} stron. "
              f"Tekst z OCR (oznaczony) ma {sum(int(r['ocr_pages']) for r in ocr)} z nich w {len(ocr)} aktach; "
              f"treści pozostałych brak.",
          f"Akty ze stronami z dużymi obrazami (wzory, rysunki; ich treści brak): "
          f"{sum(int(r.get('image_pages') or 0) > 0 for r in ok)}."]
types = Counter(r["type"] for r in ok)
lines += ["", "Rodzaje aktów: " + ", ".join(f"{t} {n}" for t, n in types.most_common()) + "."]
conv = Counter(r["converter"] for r in ok)
lines += ["Wersje konwertera: " + ", ".join(f"{c} ({n})" for c, n in conv.most_common()) + "."]
readme = Path("README.md").read_text(encoding="utf-8")
a, b = "<!-- stats:start -->", "<!-- stats:end -->"
i, j = readme.index(a) + len(a), readme.index(b)
Path("README.md").write_text(readme[:i] + "\n" + "\n".join(lines) + "\n" + readme[j:], encoding="utf-8")
