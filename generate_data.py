"""توليد ملف CSV اصطناعي بحجم محدد.
مثال:  python generate_data.py --gb 6
تجربة سريعة:  python generate_data.py --gb 0.2
"""
import argparse
import os

import numpy as np
import pandas as pd

from utils import DATA_FILE

parser = argparse.ArgumentParser()
parser.add_argument("--gb", type=float, default=0.2, help="الحجم المطلوب بالـ GB")
parser.add_argument("--out", default=DATA_FILE)
parser.add_argument("--rows", type=int, default=1_000_000, help="صفوف لكل دفعة")
args = parser.parse_args()

target = args.gb * 1024**3
if os.path.exists(args.out):
    os.remove(args.out)

i = 0
while not os.path.exists(args.out) or os.path.getsize(args.out) < target:
    n = args.rows
    df = pd.DataFrame({
        "id": np.arange(i * n, (i + 1) * n),
        "category": np.random.choice(list("ABCDE"), n),
        "value": np.random.rand(n) * 1000,
        "quantity": np.random.randint(1, 100, n),
    })
    df.to_csv(args.out, mode="w" if i == 0 else "a", header=(i == 0), index=False)
    i += 1
    size = os.path.getsize(args.out) / 1024**3
    print(f"\rbatch {i} | {size:.2f} GB / {args.gb} GB", end="", flush=True)

print(f"\nتم: {args.out}")
