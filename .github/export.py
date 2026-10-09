"""Write the whole data set as one gzipped JSON Lines file: one act per line.

Fields: the columns of index.csv (numbers as ints, empty as null), `meta` (the Markdown front matter),
`markdown` (the Markdown without front matter) and `tree` (the .json tree of units, null if missing).
Usage: python .github/export.py OUT.jsonl.gz
"""
import csv
import gzip
import json
import re
import sys
from pathlib import Path

INTS = {"year", "pos", "pages", "words", "no_text_pages", "image_pages", "ocr_pages", "image_ocr_pages"}
FRONT = re.compile(r"\A---\n(.*?)\n---\n+", re.S)


def front_matter(text: str) -> tuple[dict, str]:
    m = FRONT.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(": ")
        if sep:
            meta[key] = json.loads(value)  # the converter writes every value with json.dumps
    return meta, text[m.end():]


def main() -> None:
    out = Path(sys.argv[1])
    rows = [r for r in csv.DictReader(open("index.csv", encoding="utf-8")) if r["status"] == "ok"]
    n = 0
    with gzip.open(out, "wt", encoding="utf-8", compresslevel=9) as f:
        for r in sorted(rows, key=lambda r: (int(r["year"]), int(r["pos"]))):
            pub = r["eli"].split("/")[0]
            base = Path(pub) / r["year"] / f"{pub}-{r['year']}-{r['pos']}"
            md = base.with_suffix(".md")
            if not md.exists():
                continue
            meta, body = front_matter(md.read_text(encoding="utf-8"))
            tree = base.with_suffix(".json")
            rec = {k: (int(v) if k in INTS and v else v or None) for k, v in r.items()}
            rec.update(meta=meta, markdown=body,
                       tree=json.loads(tree.read_text(encoding="utf-8")) if tree.exists() else None)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"{out}: {n} of {len(rows)} acts")
    if n < len(rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
