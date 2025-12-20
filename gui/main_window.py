import sys
import os
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QAbstractItemView



#midlertidig fil-lokalisering - ændre/fix det senere
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


#importer en ny GUI (lidt som html/css/javascript, blot at det ikke er DOM (ofc))
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QInputDialog,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from core.vault_session import VaultSession


class MainWindow(QWidget):



    def __init__(self):
        super().__init__()

        raise RuntimeError("AM I RUNNING?")
        self.setAcceptDrops(True)
        #self.setWindowFlags(Qt.FramelessWindowHint)    -for senere udvikling (mere tilpasset vindue)

        self.setWindowTitle("Vault App (prototype)")
        self.resize(700, 300)

        self.session = None

        layout = QVBoxLayout()

        self.status_label = QLabel("No vault open")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.file_list = QListWidget()

        self.create_btn = QPushButton("Create Vault")
        self.open_btn = QPushButton("Open Vault")
        self.close_btn = QPushButton("Close Vault")
        self.extract_btn = QPushButton("Extract Selected")
        
        self.extract_btn.setEnabled(False)
        self.close_btn.setEnabled(False)

        layout.addWidget(self.status_label, 0)
        layout.addWidget(self.file_list, 1)
        layout.addWidget(self.create_btn)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.close_btn)
        layout.addWidget(self.extract_btn)


        self.setLayout(layout)

        #events fra vault.py
        self.create_btn.clicked.connect(self.create_vault)
        self.open_btn.clicked.connect(self.open_vault)
        self.close_btn.clicked.connect(self.close_vault)
        self.extract_btn.clicked.connect(self.extract_selected_file)
        self.file_list.itemSelectionChanged.connect(self._on_selection_changed)
        #dobbeltklik for extract
        self.file_list.itemDoubleClicked.connect(lambda _: self.extract_selected_file())




    def create_vault(self):
        path, _ = QFileDialog.getSaveFileName(self, "Create Vault", "", "Vault Files (*.vault)")
        if not path:
            return

        password, ok = QInputDialog.getText(
            self, 
            "Password", 
            "Enter vault password:", 
            QLineEdit.Password
        )
        if not ok or not password:
            return

        try:
            self.session = VaultSession(path, password, create=True)
            self._vault_opened()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def refresh_file_list(self):
        self.file_list.clear()

        if not self.session:
            return

        for file_entry in self.session.data.get("files", []):
            self.file_list.addItem(file_entry["name"])


    def open_vault(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Vault", "", "Vault Files (*.vault)")
        if not path:
            return

        password, ok = QInputDialog.getText(
            self, 
            "Password", 
            "Enter vault password:", 
            QLineEdit.Password
        )
        
        if not ok or not password:
            return

        try:
            self.session = VaultSession(path, password)
            self._vault_opened()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Failed to open vault")

    def close_vault(self):
        if self.session:
            self.session.close()
            self.session = None
            self.file_list.clear()
            self.extract_btn.setEnabled(False)

        self.status_label.setText("No vault open")
        self.close_btn.setEnabled(False)


    def _vault_opened(self):
        self.status_label.setText("Vault OPEN (session is active)")
        self.close_btn.setEnabled(True)
        self.refresh_file_list()
        self._on_selection_changed()


    def closeEvent(self, event):
        if self.session:
            self.session.close()
        event.accept()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    

    def dropEvent(self, event):
        if not self.session:
            QMessageBox.warning(self, "No vault", "Open a vault first")
            return

        files_added = 0


        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if not path or not os.path.isfile(path):
                continue

            with open(path, "rb") as f:
                data = f.read()

            self.session.data["files"].append({
                "name": os.path.basename(path),
                "content": data.hex()
            })

            files_added += 1

        self.refresh_file_list()

        # QMessageBox.information(
        #     self,
        #     "Files added",
        #     f"{files_added} file(s) added to vault (in RAM)"
        # )
    
    #extract - virker fint, men 
    def extract_selected_file(self):

        if not self.session:
            QMessageBox.warning(self, "No vault", "Open a vault first")
            return

        selected = self.file_list.selectedItems()
        if not selected:
            QMessageBox.information(self, "No selection", "Select a file first")
            return

        filename = selected[0].text()

        entry = None
        for fe in self.session.data.get("files", []):
            if fe.get("name") == filename:
                entry = fe
                break

        if not entry:
            QMessageBox.critical(self, "Error", "File entry not found in vault data")
            return

        #hvor den skal gemmes
        default_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        out_path, _ = QFileDialog.getSaveFileName(self, "Extract file", default_path, "All Files (*)")
        if not out_path:
            return

        try:
            data = bytes.fromhex(entry["content"])
            with open(out_path, "wb") as f:
                f.write(data)

            QMessageBox.information(self, "Extracted", f"Saved to:\n{out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract file:\n{e}")


    def _on_selection_changed(self):
        has_selection = len(self.file_list.selectedItems()) > 0
        self.extract_btn.setEnabled(bool(self.session) and has_selection)













def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
