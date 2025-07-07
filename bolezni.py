import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Определите переменную базы данных здесь
database = {}

class AddDiseaseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить болезнь")
        self.setFixedSize(400, 300)

        self.init_ui()

    def init_ui(self):
        self.name_label = QLabel("Название болезни:")
        self.name_line_edit = QLineEdit()

        self.symptoms_label = QLabel("Описание симптомов:")
        self.symptoms_text_edit = QTextEdit()

        self.diagnosis_label = QLabel("Диагностика:")
        self.diagnosis_text_edit = QTextEdit()

        self.treatment_label = QLabel("Лечение:")
        self.treatment_text_edit = QTextEdit()

        self.prevention_label = QLabel("Профилактика:")
        self.prevention_text_edit = QTextEdit()

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_disease)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.symptoms_label)
        layout.addWidget(self.symptoms_text_edit)
        layout.addWidget(self.diagnosis_label)
        layout.addWidget(self.diagnosis_text_edit)
        layout.addWidget(self.treatment_label)
        layout.addWidget(self.treatment_text_edit)
        layout.addWidget(self.prevention_label)
        layout.addWidget(self.prevention_text_edit)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_disease(self):
        global database
        name = self.name_line_edit.text()
        symptoms = self.symptoms_text_edit.toPlainText()
        diagnosis = self.diagnosis_text_edit.toPlainText()
        treatment = self.treatment_text_edit.toPlainText()
        prevention = self.prevention_text_edit.toPlainText()

        database[name] = {
            "description": symptoms,
            "diagnosis": diagnosis,
            "treatment": treatment,
            "prevention": prevention,
        }

        self.name_line_edit.clear()
        self.symptoms_text_edit.clear()
        self.diagnosis_text_edit.clear()
        self.treatment_text_edit.clear()
        self.prevention_text_edit.clear()

        self.accept()

class ViewDiseaseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Просмотр болезни")
        self.setFixedSize(400, 300)

        self.init_ui()

    def init_ui(self):
        self.name_label = QLabel("Название болезни:")
        self.name_line_edit = QLineEdit()

        self.view_button = QPushButton("Просмотреть")
        self.view_button.clicked.connect(self.view_disease)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.view_button)
        layout.addWidget(self.result_text_edit)

        self.setLayout(layout)

    def view_disease(self):
        global database
        name = self.name_line_edit.text()
        disease_info = database.get(name)

        if disease_info:
            description = disease_info.get("description")
            if description:
                self.result_text_edit.setPlainText(description)
            else:
                self.result_text_edit.setPlainText("Описание отсутствует")
        else:
            self.result_text_edit.setPlainText("Болезнь не найдена")

class MedicalReferenceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Медицинский справочник")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.search_label = QLabel("Поиск:")
        self.search_line_edit = QLineEdit()
        self.search_button = QPushButton("Искать")

        self.add_disease_button = QPushButton("Добавить болезнь")
        self.view_disease_button = QPushButton("Просмотреть болезнь")

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(300, 300)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(self.search_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_disease_button)
        button_layout.addWidget(self.view_disease_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_text_edit)
        main_layout.addWidget(self.image_label)

        self.central_widget.setLayout(main_layout)

        self.search_button.clicked.connect(self.search)
        self.search_line_edit.returnPressed.connect(self.search)
        self.add_disease_button.clicked.connect(self.show_add_disease_dialog)
        self.view_disease_button.clicked.connect(self.show_view_disease_dialog)

    def search(self):
        search_text = self.search_line_edit.text()
        result = self.perform_search(search_text)

        if result:
            self.result_text_edit.setPlainText(result["description"])
            if "image_path" in result:
                pixmap = QPixmap(result["image_path"])
                self.image_label.setPixmap(pixmap)
            else:
                self.image_label.clear()
        else:
            self.result_text_edit.setPlainText("Болезнь не найдена")

    def perform_search(self, query):
        global database

        result = database.get(query)

        return result

    def show_add_disease_dialog(self):
        dialog = AddDiseaseDialog()
        dialog.exec_()

    def show_view_disease_dialog(self):
        dialog = ViewDiseaseDialog()
        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = MedicalReferenceApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
