import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)
window = QWidget()
window.setGeometry(100, 100, 300, 200)
label = QLabel("Hello, PyQt!", window)
label.setAlignment(Qt.AlignCenter)
label.show()
window.show()
sys.exit(app.exec_())