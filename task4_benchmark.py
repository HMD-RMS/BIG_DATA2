"""Task 4: رسم المقارنة من results.json."""
import json

import matplotlib.pyplot as plt

with open("results.json") as f:
    res = json.load(f)

ok = {k: v for k, v in res.items() if v["status"] == "success"}
names = list(ok)
times = [ok[k]["time_s"] for k in names]
mems = [ok[k]["peak_mb"] for k in names]
colors = ["#e67e22", "#2ecc71", "#3498db"][: len(names)]

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].bar(names, times, color=colors); ax[0].set_title("Execution Time (s)")
ax[1].bar(names, mems, color=colors);  ax[1].set_title("Peak RAM (MB)")
plt.tight_layout()
plt.savefig("benchmark.png", dpi=150)
plt.show()

print(f"{'Method':<18}{'Status':<14}{'Peak RAM (MB)':>14}{'Time (s)':>10}")
for k, v in res.items():
    print(f"{k:<18}{v['status']:<14}{v['peak_mb']:>14.0f}{v['time_s']:>10.1f}")
