import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from GUI.aes_gui_ui import Ui_MainWindow
from aes_tool import encrypt, decrypt
import os
import sys
from PyQt5.QtGui import QCursor
from widgets.hexagon_spinner import HexagonWidget
from PyQt5.QtWidgets import QVBoxLayout



def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)




class NeonButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.default_color = "#39ff14"
        self.hover_color = "#70ff58"
        self.pressed_color = "#20c700"
        self.apply_neon_effect(self.default_color)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, event):
        self.apply_neon_effect(self.hover_color, blur_radius=20)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.apply_neon_effect(self.default_color, blur_radius=10)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.apply_neon_effect(self.pressed_color, blur_radius=5)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.apply_neon_effect(self.hover_color, blur_radius=15)
        super().mouseReleaseEvent(event)

    def apply_neon_effect(self, color, blur_radius=1):
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(blur_radius)
        glow.setColor(QColor(color))
        glow.setOffset(0)
        self.setGraphicsEffect(glow)




class AESApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.hex = HexagonWidget()
        layout = QVBoxLayout(self.ui.hexagonWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.hex)

        self.replace_buttons_with_neon()


        self.ui.browseInputButton.clicked.connect(self.select_input_file)
        self.ui.browseOutputButton.clicked.connect(self.select_output_file)
        self.ui.browseKeyButton.clicked.connect(self.select_key_file)
        self.ui.encryptButton.clicked.connect(self.encrypt_file)
        self.ui.decryptButton.clicked.connect(self.decrypt_file)


        for line_edit in [self.ui.inputLineEdit, self.ui.outputLineEdit, self.ui.keyLineEdit]:
            self.apply_neon_glow(line_edit, "#39ff14")

    def replace_buttons_with_neon(self):

        for layout in [self.ui.verticalLayout_5, self.ui.verticalLayout_7, 
                       self.ui.verticalLayout_6, self.ui.verticalLayout_10, 
                       self.ui.verticalLayout_11]:
            while layout.count():
                old_widget = layout.takeAt(0).widget()
                if old_widget:
                    old_widget.deleteLater()


        self.ui.browseInputButton = NeonButton("browse..")
        self.ui.browseOutputButton = NeonButton("browse..")
        self.ui.browseKeyButton = NeonButton("browse..")
        self.ui.encryptButton = NeonButton("ENCRYPT")
        self.ui.decryptButton = NeonButton("DECRYPT")


        self.ui.verticalLayout_5.addWidget(self.ui.browseInputButton)
        self.ui.verticalLayout_7.addWidget(self.ui.browseOutputButton)
        self.ui.verticalLayout_6.addWidget(self.ui.browseKeyButton)
        self.ui.verticalLayout_10.addWidget(self.ui.encryptButton)
        self.ui.verticalLayout_11.addWidget(self.ui.decryptButton)


    def apply_neon_glow(self, widget, color="#39ff14"):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        widget.setGraphicsEffect(glow)

    def select_input_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select input file")
        if file:
            self.ui.inputLineEdit.setText(file)
            self.hex.set_rotation_speed(5.0)        #juster farten af hexagon spin

    def select_output_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Select output file")
        if file:
            self.ui.outputLineEdit.setText(file)

    def select_key_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Select key file")
        if file:
            self.ui.keyLineEdit.setText(file)

    def encrypt_file(self):
        try:
            self.hex.stop_rotation(3000)                         #pauser spin
            encrypt(
                self.ui.inputLineEdit.text(),
                self.ui.outputLineEdit.text(),
                self.ui.keyLineEdit.text()
            )
            self.show_message("File successfully encrypted!")
        except Exception as e:
            self.show_message(f"Error: {e}")

    def decrypt_file(self):
        try:
            self.hex.stop_rotation(3000)                         #pauser spin
            decrypt(
                self.ui.inputLineEdit.text(),
                self.ui.outputLineEdit.text(),
                self.ui.keyLineEdit.text()
            )
            self.show_message("File successfully decrypted!")
        except Exception as e:
            self.show_message(f"Error: {e}")

    def show_message(self, text):
        QMessageBox.information(self, "Status", text)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(resource_path("styles/style.qss"), "r") as f:
        app.setStyleSheet(f.read())

    window = AESApp()
    window.show()
    sys.exit(app.exec_())
