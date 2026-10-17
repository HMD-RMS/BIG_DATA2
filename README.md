# Big Data Lab: Pandas vs Dask

## الإعداد في VS Code
1. افتح المجلد: File > Open Folder > bigdata_lab
2. افتح Terminal (Ctrl + `) وأنشئ بيئة افتراضية:
   - Windows: `python -m venv .venv` ثم `.venv\Scripts\activate`
   - Linux/Mac: `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. اختر الـ Interpreter: Ctrl+Shift+P > "Python: Select Interpreter" > .venv

## الترتيب
```
python generate_data.py --gb 0.2     # تجربة سريعة أولاً
python task2_chunking.py
python task3_dask.py
python task4_benchmark.py            # رسم المقارنة

python generate_data.py --gb 8       # الحجم الحقيقي (أكبر من RAM)
python task2_chunking.py
python task3_dask.py
python task1_oom.py --limit-gb 4     # أخيراً (الأخطر)
python task4_benchmark.py
```
