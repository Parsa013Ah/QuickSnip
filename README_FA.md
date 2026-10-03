# quicksnip

> یک ابزار سریع برای مدیریت کد اسنیپت‌ها مستقیم از ترمینال

[![PyPI](https://img.shields.io/pypi/v/quicksnip.svg)](https://pypi.org/project/quicksnip/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![demo](demo.gif)

## چرا quicksnip؟

خسته‌اید که برای پیدا کردن یه تابع که قبلاً نوشتید باید توی پروژه‌های قدیمی بگردید؟ **quicksnip** بهتون اجازه میده کد اسنیپت‌ها رو ذخیره، جستجو و کپی کنید مستقیم از ترمینال.

## ویژگی‌ها

- **سریع** - جستجو و کپی اسنیپت‌ها در میلی‌ثانیه
- **جستجوی فازی** - پیدا کردن اسنیپت‌ها بر اساس نام، توضیحات یا کد
- **تگ و زبان** - سازماندهی اسنیپت‌ها
- **یکپارچگی با کلیپ‌بورد** - کپی با یک دستور
- **ورودی/خروجی** - پشتیبان‌گیری و اشتراک‌گذاری اسنیپت‌ها
- **هایلایت سینتکس** - نمایش زیبا کد

## نصب

```bash
pip install quicksnip
```

## استفاده

هر دو دستور `snip` و `quicksnip` کار می‌کنند:

### افزودن اسنیپت
```bash
snip add my-function -d "Quick sort implementation" -l python -t "algorithms,sorting" -c "def quicksort(arr): ..."
```

### جستجوی اسنیپت‌ها
```bash
snip search "sort"
snip search -l python
snip search -t algorithms
```

### کپی به کلیپ‌بورد
```bash
snip copy my-function
```

### لیست همه اسنیپت‌ها
```bash
snip list
snip list -l python
```

### نمایش یک اسنیپت
```bash
snip show my-function
```

### ورودی/خروجی
```bash
snip export backup.json
snip import backup.json
```

## لایسنس

MIT
