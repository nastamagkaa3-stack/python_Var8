import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class AgriculturePriceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.INSURANCE_RATE = 30
        self.PLANNED_PRICE = 150
        self.delivery_cost = 0.5

        self.markup_rates = {
            'ячмень': 50,
            'озимая пшеница': 35,
            'подсолнечник': 45
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Калькулятор цены продукции')
        self.setGeometry(100, 100, 600, 700)

        main_layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Калькулятор цены растениеводства")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title)

        # Поля ввода
        grid = QGridLayout()

        grid.addWidget(QLabel("Культура:"), 0, 0)
        self.crop_combo = QComboBox()
        self.crop_combo.addItems(['ячмень', 'озимая пшеница', 'подсолнечник'])
        grid.addWidget(self.crop_combo, 0, 1)

        fields = [
            ("Себестоимость 1 ц (тыс. руб.):", "cost_input"),
            ("Объем реализации (ц):", "volume_input"),
            ("Аренда точки (тыс. руб.):", "rent_input"),
            ("Зарплата (тыс. руб.):", "salary_input"),
            ("Маркетинг (тыс. руб.):", "marketing_input")
        ]

        self.inputs = {}
        for i, (label_text, name) in enumerate(fields, 1):
            grid.addWidget(QLabel(label_text), i, 0)
            input_field = QLineEdit()
            input_field.setPlaceholderText("Введите...")
            grid.addWidget(input_field, i, 1)
            self.inputs[name] = input_field

        # Кнопки
        btn_layout = QHBoxLayout()

        self.price_btn = QPushButton("Рассчитать цену")
        self.price_btn.clicked.connect(self.calculate_selling_price)
        self.price_btn.setStyleSheet("background-color: #3498db; color: white;")
        btn_layout.addWidget(self.price_btn)

        self.compare_btn = QPushButton("Сравнить с планом")
        self.compare_btn.clicked.connect(self.compare_prices)
        self.compare_btn.setStyleSheet("background-color: #2ecc71; color: white;")
        btn_layout.addWidget(self.compare_btn)

        grid.addLayout(btn_layout, len(fields) + 1, 0, 1, 2)
        main_layout.addLayout(grid)

        # Результаты
        results_group = QGroupBox("Результаты")
        results_layout = QGridLayout()

        self.results = {}
        result_fields = [
            ("Транспортные расходы (тыс. руб.):", "transport"),
            ("Страховые взносы (тыс. руб.):", "insurance"),
            ("Уровень наценки (%):", "markup"),
            ("Цена реализации (тыс. руб.):", "price")
        ]

        for i, (label_text, name) in enumerate(result_fields):
            results_layout.addWidget(QLabel(label_text), i, 0)
            result_field = QLineEdit()
            result_field.setReadOnly(True)
            if name == "price":
                result_field.setStyleSheet("font-weight: bold; font-size: 14px; color: #27ae60;")
            results_layout.addWidget(result_field, i, 1)
            self.results[name] = result_field

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        # Управление
        control_layout = QHBoxLayout()

        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        control_layout.addWidget(clear_btn)

        info_btn = QPushButton("Справка")
        info_btn.clicked.connect(self.show_info)
        control_layout.addWidget(info_btn)

        main_layout.addLayout(control_layout)

        # Статус
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; color: #7f8c8d;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: Arial; background-color: #f8f9fa; }
            QLineEdit { padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            QPushButton { padding: 10px; border-radius: 5px; font-weight: bold; }
            QGroupBox { border: 2px solid #3498db; border-radius: 5px; }
            QGroupBox::title { color: #2c3e50; padding: 0 10px; }
        """)

    def calculate_selling_price(self):
        # Проверка заполнения полей
        for name, field in self.inputs.items():
            if not field.text().strip():
                self.show_status("Заполните все поля!", "red")
                return

        try:
            # Получение данных
            cost = float(self.inputs['cost_input'].text().replace(',', '.'))
            volume = float(self.inputs['volume_input'].text().replace(',', '.'))
            rent = float(self.inputs['rent_input'].text().replace(',', '.'))
            salary = float(self.inputs['salary_input'].text().replace(',', '.'))
            marketing = float(self.inputs['marketing_input'].text().replace(',', '.'))

            # Расчеты
            transport = round(volume * self.delivery_cost, 2)
            insurance = round(salary * self.INSURANCE_RATE / 100, 2)

            crop = self.crop_combo.currentText()
            markup = self.markup_rates.get(crop, 0)

            # Итоговая цена
            total_expenses = rent + salary + insurance + marketing
            selling_price = round((cost + total_expenses) * (1 + markup / 100), 2)

            # Вывод результатов
            self.results['transport'].setText(f"{transport:.2f}")
            self.results['insurance'].setText(f"{insurance:.2f}")
            self.results['markup'].setText(f"{markup}%")
            self.results['price'].setText(f"{selling_price:.2f}")

            self.calculated_price = selling_price
            self.show_status(f"Цена рассчитана: {selling_price:.2f} тыс. руб.", "green")

        except ValueError:
            self.show_status("Ошибка в данных!", "red")

    def compare_prices(self):
        if not hasattr(self, 'calculated_price'):
            self.show_status("Сначала рассчитайте цену!", "orange")
            return

        # Гистограмма сравнения
        fig, ax = plt.subplots(figsize=(6, 4))
        prices = [self.calculated_price, self.PLANNED_PRICE]
        labels = ['Рассчитанная', 'Плановая']
        colors = ['#2ecc71', '#e74c3c']

        bars = ax.bar(labels, prices, color=colors, alpha=0.8)
        ax.set_ylabel('Цена (тыс. руб.)')
        ax.set_title('Сравнение цен')

        for bar, price in zip(bars, prices):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f'{price:.2f}', ha='center', fontweight='bold')

        diff = self.calculated_price - self.PLANNED_PRICE
        ax.text(0.5, max(prices) + 2, f"Разница: {diff:+.2f}",
                ha='center', fontweight='bold', color='blue')

        plt.tight_layout()
        plt.show()

        self.show_status("Сравнение выполнено", "green")

    def clear_all(self):
        for field in self.inputs.values():
            field.clear()
        for field in self.results.values():
            field.clear()

        if hasattr(self, 'calculated_price'):
            delattr(self, 'calculated_price')

        self.show_status("Все очищено", "blue")

    def show_info(self):
        info = (
            "Формула расчета:\n"
            "Цена = (Себестоимость + Расходы) × (1 + Наценка%)\n\n"
            "Расходы включают:\n"
            "- Аренда\n- Зарплата\n- Страховые взносы (30% от зарплаты)\n"
            "- Маркетинг\n\n"
            "Наценки:\n"
            "Ячмень: 50%\nПшеница: 35%\nПодсолнечник: 45%"
        )
        QMessageBox.information(self, "Справка", info)

    def show_status(self, message, color="black"):
        colors = {'red': '#e74c3c', 'green': '#27ae60',
                  'blue': '#3498db', 'orange': '#f39c12'}
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {colors.get(color, 'black')}; padding: 10px;")


def main():
    app = QApplication(sys.argv)
    window = AgriculturePriceCalculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()