"""Task 2: Pandas Chunking (100,000 صف في كل مرة)."""
from collections import defaultdict

import pandas as pd

from utils import CAT_COL, DATA_FILE, VALUE_COL, Monitor, save_result, system_info

CHUNK = 100_000
system_info()

total_sum, total_count = 0.0, 0
group_sum = defaultdict(float)
group_cnt = defaultdict(int)

with Monitor() as m:
    for chunk in pd.read_csv(
        DATA_FILE,
        chunksize=CHUNK,
        usecols=[CAT_COL, VALUE_COL],
        dtype={CAT_COL: "category", VALUE_COL: "float32"},
    ):
        total_sum += chunk[VALUE_COL].sum()
        total_count += len(chunk)
        g = chunk.groupby(CAT_COL, observed=True)[VALUE_COL].agg(["sum", "count"])
        for cat, row in g.iterrows():
            group_sum[cat] += row["sum"]
            group_cnt[cat] += int(row["count"])

# المتوسط = المجموع الكلي / العدد الكلي (وليس متوسط المتوسطات)
global_mean = total_sum / total_count

print(f"\nGlobal mean : {global_mean:.4f}")
print(f"Total rows  : {total_count:,}")
for cat in sorted(group_sum):
    print(f"  {cat}: sum={group_sum[cat]:.2f}  mean={group_sum[cat] / group_cnt[cat]:.4f}")
print(f"Time: {m.elapsed:.1f}s | Peak RAM: {m.peak:.0f} MB")

save_result("Pandas Chunking", status="success", peak_mb=m.peak,
            time_s=m.elapsed, mean=float(global_mean), rows=total_count)
