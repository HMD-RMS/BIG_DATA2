"""Task 3: Dask DataFrame (Lazy + Parallel)."""
import dask
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

from utils import CAT_COL, DATA_FILE, VALUE_COL, Monitor, save_result, system_info


def main():
    system_info()

    # 1) التحميل: لا يقرأ شيئاً بعد، فقط يبني الأجزاء (partitions)
    ddf = dd.read_csv(
        DATA_FILE,
        blocksize="32MB",
        usecols=[CAT_COL, VALUE_COL],
        dtype={VALUE_COL: "float32"},
    )
    print("Partitions:", ddf.npartitions)

    # 2) Lazy Evaluation: هذه الأسطر تبني الـ Task Graph فقط
    mean_task = ddf[VALUE_COL].mean()
    group_task = ddf.groupby(CAT_COL)[VALUE_COL].sum()
    print("Lazy object:", type(mean_task))  # لم يُحسب شيء بعد
    raw = mean_task.__dask_graph__()
    opt = mean_task.optimize().__dask_graph__()
    print(f"Graph tasks: raw={len(raw)} | optimized={len(opt)}")
    # 3) رسم المخطط قبل/بعد التحسين (يحتاج Graphviz، اختياري)
    try:
        mean_task.visualize(filename="graph_raw.png", optimize_graph=False)
        mean_task.visualize(filename="graph_optimized.png", optimize_graph=True)
        print("تم حفظ graph_raw.png و graph_optimized.png")
    except Exception as e:
        print("تخطي الرسم (ثبّت Graphviz):", type(e).__name__)

    # 4) التنفيذ: compute واحد لكليهما ليتشاركا قراءة الملف
    with Monitor() as m, ProgressBar():
        mean_val, by_cat = dask.compute(mean_task, group_task)

    print(f"\nMean: {mean_val:.4f}")
    print(by_cat)
    print(f"Time: {m.elapsed:.1f}s | Peak RAM: {m.peak:.0f} MB")

    save_result("Dask DataFrame", status="success", peak_mb=m.peak,
                time_s=m.elapsed, mean=float(mean_val), partitions=ddf.npartitions)


if __name__ == "__main__":  # ضروري على Windows/Mac
    main()
