"""Metadata of the acts in index.csv brought up to date with the API ELI without converting the text again: for each act
whose changeDate in the API year list differs from index.csv, the index.csv row fields from the list, in the .md the
front matter keys from the API metadata and the "# title" line, in the .json the "title" line. The PDF is not
downloaded (pdf_sha256, counts and converter stay those of the conversion). In dziennik-ustaw-md (--html-only) only the
acts with HTML in the API, the t.j. of 2012–2024: `eli2md.dataset` converts the others again. In the 1918–2011
datasets all acts: they have no conversion workflow, and the API corrects dates and titles of old acts (2026-10).

    python .github/meta_sync.py [--html-only] [--max N]   (in the repo root; one request at a time, 1 s apart)
"""
import json
import sys
import time
from pathlib import Path

from eli2md.dataset import API, _base_row, get, json_path, load_index, md_path, save_index
from eli2md.eli import clean_title
from eli2md.pdf import frontmatter

META_KEYS = ["title", "rank", "display_address", "internal_address", "announcement_date", "promulgation_date",
             "entry_into_force", "status_pl", "keywords"]


def update_files(md: Path, meta: dict) -> int:
    """Replace the META_KEYS lines of the front matter in place (a key the API no longer has is dropped, a new one goes
    after the key before it in META_KEYS), then the "# title" line and the .json "title" line. Returns changed values."""
    want = {}
    for line in frontmatter(meta).splitlines()[1:-1]:
        k, _, v = line.partition(": ")
        if k in META_KEYS:
            want[k] = v
    lines = md.read_text(encoding="utf-8").split("\n")
    end = lines.index("---", 1)
    fm = lines[1:end]
    have = {l.partition(": ")[0]: l.partition(": ")[2] for l in fm}
    changed = sum(have.get(k, "") != want.get(k, "") for k in META_KEYS)
    if not changed:
        return 0
    order = [l.partition(": ")[0] for l in fm]
    for k in META_KEYS:
        if k in want and k not in order:
            prev = [p for p in META_KEYS[:META_KEYS.index(k)] if p in order]
            order.insert(order.index(prev[-1]) + 1 if prev else 0, k)
    rest = iter(l for l in fm if l.partition(": ")[0] not in META_KEYS)
    out = ["---"] + [f"{k}: {want[k]}" if k in META_KEYS else next(rest) for k in order
                     if k not in META_KEYS or k in want]
    tail = lines[end:]
    old_title, new_title = json.loads(have["title"]), json.loads(want["title"])
    if new_title != old_title:
        h1 = next(i for i, l in enumerate(tail) if l.startswith("# "))
        if tail[h1] == "# " + old_title:
            tail[h1] = "# " + new_title
        js = json_path(md)
        if js.exists():
            text = js.read_text(encoding="utf-8")
            key = '"title": ' + json.dumps(old_title, ensure_ascii=False)
            if key in text.split("\n", 3)[2]:
                js.write_text(text.replace(key, '"title": ' + json.dumps(new_title, ensure_ascii=False), 1),
                              encoding="utf-8")
    md.write_text("\n".join(out + tail), encoding="utf-8")
    return changed


def main() -> int:
    limit = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 400
    html_only = "--html-only" in sys.argv
    root = Path(".")
    index = load_index(root)
    pub = next(iter(index)).split("/")[0]
    todo = []
    for year in sorted({int(r["year"]) for r in index.values()}):
        for it in json.loads(get(f"{API}/{pub}/{year}"))["items"]:
            row = index.get(it["ELI"])
            if row and (it.get("textHTML") or not html_only) and it.get("changeDate") != row["change_date"]:
                it["title"] = clean_title(it.get("title"))
                todo.append(it)
        time.sleep(1)
    print(f"acts{' with HTML' if html_only else ''} whose changeDate changed: {len(todo)} (max {limit})", flush=True)
    files = 0
    for it in todo[:limit]:
        meta = json.loads(get(f"{API}/{it['ELI']}"))
        meta["title"] = clean_title(meta.get("title"))
        time.sleep(1)
        row = index[it["ELI"]]
        row.update(_base_row(it))
        md = md_path(root, it["year"], it["pos"], pub)
        n = update_files(md, meta) if row["status"] == "ok" and md.exists() else 0
        files += n > 0
        print(f"{it['ELI']}: change_date {it['changeDate']}, {n} metadata values in .md", flush=True)
    save_index(root, index)
    print(f"done: {min(len(todo), limit)} rows, {files} .md changed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
