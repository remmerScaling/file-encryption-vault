import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QPen, QFont, QIcon

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QListWidget, QSizePolicy, QDialog,
    QListWidgetItem, QVBoxLayout, QSpacerItem
)

from password_window import PasswordDialog

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.vault_session import VaultSession


def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base, rel_path)

icon_path = resource_path("app_icon.ico")

class GlassBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        grad = QLinearGradient(0, 0, 0, rect.height())
        grad.setColorAt(0, QColor(60, 140, 190, 120))
        grad.setColorAt(1, QColor(20, 60, 90, 160))

        p.setBrush(grad)
        p.setPen(QPen(QColor(140, 220, 255, 180), 1.5))
        p.drawRoundedRect(rect, 18, 18)


class ExitButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("EXIT", parent)
        self.setFixedSize(90, 36)


class VaultList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)
        self.setSelectionMode(QListWidget.SingleSelection)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        w = self.window()

        if not e.mimeData().hasUrls():
            return

        urls = e.mimeData().urls()

        if len(urls) == 1:
            p = urls[0].toLocalFile()
            if p.lower().endswith(".vault") and os.path.isfile(p):
                dlg = PasswordDialog("Open Vault", w)
                if dlg.exec_() != QDialog.Accepted:
                    return
                w.session = VaultSession(p, dlg.password_input.text())
                w._vault_opened()
                return

        if not w.session:
            QMessageBox.warning(self, "No vault", "Open a vault first")
            return

        changed = False
        for url in urls:
            path = url.toLocalFile()
            if not os.path.isfile(path):
                continue
            if path.lower().endswith(".vault"):
                continue

            base, ext = os.path.splitext(os.path.basename(path))

            with open(path, "rb") as f:
                data = f.read()

            w.session.data.setdefault("files", []).append({
                "name": base,
                "ext": ext,
                "content": data.hex()
            })
            changed = True

        if changed:
            try:
                w._normalize_files()
                w.session.save()
            except Exception:
                pass
            w._vault_opened()

        e.acceptProposedAction()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Crypto Vault")
        self.setWindowIcon(QIcon(icon_path)) 

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.session = None
        self._drag_pos = None

        self.resize(860, 520)
        self.setMinimumSize(740, 420)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20,20,20,20)

        self.content = QWidget(self)
        outer.addWidget(self.content)

        self.glass = GlassBackground(self)
        self.glass.lower()

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(24,24,24,24)
        layout.setSpacing(12)

        self.title = QLabel("Crypto Vault", alignment=Qt.AlignCenter)
        self.status = QLabel("No vault open", alignment=Qt.AlignCenter)

        self.list = VaultList(self.content)

        self.create_btn = QPushButton("Create Vault")
        self.open_btn = QPushButton("Open Vault")
        self.close_btn = QPushButton("Close Vault")
        self.extract_btn = QPushButton("Extract Selected")

        self.close_btn.setEnabled(False)
        self.extract_btn.setEnabled(False)

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.list, 3)
        self.list.setMaximumHeight(150)


        # layout.addWidget(self.create_btn, 1)
        # layout.addWidget(self.open_btn, 1)
        # layout.addWidget(self.close_btn, 1)
        # layout.addWidget(self.extract_btn, 1)
        self.button_panel = QWidget(self.content)
        btn_layout = QVBoxLayout(self.button_panel)
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        for b in (self.create_btn, self.open_btn, self.close_btn, self.extract_btn):
            btn_layout.addWidget(b)
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        layout.addWidget(self.button_panel, 1)

        self.exit_btn = ExitButton(self.content)
        self.exit_btn.clicked.connect(self.close)

        for b in (self.create_btn, self.open_btn, self.close_btn, self.extract_btn):
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._style()
        self._connect()
        self._reposition_overlays()

    def _style(self):
        self.setStyleSheet("""
        QWidget { color:#cfefff; font-family:"Segoe UI"; font-size:13px; }

        QListWidget {
            background:rgba(10,50,80,120);
            border:1px solid rgba(120,220,255,180);
            border-radius:6px;
            padding:6px;
        }
        QListWidget::item:selected {
            background:rgba(120,220,255,200);
            color:#002030;
        }

        QPushButton {
            background:rgba(20,80,120,140);
            border:1px solid rgba(120,220,255,180);
            border-radius:6px;
            padding:10px;
        }

        QPushButton:hover {
            background:rgba(40,140,200,200);
            border-color:rgba(180,255,255,240);
        }

        QPushButton:pressed {
            background:rgba(20,100,160,220);
        }

        ExitButton {
            background:rgba(200,80,40,220);
            border:1px solid rgba(255,190,120,220);
            font-weight:bold;
        }

        ExitButton:hover {
            background:rgba(255,120,60,240);
        }
        """)

        f = QFont("Segoe UI", 16, QFont.Bold)
        self.title.setFont(f)
        self.title.setStyleSheet("color:#7fefff")

    def _connect(self):
        self.create_btn.clicked.connect(self.create_vault)
        self.open_btn.clicked.connect(self.open_vault)
        self.close_btn.clicked.connect(self.close_vault)
        self.extract_btn.clicked.connect(self.extract_selected)
        self.list.itemSelectionChanged.connect(self._on_select)
        self.list.itemDoubleClicked.connect(lambda _: self.extract_selected())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._reposition_overlays()

    def _reposition_overlays(self):
        g = self.content.geometry()
        self.glass.setGeometry(g)
        self.exit_btn.move(self.content.width() - self.exit_btn.width() - 16, 16)
        self.exit_btn.raise_()

    def closeEvent(self, e):
        try:
            self.close_vault()
        except Exception:
            pass
        super().closeEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            child = self.childAt(e.pos())
            if isinstance(child, (QPushButton, QListWidget)):
                return
            self._drag_pos = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(e.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None

    def _normalize_files(self):
        if not self.session:
            return
        files = self.session.data.setdefault("files", [])
        changed = False
        for f in files:
            if "ext" not in f:
                name = f.get("name", "")
                base, ext = os.path.splitext(name)
                f["name"] = base
                f["ext"] = ext
                changed = True
        if changed:
            try:
                self.session.save()
            except Exception:
                pass

    def create_vault(self):
        path, _ = QFileDialog.getSaveFileName(self, "Create Vault", "", "*.vault")
        if not path:
            return
        dlg = PasswordDialog("Create Vault", self)
        if dlg.exec_() != QDialog.Accepted:
            return
        self.session = VaultSession(path, dlg.password_input.text(), create=True)
        self._vault_opened()

    def open_vault(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Vault", "", "*.vault")
        if not path:
            return
        dlg = PasswordDialog("Open Vault", self)
        if dlg.exec_() != QDialog.Accepted:
            return
        self.session = VaultSession(path, dlg.password_input.text())
        self._vault_opened()

    def close_vault(self):
        if self.session:
            try:
                self._normalize_files()
                self.session.save()
                self.session.close()
            except Exception:
                pass
        self.session = None
        self.list.clear()
        self.status.setText("No vault open")
        self.close_btn.setEnabled(False)
        self.extract_btn.setEnabled(False)

    def _vault_opened(self):
        self.status.setText("Vault OPEN")
        self.close_btn.setEnabled(True)

        self._normalize_files()

        self.list.clear()
        files = self.session.data.get("files", []) if self.session else []
        for i, f in enumerate(files):
            display = f'{f.get("name","")}{f.get("ext","")}'
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, i)
            self.list.addItem(item)

        self._on_select()

    def extract_selected(self):
        if not self.session:
            return

        items = self.list.selectedItems()
        if not items:
            return

        idx = items[0].data(Qt.UserRole)
        if idx is None:
            return

        files = self.session.data.get("files", [])
        if idx < 0 or idx >= len(files):
            return

        entry = files[idx]
        base = entry.get("name", "")
        ext = entry.get("ext", "")
        display = f"{base}{ext}"

        out, _ = QFileDialog.getSaveFileName(
            self, "Extract file", display, f"*{ext}" if ext else ""
        )
        if not out:
            return

        if ext and not out.lower().endswith(ext.lower()):
            out = out + ext

        with open(out, "wb") as fh:
            fh.write(bytes.fromhex(entry["content"]))

    def _on_select(self):
        self.extract_btn.setEnabled(bool(self.session and self.list.selectedItems()))


def run():
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        "CryptoVault.App"
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(icon_path))  

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
