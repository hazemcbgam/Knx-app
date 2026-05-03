[app]

# اسم التطبيق الذي سيظهر على الهاتف
title = KNX PRO MAX

# اسم الحزمة (داخلي)
package.name = knxpromax

# النطاق (عكس عنوان موقعك)
package.domain = com.knx

# المجلد الذي يحتوي على الكود
source.dir = .

# الملفات التي سيتم تضمينها
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json,db

# الملف الرئيسي
main.py = main.py

# الإصدار
version = 1.0.0

# متطلبات التطبيق (المكتبات)
requirements = python3,kivy,kivymd,sqlite3

# لغة التطبيق
language = fr

# أيقونة التطبيق (ضع صورتك هنا)
icon.filename = icon.png

# شاشة الترحيب
presplash.filename = presplash.png

# النشاط الرئيسي
android.entrypoint = org.kivy.android.PythonActivity

# أذونات التطبيق
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# إصدار Android API (30 = Android 11)
android.api = 30

# أقل إصدار Android مدعوم (21 = Android 5.0)
android.minapi = 21

# إصدار NDK
android.ndk = 23b

# SDK
android.sdk = 30

# المعالجات المدعومة
android.archs = arm64-v8a, armeabi-v7a

# رفع مستوى الأمان
android.gradle_repository = true

# دقة الشاشة
android.whitelist = True

# وضع الكامل
fullscreen = 0

# اتجاه الشاشة
orientation = portrait

# وحدة المعالجة المركزية المسموح بها
android.add_src = 

# الخدمات الإضافية
services = 

# متغيرات البيئة
android.env = 

# إعدادات Debug
android.accept_sdk_license = True

[buildozer]

# مستوى التسجيل (1 = أقل، 2 = عادي)
log_level = 2

# تحذير إذا كان الجذر
warn_on_root = 1

# الخادم (دائماً 1)
build_server = 1

# استخدام صندوق عزل
build_server_platform = linux

# مسار التخزين المؤقت
cache_dir = .buildozer_cache

# تحديث القائمة
update_on_changes = True