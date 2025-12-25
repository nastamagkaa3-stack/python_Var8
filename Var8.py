import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class AgriculturePriceCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.rates = {'ячмень': 50, 'озимая пшеница': 35, 'подсолнечник': 45}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Калькулятор цен')
        self.setGeometry(100, 100, 500, 600)

        # Главный лейаут
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Калькулятор цены растениеводства")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Поля ввода
        self.crop = QComboBox()
        self.crop.addItems(self.rates.keys())
        self.inputs = {
            'Себестоимость': QLineEdit(),
            'Объем': QLineEdit(),
            'Аренда': QLineEdit(),
            'Зарплата': QLineEdit(),
            'Маркетинг': QLineEdit()
        }

        for label, widget in self.inputs.items():
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            row.addWidget(widget)
            layout.addLayout(row)

        layout.addWidget(QLabel("Культура:"))
        layout.addWidget(self.crop)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn1 = QPushButton("Рассчитать")
        btn1.clicked.connect(self.calculate)
        btn2 = QPushButton("Сравнить")
        btn2.clicked.connect(self.compare)
        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        layout.addLayout(btn_layout)

        # Результаты
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)

        # Статус
        self.status = QLabel("Введите данные")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def calculate(self):
        try:
            # Получаем данные
            cost = float(self.inputs['Себестоимость'].text() or 0)
            volume = float(self.inputs['Объем'].text() or 0)
            rent = float(self.inputs['Аренда'].text() or 0)
            salary = float(self.inputs['Зарплата'].text() or 0)
            marketing = float(self.inputs['Маркетинг'].text() or 0)

            # Расчеты
            transport = volume * 0.5
            insurance = salary * 0.3
            markup = self.rates.get(self.crop.currentText(), 0)
            total = (cost + rent + salary + insurance + marketing) * (1 + markup / 100)

            # Вывод
            text = f"""
            РЕЗУЛЬТАТЫ:
            ---------------------------
            Культура: {self.crop.currentText()}
            Транспорт: {transport:.2f} тыс. руб.
            Страховые: {insurance:.2f} тыс. руб.
            Наценка: {markup}%
            ---------------------------
            ИТОГО: {total:.2f} тыс. руб.
            """
            self.results.setText(text)
            self.status.setText(f"Цена: {total:.2f} тыс. руб.")
            self.calculated_price = total
        except:
            self.status.setText("Ошибка в данных")

    def compare(self):
        if not hasattr(self, 'calculated_price'):
            self.status.setText("Сначала рассчитайте цену")
            return

        planned = 150
        prices = [self.calculated_price, planned]
        labels = ['Рассчитанная', 'Плановая']

        plt.bar(labels, prices, color=['green', 'red'])
        plt.title(f'Разница: {self.calculated_price - planned:+.2f}')
        plt.ylabel('Цена (тыс. руб.)')
        plt.show()


def main():
    app = QApplication(sys.argv)
    window = AgriculturePriceCalculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()