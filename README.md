# 📄 PDF Generator - Генератор PDF документов

Автоматическая генерация PDF-документов из CSV и JSON данных с использованием HTML-шаблонов.

## ✨ Возможности

- 📊 Чтение данных из CSV (pandas) и JSON (стандартная библиотека)
- 📝 Использование HTML-шаблонов с поддержкой Jinja2
- 🌍 Полная поддержка кириллицы (шрифты DejaVu Sans, Roboto)
- 🖥️ Кросс-платформенность (Windows, macOS, Linux)
- 🎨 Интерактивное меню выбора файлов и шаблонов
- 🚀 Автоматическое открытие сгенерированного PDF

## 📦 Установка

### 1. Клонирование/скачивание проекта

Убедитесь, что вы находитесь в директории проекта:
```bash
cd "C:\Users\visig\Python scripts\pdf_gen"
```

### 2. Установка зависимостей

#### Windows

```bash
pip install -r requirements.txt
```

**Важно для Windows:** WeasyPrint требует установки GTK3. Скачайте и установите GTK3 Runtime:
- [Скачать GTK3 для Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

Или используйте альтернативный метод установки:
```bash
pip install weasyprint
```

Если возникают проблемы, используйте conda:
```bash
conda install -c conda-forge weasyprint
```

#### macOS

```bash
# Установите зависимости через Homebrew
brew install python3 cairo pango gdk-pixbuf libffi

# Установите Python пакеты
pip install -r requirements.txt
```

#### Linux (Ubuntu/Debian)

```bash
# Установите системные зависимости
sudo apt-get update
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Установите Python пакеты
pip install -r requirements.txt
```

### 3. Установка шрифтов (опционально, но рекомендуется)

Для корректного отображения кириллицы установите шрифты:

#### Windows
Шрифты обычно уже установлены. Если нет, скачайте:
- [DejaVu Sans](https://dejavu-fonts.github.io/)
- [Roboto](https://fonts.google.com/specimen/Roboto)

#### macOS / Linux
```bash
# Для Ubuntu/Debian
sudo apt-get install fonts-dejavu fonts-roboto

# Для macOS
brew tap homebrew/cask-fonts
brew install font-dejavu font-roboto
```

## 📁 Структура проекта

```
pdf_gen/
├── pdf_generator.py      # Основной скрипт
├── requirements.txt      # Зависимости Python
├── README.md            # Документация
├── data/                # Директория с данными
│   ├── invoices.csv    # Пример CSV файла
│   └── orders.json     # Пример JSON файла
├── templates/           # Директория с HTML-шаблонами
│   ├── invoice_simple.html      # Простой шаблон
│   └── invoice_detailed.html    # Детализированный шаблон
└── output/              # Сгенерированные PDF файлы
```

## 🚀 Использование

### Запуск программы

```bash
python pdf_generator.py
```

### Процесс работы

1. **Выбор файла данных** - Программа покажет список доступных CSV и JSON файлов в директории `/data`
2. **Выбор шаблона** - Выберите HTML-шаблон из директории `/templates`
3. **Выбор Invoice ID** - Выберите конкретный чек для генерации PDF
4. **Генерация PDF** - PDF создается автоматически и открывается в системной программе

### Пример работы

```
============================================================
  📄 PDF Generator - Генератор PDF документов
============================================================

============================================================
  📊 Доступные файлы с данными
============================================================
  1. invoices.csv
  2. orders.json
============================================================

Выберите вариант (1-2): 1

⏳ Чтение файла: invoices.csv...
✅ Загружено записей: 5

============================================================
  📝 Доступные HTML-шаблоны
============================================================
  1. invoice_simple.html
  2. invoice_detailed.html
============================================================

Выберите вариант (1-2): 2

============================================================
  🧾 Доступные чеки (Invoice ID)
============================================================
  1. INV-001
  2. INV-002
  3. INV-003
  4. INV-004
  5. INV-005
============================================================

Выберите вариант (1-5): 1

⏳ Генерация PDF для Invoice ID: INV-001...
✅ PDF успешно создан: invoice_INV-001.pdf
📁 Путь: C:\Users\visig\Python scripts\pdf_gen\output\invoice_INV-001.pdf

⏳ Открытие PDF...
```

## 📝 Формат данных

### CSV файлы

CSV файлы должны содержать следующие поля:
- `invoice_id` (обязательно) - уникальный идентификатор счета
- `company_name` - название компании
- `customer_name` - имя клиента
- `date` - дата
- `item_name` - название товара
- `quantity` - количество
- `price` - цена за единицу
- `total` - общая сумма

Пример (`data/invoices.csv`):
```csv
invoice_id,company_name,customer_name,date,item_name,quantity,price,total
INV-001,ООО "Технологии",Иванов Иван,2025-01-15,Ноутбук Dell,2,85000,170000
```

### JSON файлы

JSON файлы могут быть в одном из форматов:

**Формат 1: Массив объектов**
```json
[
  {
    "invoice_id": "ORD-001",
    "company_name": "ООО Прогресс",
    ...
  }
]
```

**Формат 2: Объект с полем invoices или data**
```json
{
  "invoices": [
    {
      "invoice_id": "ORD-001",
      ...
    }
  ]
}
```

Для детализированных счетов можно использовать вложенный массив `items`:
```json
{
  "invoice_id": "ORD-001",
  "company_name": "ООО Прогресс",
  "items": [
    {
      "item_name": "Товар 1",
      "quantity": 2,
      "price": 1000,
      "total": 2000
    }
  ],
  "subtotal": 2000,
  "tax": 400,
  "total": 2400
}
```

## 🎨 Создание своих шаблонов

Шаблоны используют синтаксис Jinja2. Доступные переменные зависят от структуры ваших данных.

### Основные переменные (для простых шаблонов):
- `{{ invoice_id }}` - номер счета
- `{{ company_name }}` - название компании
- `{{ customer_name }}` - имя клиента
- `{{ date }}` - дата
- `{{ item_name }}` - название товара
- `{{ quantity }}` - количество
- `{{ price }}` - цена
- `{{ total }}` - сумма

### Для детализированных шаблонов:
```html
{% if items %}
  {% for item in items %}
    <tr>
      <td>{{ item.item_name }}</td>
      <td>{{ item.quantity }}</td>
      <td>{{ item.price }}</td>
    </tr>
  {% endfor %}
{% endif %}
```

### Форматирование чисел:
```html
<!-- Формат с разделителями тысяч -->
{{ "{:,.0f}".format(total) }} ₽

<!-- Формат с двумя знаками после запятой -->
{{ "{:,.2f}".format(price) }} ₽
```

### Пример базового шаблона:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Счёт {{ invoice_id }}</title>
    <style>
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
        }
    </style>
</head>
<body>
    <h1>Счёт № {{ invoice_id }}</h1>
    <p>Клиент: {{ customer_name }}</p>
    <p>Дата: {{ date }}</p>
    <p>Итого: {{ total }} ₽</p>
</body>
</html>
```

## 🔧 Решение проблем

### Проблема: WeasyPrint не устанавливается на Windows

**Решение:**
1. Установите GTK3 Runtime: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
2. Или используйте conda: `conda install -c conda-forge weasyprint`

### Проблема: Кириллица отображается неправильно

**Решение:**
1. Убедитесь, что установлены шрифты DejaVu Sans или Roboto
2. Проверьте, что в HTML-шаблоне указан `<meta charset="UTF-8">`
3. В CSS должно быть: `font-family: 'DejaVu Sans', 'Roboto', Arial, sans-serif;`

### Проблема: PDF не открывается автоматически

**Решение:**
- PDF файл все равно сохраняется в директории `/output`
- Откройте его вручную или проверьте права доступа

### Проблема: "Не найдено файлов с данными"

**Решение:**
- Убедитесь, что CSV/JSON файлы находятся в директории `/data`
- Проверьте расширение файлов (должно быть `.csv` или `.json`)

## 📋 Зависимости

- **Python 3.8+**
- **pandas** - чтение и обработка CSV файлов
- **weasyprint** - генерация PDF из HTML
- **jinja2** - шаблонизация HTML

## 🤝 Вклад в проект

Если вы хотите улучшить проект:
1. Добавьте новые шаблоны в `/templates`
2. Создайте примеры данных в `/data`
3. Предложите улучшения кода

## 📄 Лицензия

Этот проект создан в образовательных целях и может быть свободно использован.

## 💡 Дополнительные возможности

Вы можете расширить функциональность:
- Добавить поддержку Excel файлов (`.xlsx`)
- Реализовать пакетную генерацию PDF для всех чеков
- Добавить возможность отправки PDF по email
- Создать веб-интерфейс с помощью Flask или Django
- Добавить QR-коды на счета
- Реализовать цифровую подпись документов

---

**Автор:** PDF Generator Script  
**Версия:** 1.0.0  
**Дата создания:** 2025

