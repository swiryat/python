import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)
window = QMainWindow()
window.show()
sys.exit(app.exec_())
