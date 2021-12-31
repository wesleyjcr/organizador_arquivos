import sys
from PyQt5.QtWidgets import QApplication
from organizador.organizador import Organizador

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Organizador()
    window.show()
    sys.exit(app.exec_())
