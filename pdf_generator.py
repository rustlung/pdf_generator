#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Generator Script
Генерирует PDF-документы из CSV/JSON данных с использованием HTML-шаблонов
"""

import os
import sys
import json
import csv
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import pandas as pd
    from weasyprint import HTML, CSS
    from jinja2 import Template
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nУстановите необходимые библиотеки:")
    print("pip install pandas weasyprint jinja2")
    sys.exit(1)


class PDFGenerator:
    """Класс для генерации PDF из данных и шаблонов"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "output"
        
        # Создаем директории если их нет
        self._create_directories()
    
    def _create_directories(self):
        """Создает необходимые директории"""
        for directory in [self.data_dir, self.templates_dir, self.output_dir]:
            directory.mkdir(exist_ok=True)
    
    def get_data_files(self) -> Dict[str, List[Path]]:
        """Находит все CSV и JSON файлы в директории data"""
        csv_files = list(self.data_dir.glob("*.csv"))
        json_files = list(self.data_dir.glob("*.json"))
        
        return {
            "csv": csv_files,
            "json": json_files
        }
    
    def get_template_files(self) -> List[Path]:
        """Находит все HTML-шаблоны в директории templates"""
        return list(self.templates_dir.glob("*.html"))
    
    def read_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Читает CSV файл с помощью pandas"""
        try:
            df = pd.read_csv(file_path)
            # Конвертируем NaN в None для корректной работы
            df = df.where(pd.notnull(df), None)
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Ошибка чтения CSV файла {file_path}: {e}")
            return []
    
    def read_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Читает JSON файл стандартной библиотекой"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Если это список записей - возвращаем как есть
                if isinstance(data, list):
                    return data
                # Если это объект с полем 'invoices' или 'data'
                elif isinstance(data, dict):
                    if 'invoices' in data:
                        return data['invoices']
                    elif 'data' in data:
                        return data['data']
                    else:
                        # Возвращаем как единственную запись
                        return [data]
                return []
        except Exception as e:
            print(f"❌ Ошибка чтения JSON файла {file_path}: {e}")
            return []
    
    def read_data_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Читает файл данных в зависимости от расширения"""
        if file_path.suffix.lower() == '.csv':
            return self.read_csv_file(file_path)
        elif file_path.suffix.lower() == '.json':
            return self.read_json_file(file_path)
        return []
    
    def get_invoice_ids(self, data: List[Dict[str, Any]]) -> List[str]:
        """Извлекает список invoice_id из данных"""
        invoice_ids = []
        for record in data:
            # Ищем поле invoice_id (или его вариации)
            for key in ['invoice_id', 'invoiceId', 'id', 'invoice_number', 'number']:
                if key in record and record[key] is not None:
                    invoice_ids.append(str(record[key]))
                    break
        return invoice_ids
    
    def find_invoice_data(self, data: List[Dict[str, Any]], invoice_id: str) -> Optional[Dict[str, Any]]:
        """Находит данные по конкретному invoice_id"""
        for record in data:
            for key in ['invoice_id', 'invoiceId', 'id', 'invoice_number', 'number']:
                if key in record and str(record[key]) == invoice_id:
                    return record
        return None
    
    def read_template(self, template_path: Path) -> str:
        """Читает HTML-шаблон"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Ошибка чтения шаблона {template_path}: {e}")
            return ""
    
    def render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Рендерит HTML-шаблон с данными"""
        try:
            template = Template(template_content)
            return template.render(**data)
        except Exception as e:
            print(f"❌ Ошибка рендеринга шаблона: {e}")
            print(f"   Тип ошибки: {type(e).__name__}")
            import traceback
            print(f"   Детали: {traceback.format_exc()}")
            return ""
    
    def generate_pdf(self, html_content: str, output_path: Path) -> bool:
        """Генерирует PDF из HTML с поддержкой кириллицы"""
        try:
            # CSS для поддержки кириллицы
            css_content = """
            @font-face {
                font-family: 'DejaVu Sans';
                src: local('DejaVu Sans');
            }
            body {
                font-family: 'DejaVu Sans', 'Roboto', 'Arial', sans-serif;
            }
            """
            
            HTML(string=html_content).write_pdf(
                output_path,
                stylesheets=[CSS(string=css_content)]
            )
            return True
        except Exception as e:
            print(f"❌ Ошибка генерации PDF: {e}")
            print(f"   Тип ошибки: {type(e).__name__}")
            import traceback
            print(f"   Детали: {traceback.format_exc()}")
            return False
    
    def open_pdf(self, pdf_path: Path):
        """Открывает PDF в системной программе"""
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        except Exception as e:
            print(f"❌ Не удалось открыть PDF: {e}")
            print(f"Файл сохранен в: {pdf_path}")
    
    def display_menu(self, items: List[Any], title: str) -> int:
        """Отображает меню и возвращает выбор пользователя"""
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
        
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")
        
        print(f"{'=' * 60}")
        
        while True:
            try:
                choice = input(f"\nВыберите вариант (1-{len(items)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(items):
                    return choice_num - 1
                else:
                    print(f"⚠️  Введите число от 1 до {len(items)}")
            except ValueError:
                print("⚠️  Введите корректное число")
            except KeyboardInterrupt:
                print("\n\n👋 Выход из программы")
                sys.exit(0)
    
    def run(self):
        """Главный цикл программы"""
        print("\n" + "=" * 60)
        print("  📄 PDF Generator - Генератор PDF документов")
        print("=" * 60)
        
        # Шаг 1: Получаем список файлов данных
        data_files = self.get_data_files()
        all_data_files = data_files["csv"] + data_files["json"]
        
        if not all_data_files:
            print("\n❌ Не найдено файлов с данными в директории /data")
            print(f"   Добавьте CSV или JSON файлы в: {self.data_dir}")
            return
        
        # Отображаем доступные файлы данных
        file_names = [f.name for f in all_data_files]
        selected_data_idx = self.display_menu(file_names, "📊 Доступные файлы с данными")
        selected_data_file = all_data_files[selected_data_idx]
        
        # Читаем данные
        print(f"\n⏳ Чтение файла: {selected_data_file.name}...")
        data = self.read_data_file(selected_data_file)
        
        if not data:
            print("❌ Не удалось прочитать данные из файла")
            return
        
        print(f"✅ Загружено записей: {len(data)}")
        
        # Шаг 2: Получаем список шаблонов
        template_files = self.get_template_files()
        
        if not template_files:
            print("\n❌ Не найдено HTML-шаблонов в директории /templates")
            print(f"   Добавьте HTML файлы в: {self.templates_dir}")
            return
        
        # Отображаем доступные шаблоны
        template_names = [f.name for f in template_files]
        selected_template_idx = self.display_menu(template_names, "📝 Доступные HTML-шаблоны")
        selected_template_file = template_files[selected_template_idx]
        
        # Шаг 3: Показываем список invoice_id
        invoice_ids = self.get_invoice_ids(data)
        
        if not invoice_ids:
            print("\n❌ Не найдено invoice_id в данных")
            return
        
        # Отображаем список чеков
        selected_invoice_idx = self.display_menu(invoice_ids, "🧾 Доступные чеки (Invoice ID)")
        selected_invoice_id = invoice_ids[selected_invoice_idx]
        
        # Шаг 4: Генерируем PDF
        print(f"\n⏳ Генерация PDF для Invoice ID: {selected_invoice_id}...")
        
        # Получаем данные для выбранного invoice
        invoice_data = self.find_invoice_data(data, selected_invoice_id)
        
        if not invoice_data:
            print("❌ Не удалось найти данные для выбранного invoice_id")
            return
        
        # Читаем и рендерим шаблон
        template_content = self.read_template(selected_template_file)
        if not template_content:
            return
        
        html_content = self.render_template(template_content, invoice_data)
        if not html_content:
            return
        
        # Генерируем PDF
        output_filename = f"invoice_{selected_invoice_id}.pdf"
        output_path = self.output_dir / output_filename
        
        if self.generate_pdf(html_content, output_path):
            print(f"✅ PDF успешно создан: {output_filename}")
            print(f"📁 Путь: {output_path}")
            
            # Открываем PDF
            print("\n⏳ Открытие PDF...")
            self.open_pdf(output_path)
        else:
            print("❌ Не удалось создать PDF")


def main():
    """Точка входа в программу"""
    generator = PDFGenerator()
    generator.run()


if __name__ == "__main__":
    main()

