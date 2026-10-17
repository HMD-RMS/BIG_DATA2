"""Task 1: القراءة التقليدية (كل الملف في الذاكرة) -> OOM.
يعمل على Windows/Linux/Mac. لتجنب تجميد جهازك نستخدم "حارس ذاكرة":
نحمّل الملف تراكمياً في RAM، وعند بلوغ الحد (--limit-gb) نرمي MemoryError بأنفسنا.
هذا يحاكي ما يفعله pd.read_csv() العادي. استخدم --no-guard للتجربة الحقيقية (خطر!).
"""
import argparse

import pandas as pd
import psutil

from utils import DATA_FILE, VALUE_COL, Monitor, mem_mb, save_result, system_info

default_limit = round(psutil.virtual_memory().total / 1024**3 * 0.7, 1)
ap = argparse.ArgumentParser()
ap.add_argument("--limit-gb", type=float, default=default_limit,
                help=f"حد الذاكرة للحماية (الافتراضي 70%% من RAM = {default_limit} GB)")
ap.add_argument("--no-guard", action="store_true",
                help="قراءة عادية بدون حماية (قد يتجمد الجهاز!)")
args = ap.parse_args()

system_info()
print(f"RAM before: {mem_mb():.0f} MB")

status = "success"
m = Monitor()
try:
    with m:
        if args.no_guard:
            df = pd.read_csv(DATA_FILE)           # القراءة التقليدية الحقيقية
        else:
            print(f"Guard limit: {args.limit_gb} GB")
            chunks = []
            for i, chunk in enumerate(pd.read_csv(DATA_FILE, chunksize=500_000)):
                chunks.append(chunk)              # كل شيء يتراكم في الذاكرة
                if mem_mb() > args.limit_gb * 1024:
                    raise MemoryError(f"RAM exceeded {args.limit_gb} GB "
                                      f"after {(i + 1) * 500_000:,} rows")
            df = pd.concat(chunks)
        print("mean =", df[VALUE_COL].mean())
except MemoryError as e:
    status = "MemoryError"
    print(f"\nMemoryError: {e}")

if status == "success":
    print("\nالقراءة نجحت: ملفك أصغر من حد الذاكرة. ولّد ملفاً أكبر أو خفّض --limit-gb.")
print(f"Status: {status} | Peak RAM: {m.peak:.0f} MB | Time: {m.elapsed:.1f}s")
save_result("Standard Pandas", status=status, peak_mb=m.peak, time_s=m.elapsed)
