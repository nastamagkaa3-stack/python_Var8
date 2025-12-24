import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt


class AgriculturePriceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.INSURANCE_RATE = 30  # Процент страховых взносов
        self.PLANNED_PRICE = 150  # Плановая цена для сравнения (тыс. руб.)
        self.delivery_cost = 0.5  # Доставка 1 ц продукции, тыс. руб.

        # Уровень наценки по культурам (%)
        self.markup_rates = {
            'ячмень': 50,
            'озимая пшеница': 35,
            'подсолнечник': 45
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Калькулятор цены продукции растениеводства')
        self.setGeometry(100, 100, 700, 800)

        main_layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Определение реализационной цены продукции растениеводства")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title)

        # Создаем основную сетку для размещения полей
        grid_layout = QGridLayout()

        # Тип культуры
        grid_layout.addWidget(QLabel("Тип культуры:"), 0, 0)
        self.crop_combo = QComboBox()
        self.crop_combo.addItems(['ячмень', 'озимая пшеница', 'подсолнечник'])
        grid_layout.addWidget(self.crop_combo, 0, 1)

        # Производственная себестоимость
        grid_layout.addWidget(QLabel("Производственная себестоимость 1 ц (тыс. руб.):"), 1, 0)
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Введите стоимость...")
        grid_layout.addWidget(self.cost_input, 1, 1)

        # Объем реализации
        grid_layout.addWidget(QLabel("Объем реализации (ц):"), 2, 0)
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Введите объем...")
        grid_layout.addWidget(self.volume_input, 2, 1)

        # Аренда торговой точки
        grid_layout.addWidget(QLabel("Аренда торговой точки (тыс. руб.):"), 3, 0)
        self.rent_input = QLineEdit()
        self.rent_input.setPlaceholderText("Введите сумму...")
        grid_layout.addWidget(self.rent_input, 3, 1)

        # Заработная плата продавцам
        grid_layout.addWidget(QLabel("Заработная плата продавцам (тыс. руб.):"), 4, 0)
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Введите сумму...")
        grid_layout.addWidget(self.salary_input, 4, 1)

        # Маркетинговые расходы
        grid_layout.addWidget(QLabel("Маркетинговые расходы (тыс. руб.):"), 5, 0)
        self.marketing_input = QLineEdit()
        self.marketing_input.setPlaceholderText("Введите сумму...")
        grid_layout.addWidget(self.marketing_input, 5, 1)

        # Кнопки расчетов
        buttons_layout = QHBoxLayout()

        self.insurance_btn = QPushButton("Рассчитать страховые взносы")
        self.insurance_btn.clicked.connect(self.calculate_insurance)
        buttons_layout.addWidget(self.insurance_btn)

        self.markup_btn = QPushButton("Уровень наценки")
        self.markup_btn.clicked.connect(self.show_markup)
        buttons_layout.addWidget(self.markup_btn)

        self.price_btn = QPushButton("Рассчитать цену реализации")
        self.price_btn.clicked.connect(self.calculate_selling_price)
        buttons_layout.addWidget(self.price_btn)

        self.compare_btn = QPushButton("Сравнение цен")
        self.compare_btn.clicked.connect(self.compare_prices)
        self.compare_btn.setStyleSheet("background-color: #3498db; color: white;")
        buttons_layout.addWidget(self.compare_btn)

        grid_layout.addLayout(buttons_layout, 6, 0, 1, 2)

        main_layout.addLayout(grid_layout)

        # Группа результатов
        results_group = QGroupBox("Результаты расчетов")
        results_layout = QGridLayout()

        # Страховые взносы
        results_layout.addWidget(QLabel("Страховые взносы (тыс. руб.):"), 0, 0)
        self.insurance_result = QLineEdit()
        self.insurance_result.setReadOnly(True)
        results_layout.addWidget(self.insurance_result, 0, 1)

        # Транспортные расходы
        results_layout.addWidget(QLabel("Транспортные расходы (тыс. руб.):"), 1, 0)
        self.transport_result = QLineEdit()
        self.transport_result.setReadOnly(True)
        results_layout.addWidget(self.transport_result, 1, 1)

        # Уровень наценки
        results_layout.addWidget(QLabel("Уровень наценки (%):"), 2, 0)
        self.markup_result = QLineEdit()
        self.markup_result.setReadOnly(True)
        results_layout.addWidget(self.markup_result, 2, 1)

        # Цена реализации
        results_layout.addWidget(QLabel("Цена реализации (тыс. руб.):"), 3, 0)
        self.price_result = QLineEdit()
        self.price_result.setReadOnly(True)
        self.price_result.setStyleSheet("font-weight: bold; font-size: 14px; color: #27ae60;")
        results_layout.addWidget(self.price_result, 3, 1)

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        # Кнопки управления
        control_layout = QHBoxLayout()

        clear_btn = QPushButton("Очистить все поля")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        control_layout.addWidget(clear_btn)

        info_btn = QPushButton("Справка")
        info_btn.clicked.connect(self.show_info)
        info_btn.setStyleSheet("background-color: #9b59b6; color: white;")
        control_layout.addWidget(info_btn)

        main_layout.addLayout(control_layout)

        # Статус
        self.status_label = QLabel("Готов к работе. Введите данные и нажмите кнопки расчета.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; font-style: italic;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
                background-color: #f9f9f9;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #2c3e50;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
        """)

    def validate_inputs(self):
        """Проверка введенных данных"""
        required_fields = [
            (self.cost_input, "производственная себестоимость"),
            (self.volume_input, "объем реализации"),
            (self.rent_input, "аренда торговой точки"),
            (self.salary_input, "заработная плата продавцам"),
            (self.marketing_input, "маркетинговые расходы")
        ]

        for field, name in required_fields:
            if not field.text().strip():
                self.show_status(f"Введите {name}!", "red")
                return False

            try:
                value = float(field.text().replace(',', '.'))
                if value < 0:
                    self.show_status(f"{name.capitalize()} не может быть отрицательной!", "red")
                    return False
            except ValueError:
                self.show_status(f"Некорректное значение в поле '{name}'!", "red")
                return False

        return True

    def calculate_insurance(self):
        """Расчет страховых взносов"""
        if not self.salary_input.text().strip():
            self.show_status("Введите заработную плату продавцам!", "red")
            return

        try:
            salary = float(self.salary_input.text().replace(',', '.'))
            insurance = round(salary * self.INSURANCE_RATE / 100, 2)
            self.insurance_result.setText(f"{insurance:.2f}")
            self.show_status(f"Страховые взносы рассчитаны: {insurance:.2f} тыс. руб.", "green")
        except ValueError:
            self.show_status("Ошибка ввода заработной платы!", "red")

    def show_markup(self):
        """Показ уровня наценки для выбранной культуры"""
        crop = self.crop_combo.currentText()
        markup = self.markup_rates.get(crop, 0)
        self.markup_result.setText(f"{markup}%")
        self.show_status(f"Уровень наценки для {crop}: {markup}%", "blue")

    def calculate_selling_price(self):
        """Расчет цены реализации"""
        if not self.validate_inputs():
            return

        try:
            # Получаем все входные данные
            cost = float(self.cost_input.text().replace(',', '.'))  # Производственная себестоимость
            volume = float(self.volume_input.text().replace(',', '.'))  # Объем реализации
            rent = float(self.rent_input.text().replace(',', '.'))  # Аренда
            salary = float(self.salary_input.text().replace(',', '.'))  # Зарплата
            marketing = float(self.marketing_input.text().replace(',', '.'))  # Маркетинг

            # Рассчитываем дополнительные расходы
            insurance_text = self.insurance_result.text()
            insurance = float(insurance_text) if insurance_text else 0

            # Транспортные расходы
            transport = round(volume * self.delivery_cost, 2)
            self.transport_result.setText(f"{transport:.2f}")

            # Получаем наценку
            crop = self.crop_combo.currentText()
            markup = self.markup_rates.get(crop, 0)

            if not self.markup_result.text():
                self.markup_result.setText(f"{markup}%")

            # Общие расходы (без производственной себестоимости)
            total_expenses = rent + salary + insurance + marketing

            # Цена реализации по формуле
            selling_price = round((cost + total_expenses) * (1 + markup / 100), 2)

            self.price_result.setText(f"{selling_price:.2f}")

            # Формируем подробный отчет
            report = (f"Расчет цены для {crop}:\n"
                      f"Производственная себестоимость: {cost:.2f} тыс. руб.\n"
                      f"Дополнительные расходы: {total_expenses:.2f} тыс. руб.\n"
                      f"Наценка: {markup}%\n"
                      f"Итоговая цена реализации: {selling_price:.2f} тыс. руб.\n"
                      f"Транспортные расходы: {transport:.2f} тыс. руб.")

            self.show_status(f"Цена реализации рассчитана: {selling_price:.2f} тыс. руб.", "green")

            # Сохраняем для сравнения
            self.calculated_price = selling_price

        except Exception as e:
            self.show_status(f"Ошибка расчета: {str(e)}", "red")

    def compare_prices(self):
        """Сравнение рассчитанной цены с плановой и построение гистограммы"""
        if not hasattr(self, 'calculated_price'):
            self.show_status("Сначала рассчитайте цену реализации!", "orange")
            return

        # Создаем окно с гистограммой
        fig, ax = plt.subplots(figsize=(8, 6))

        prices = [self.calculated_price, self.PLANNED_PRICE]
        labels = ['Рассчитанная цена', 'Плановая цена']
        colors = ['#2ecc71', '#e74c3c']

        bars = ax.bar(labels, prices, color=colors, alpha=0.8)
        ax.set_ylabel('Цена (тыс. руб.)', fontsize=12)
        ax.set_title('Сравнение рассчитанной и плановой цен', fontsize=14, fontweight='bold')

        # Добавляем значения на столбцы
        for bar, price in zip(bars, prices):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                    f'{price:.2f}',
                    ha='center', va='bottom', fontweight='bold')

        # Добавляем разницу
        diff = abs(self.calculated_price - self.PLANNED_PRICE)
        diff_text = f"Разница: {diff:.2f} тыс. руб."

        if self.calculated_price > self.PLANNED_PRICE:
            diff_text += " (рассчитанная цена выше)"
            ax.text(0.5, max(prices) + 2, diff_text,
                    ha='center', fontsize=11, color='red', fontweight='bold')
        elif self.calculated_price < self.PLANNED_PRICE:
            diff_text += " (рассчитанная цена ниже)"
            ax.text(0.5, max(prices) + 2, diff_text,
                    ha='center', fontsize=11, color='blue', fontweight='bold')
        else:
            diff_text = "Цены равны"
            ax.text(0.5, max(prices) + 2, diff_text,
                    ha='center', fontsize=11, color='green', fontweight='bold')

        plt.tight_layout()

        # Показываем окно с графиком
        plt.show()

        # Выводим информацию в консоль
        print("\n" + "=" * 60)
        print("СРАВНЕНИЕ ЦЕН РЕАЛИЗАЦИИ")
        print("=" * 60)
        print(f"Культура: {self.crop_combo.currentText()}")
        print(f"Рассчитанная цена: {self.calculated_price:.2f} тыс. руб.")
        print(f"Плановая цена: {self.PLANNED_PRICE:.2f} тыс. руб.")
        print(f"Разница: {diff:.2f} тыс. руб.")

        if diff / self.PLANNED_PRICE * 100 > 10:
            print("ВНИМАНИЕ: Отклонение более 10%!")
        print("=" * 60)

        self.show_status("Сравнение цен выполнено. Открыто окно с гистограммой.", "green")

    def clear_all(self):
        """Очистка всех полей"""
        self.cost_input.clear()
        self.volume_input.clear()
        self.rent_input.clear()
        self.salary_input.clear()
        self.marketing_input.clear()
        self.insurance_result.clear()
        self.transport_result.clear()
        self.markup_result.clear()
        self.price_result.clear()

        if hasattr(self, 'calculated_price'):
            delattr(self, 'calculated_price')

        self.show_status("Все поля очищены. Готово к новым расчетам.", "blue")

    def show_info(self):
        """Показ справочной информации"""
        info_text = (
            "СПРАВКА ПО РАСЧЕТУ ЦЕНЫ РЕАЛИЗАЦИИ\n\n"
            "Формула расчета:\n"
            "Цена = (Производственная себестоимость + Дополнительные расходы) × (1 + Наценка/100)\n\n"
            "Дополнительные расходы включают:\n"
            "• Аренда торговой точки\n"
            "• Заработная плата продавцам\n"
            "• Страховые взносы (30% от зарплаты)\n"
            "• Маркетинговые расходы\n\n"
            "Уровень наценки по культурам:\n"
            "• Ячмень: 50%\n"
            "• Озимая пшеница: 35%\n"
            "• Подсолнечник: 45%\n\n"
            "Транспортные расходы = Объём реализации × 0.5 тыс. руб."
        )

        QMessageBox.information(self, "Справка", info_text)

    def show_status(self, message, color="black"):
        """Обновление статусной строки"""
        color_map = {
            'red': '#e74c3c',
            'green': '#27ae60',
            'blue': '#3498db',
            'orange': '#f39c12',
            'black': '#2c3c3c'
        }

        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color_map.get(color, 'black')}; padding: 10px; font-style: italic;")


def main():
    app = QApplication(sys.argv)
    calculator = AgriculturePriceCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()