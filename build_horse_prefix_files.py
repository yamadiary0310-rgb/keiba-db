import json
import re
import shutil
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent
SRC = BASE / "horses_all.jsonl"
OUT = BASE / "horses4"

if not SRC.exists():
    raise FileNotFoundError("horses_all.jsonl が見つかりません")

if OUT.exists():
    shutil.rmtree(OUT)

OUT.mkdir(exist_ok=True)

def safe_name(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s)

groups = defaultdict(dict)
count = 0

with SRC.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        horse = json.loads(line)
        name = horse.get("name")
        if not name:
            continue

        first = safe_name(name[0])
        prefix = safe_name(name[:4]) if len(name) >= 4 else name

        groups[(first, prefix)][name] = horse
        count += 1

for (first, prefix), horses in groups.items():
    folder = OUT / first
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f"{prefix}.json"
    with path.open("w", encoding="utf-8") as fw:
        json.dump(horses, fw, ensure_ascii=False, separators=(",", ":"))

manifest = {
    "format": "horse_prefix_json",
    "total_horses": count,
    "total_files": len(groups),
    "usage": "例: ダノンデサイル → horses/ダ/ダノ.json を取得し、その中の ダノンデサイル を読む"
}

with (BASE / "horses_manifest.json").open("w", encoding="utf-8") as fw:
    json.dump(manifest, fw, ensure_ascii=False, indent=2)

print("完了")
print("馬数:", count)
print("ファイル数:", len(groups))
print("例: horses/ダ/ダノ.json")