# دليل نشر تطبيق الغيث على PythonAnywhere

## الخطوة 1: إنشاء حساب
1. اذهب إلى https://www.pythonanywhere.com
2. اضغط **Sign Up** (اختر الخطة المجانية **Beginner**)
3. سجل بريدك الإلكتروني واختر اسم مستخدم (مثلاً: `alghith`)
4. رابط تطبيقك سيكون: `https://alghith.pythonanywhere.com`

## الخطوة 2: رفع الملفات
1. بعد تسجيل الدخول، اذهب إلى **Consoles** → **Bash**
2. نفذ الأوامر التالية:

```bash
# إنشاء مجلد المشروع
mkdir -p alghith
cd alghith

# رفع الملفات عبر واجهة PythonAnywhere:
# اذهب إلى Files → Upload a file
# ارفع هذه الملفات:
# - app.py
# - requirements.txt
# - wsgi.py (بعد تعديله)
# - جميع مجلدات templates/ و static/
```

**أو** استخدم Git إذا كان عندك مستودع:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/alghith.git
cd alghith
```

## الخطوة 3: تثبيت المكتبات
في Bash console:
```bash
cd alghith
pip3.10 install -r requirements.txt
```

## الخطوة 4: تعديل wsgi.py
افتح ملف `wsgi.py` من واجهة Files واستبدل `YOUR_USERNAME` باسم حسابك:

```python
import sys
import os

project_home = '/home/YOUR_USERNAME/alghith'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.chdir(project_home)

from app import app as application
```

## الخطوة 5: إعداد التطبيق
1. اذهب إلى **Web** → **Add a new web app**
2. اختر **Manual configuration**
3. اختر **Python 3.10**
4. في **Source code** اكتب: `/home/YOUR_USERNAME/alghith`
5. في **Working directory** اكتب: `/home/YOUR_USERNAME/alghith`
6. في **WSGI configuration file** اضغط على الرابط وعدله ليكون مثل `wsgi.py`

## الخطوة 6: إنشاء قاعدة البيانات
في Bash console:
```bash
cd alghith
mkdir -p instance
python3.10 -c "from app import init_db, app; app.app_context().push(); init_db(); print('تم إنشاء قاعدة البيانات')"
```

## الخطوة 7: تشغيل التطبيق
1. اذهب إلى **Web**
2. اضغط **Reload** على تطبيقك
3. افتح الرابط: `https://YOUR_USERNAME.pythonanywhere.com/setup`

## الخطوة 8: إنشاء أول حساب
افتح الرابط واختر:
1. نوع النشاط
2. بيانات الشركة
3. اسم المستخدم وكلمة المرور

---

## ملاحظات مهمة

### تحديث التطبيق
بعد أي تعديل على الكود:
1. ارفع الملفات المعدلة عبر **Files**
2. اذهب إلى **Web** → **Reload**

### قاعدة البيانات
- ملف قاعدة البيانات `instance/alghith.db` يتم إنشاؤه تلقائياً
- لعمل نسخة احتياطية: حمّل الملف من **Files**

### الخطة المجانية
- يعمل 24/7 لكن يتوقف بعد 3 أشهر من عدم النشاط
- يجب الدخول للوحة التحكم مرة كل 3 أشهر لتجديده
- للترقية: $5/شهر

### الأمان
- غيّر `SECRET_KEY` في `app.py` لقيمة عشوائية
- استخدم كلمات مرور قوية

---

## بديل: Render.com (مجاني أيضاً)
إذا واجهت مشكلة مع PythonAnywhere:
1. اذهب إلى https://render.com
2. اربط مستودع GitHub
3. اختر **Web Service**
4. الإعدادات:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
5. أضف `gunicorn` إلى `requirements.txt`
