"""أدوات مشتركة: قياس الذاكرة/الوقت وحفظ النتائج."""
import json
import os
import threading
import time

import psutil

# ===== عدّل هذه الإعدادات حسب بياناتك =====
DATA_FILE = "big_data.csv"   # مسار ملفك (مثلاً "data/taxi.csv" أو "data/taxi_*.csv")
CAT_COL = "category"         # عمود نصي/فئوي للتجميع (groupby)
VALUE_COL = "value"          # عمود رقمي لحساب المتوسط والمجموع
# ==========================================
RESULTS_FILE = "results.json"


def mem_mb() -> float:
    """الذاكرة الحالية (RSS) للعملية بالـ MB."""
    return psutil.Process(os.getpid()).memory_info().rss / 1024**2


class Monitor:
    """context manager يقيس الوقت وأعلى استهلاك للذاكرة (Peak)."""

    def __init__(self, interval: float = 0.05):
        self.interval = interval
        self.peak = 0.0
        self.elapsed = 0.0
        self._running = False

    def _watch(self):
        while self._running:
            self.peak = max(self.peak, mem_mb())
            time.sleep(self.interval)

    def __enter__(self):
        self._running = True
        self.peak = mem_mb()
        self._start = time.time()
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.time() - self._start
        self._running = False
        self._thread.join()
        self.peak = max(self.peak, mem_mb())
        return False  # لا نبتلع الاستثناءات


def save_result(method: str, **data):
    """يحفظ نتيجة طريقة معينة في results.json."""
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            results = json.load(f)
    results[method] = data
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2, default=str)


def system_info():
    print(f"Total RAM : {psutil.virtual_memory().total / 1024**3:.1f} GB")
    print(f"Available : {psutil.virtual_memory().available / 1024**3:.1f} GB")
    print(f"CPU cores : {os.cpu_count()}")
