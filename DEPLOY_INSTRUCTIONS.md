# تعليمات نشر الغيث على PythonAnywhere

## 1. رفع الملفات
- اذهب إلى PythonAnywhere Dashboard
- افتح Files
- ارفع `alghith-deploy.zip` إلى `/home/Alimubark93/`

## 2. فتح Bash Console
- اذهب إلى Consoles > Open Bash
- نفذ الأوامر التالية:

```bash
cd /home/Alimubark93
rm -rf alghith_old 2>/dev/null
mv alghith alghith_old 2>/dev/null
unzip -o alghith-deploy.zip -d alghith
cd alghith
pip3.11 install --user -r requirements.txt
mkdir -p instance
```

## 3. تحديث wsgi.py
- اذهب إلى Web > `/home/Alimubark93/alghith/wsgi.py`
- تأكد من أن المحتوى:
```python
import sys
import os
project_home = '/home/Alimubark93/alghith'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.chdir(project_home)
instance_dir = os.path.join(project_home, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
from app import app as application
```

## 4. إعادة تشغيل التطبيق
- اذهب إلى Web
- اضغط زر **Reload** الأخضر

## 5. مسح الكاش
- افتح المتصفح واضغط `Ctrl + Shift + Delete`
- امسح الكاش والملفات المؤقتة
- أو افتح الرابط في نافذة خاصة (Incognito)

## 6. التحقق
- افتح `https://Alimubark93.pythonanywhere.com/setup`
- يجب أن تظهر أنواع الأنشطة في الخطوة 1:
  - شركة خدمات
  - متجر / بقالة / سوبر ماركت
  - شركة تجارية
  - شركة مقاولات
  - مطعم / كافتيريا
  - أخرى

## ملاحظات مهمة
- إذا ظهرت مشاكل، تحقق من logs في Web > Error log
- قاعدة البيانات القديمة قد تحتاج حذف: `rm -f /home/Alimubark93/alghith/instance/alghith.db`
- Super Admin: `superadmin` / `superadmin123`
