from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QFont
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QHBoxLayout
)


class PasswordDialog(QDialog):
    def __init__(self, title="Vault Access", parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)

        self.resize(420, 220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 32, 36, 28)
        layout.setSpacing(12)

        self.title_label = QLabel(title, alignment=Qt.AlignCenter)
        title_font = QFont("Segoe UI", 13)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #6fe9ff; letter-spacing: 1px;")

        self.info_label = QLabel("Enter vault password", alignment=Qt.AlignCenter)
        self.info_label.setStyleSheet(
            "color: rgba(210,245,255,180); font-size: 12px;"
        )

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.ok_btn = QPushButton("CONFIRM")
        self.cancel_btn = QPushButton("CANCEL")

        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.ok_btn)

        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addSpacing(6)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addLayout(btn_row)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        self.ok_btn.setDefault(True)
        self.ok_btn.setAutoDefault(True)

        self.password_input.returnPressed.connect(self.accept)
        self.password_input.setFocus()


        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet("""
        QLabel {
            font-family: "Segoe UI";
        }

        QLineEdit {
            background-color: rgba(10, 16, 22, 120);
            border: 1px solid rgba(90, 220, 255, 150);
            border-radius: 6px;
            padding: 8px;
            color: #d8f6ff;
        }

        QLineEdit:focus {
            border: 1px solid rgba(0, 210, 255, 220);
        }

        QPushButton {
            background-color: rgba(16, 22, 28, 235);
            border: 1px solid rgba(90, 220, 255, 130);
            border-radius: 6px;
            padding: 8px;
            color: #d8f6ff;
        }

        QPushButton:hover {
            border: 1px solid rgba(90, 220, 255, 200);
            background-color: rgba(22, 30, 38, 245);
        }

        QPushButton:pressed {
            border: 1px solid rgba(255, 170, 90, 200);
            background-color: rgba(10, 14, 18, 255);
        }
        """)


    def _frame_path(self, r: QRectF):
        c = 20
        radius = 14
        x, y, w, h = r.x(), r.y(), r.width(), r.height()

        p = QPainterPath()
        p.moveTo(x + radius + c, y)
        p.lineTo(x + w - radius - c, y)
        p.quadTo(x + w - c, y, x + w - c, y + radius)
        p.lineTo(x + w, y + c + radius)
        p.lineTo(x + w, y + h - c - radius)
        p.quadTo(x + w, y + h - c, x + w - radius, y + h - c)
        p.lineTo(x + w - c - radius, y + h)
        p.lineTo(x + c + radius, y + h)
        p.quadTo(x + c, y + h, x + c, y + h - radius)
        p.lineTo(x, y + h - c - radius)
        p.lineTo(x, y + c + radius)
        p.quadTo(x, y + c, x + radius, y + c)
        p.closeSubpath()
        return p

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        r = QRectF(8, 8, self.width() - 16, self.height() - 16)
        path = self._frame_path(r)

        painter.setBrush(QColor(12, 16, 20, 245))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        glow = QPen(QColor(0, 210, 255, 80), 1.2)
        painter.setPen(glow)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        painter.setPen(QPen(QColor(0, 210, 255, 40), 8))
        painter.drawPath(path)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 140, 60, 160))
        painter.drawRoundedRect(
            QRectF(r.left() + 22, r.top() + 14, 44, 6),
            3, 3
        )

        painter.end()
