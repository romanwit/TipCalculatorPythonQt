import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QDoubleSpinBox, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

import qt_material_resources_rc
from qt_material import apply_stylesheet


class BillRow(QWidget):
    def __init__(self, parent_layout, update_total_callback):
        super().__init__()
        self.parent_layout = parent_layout
        self.update_total_callback = update_total_callback

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_self)
        self.layout.addWidget(self.delete_button)

        # Bill amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setDecimals(2)
        self.amount_input.setMaximum(1_000_000)
        self.amount_input.valueChanged.connect(self.update_tip_total)
        self.layout.addWidget(self.amount_input)

        # Tip percentage
        self.tip_percent_input = QSpinBox()
        self.tip_percent_input.setSuffix(" %")
        self.tip_percent_input.setMaximum(100)
        self.tip_percent_input.valueChanged.connect(self.update_tip_total)
        self.layout.addWidget(self.tip_percent_input)

        # Total amount (bill + tip)
        self.total_label = QLabel("0.00")
        self.layout.addWidget(self.total_label)

    def delete_self(self):
        self.setParent(None)
        self.parent_layout.removeWidget(self)
        self.deleteLater()
        self.update_total_callback()

    def update_tip_total(self):
        amount = self.amount_input.value()
        percent = self.tip_percent_input.value()
        total = amount + (amount * percent / 100)
        self.total_label.setText(f"{total:.2f}")
        self.update_total_callback()

    def get_total(self):
        return float(self.total_label.text())


class TipCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tip Calculator")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.bill_rows = []

        # Add row button
        self.add_button = QPushButton("Add Row")
        self.add_button.clicked.connect(self.add_row)
        self.layout.addWidget(self.add_button)

        # Container for bill rows
        self.rows_container = QVBoxLayout()
        self.layout.addLayout(self.rows_container)

        # Total amount
        self.total_sum_label = QLabel("Total Amount: 0.00")
        self.total_sum_label.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.total_sum_label)

        self.add_row()

    def add_row(self):
        row = BillRow(self.rows_container, self.update_total_sum)
        self.bill_rows.append(row)
        self.rows_container.addWidget(row)
        self.update_total_sum()

    def update_total_sum(self):
        total = sum(row.get_total() for row in self.bill_rows if row.parent() is not None)
        self.total_sum_label.setText(f"Total Amount: {total:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_db = QFontDatabase()
    app.setFont(font_db.systemFont(QFontDatabase.GeneralFont))
    apply_stylesheet(app, theme='light_blue.xml')
    window = TipCalculator()
    window.show()
    sys.exit(app.exec_())
