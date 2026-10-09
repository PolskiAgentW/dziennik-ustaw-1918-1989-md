"""Convert the JSON Lines export (export.py) into one Parquet file for the Hugging Face dataset.

One row per act. The tree of units nests to any depth, so it is stored as a JSON string (`tree`).
Usage: python .github/to_parquet.py IN.jsonl.gz OUT.parquet   (needs pyarrow)
"""
import gzip
import json
import sys

import pyarrow as pa
import pyarrow.parquet as pq

INT = ("year", "pos", "pages", "words", "no_text_pages", "image_pages", "ocr_pages", "image_ocr_pages")
FIELDS = [  # (column, where to take it from: index.csv column or front matter key)
    ("eli", "eli"), ("year", "year"), ("pos", "pos"), ("type", "type"), ("title", "title"),
    ("display_address", "meta.display_address"), ("announcement_date", "announcement_date"),
    ("promulgation", "promulgation"), ("entry_into_force", "meta.entry_into_force"),
    ("legal_status", "meta.status_pl"), ("keywords", "meta.keywords"), ("change_date", "change_date"),
    ("source_pdf", "meta.source_pdf"), ("pdf_sha256", "pdf_sha256"), ("pages", "pages"), ("words", "words"),
    ("no_text_pages", "no_text_pages"), ("image_pages", "image_pages"), ("ocr_pages", "ocr_pages"),
    ("image_ocr_pages", "image_ocr_pages"),
    ("converter", "converter"), ("converted_at", "converted_at"),
]
SCHEMA = pa.schema([(c, pa.int32() if c in INT else pa.string()) for c, _ in FIELDS]
                   + [("markdown", pa.large_string()), ("tree", pa.large_string())])


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    cols = {f.name: [] for f in SCHEMA}
    for line in gzip.open(src, "rt", encoding="utf-8"):
        r = json.loads(line)
        for col, key in FIELDS:
            v = r["meta"].get(key[5:]) if key.startswith("meta.") else r.get(key)
            cols[col].append(v if v not in ("", None) else None)
        cols["markdown"].append(r["markdown"])
        cols["tree"].append(json.dumps(r["tree"], ensure_ascii=False) if r["tree"] is not None else None)
    table = pa.table(cols, schema=SCHEMA)
    pq.write_table(table, out, compression="zstd", row_group_size=500)
    print(f"{out}: {table.num_rows} rows")


if __name__ == "__main__":
    main()
