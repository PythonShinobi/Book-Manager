from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

class BookCard(QWidget):
    clicked = pyqtSignal(str)  # Signal to emit book title on click

    def __init__(self, title, cover_path=None):
        super().__init__()

        layout = QVBoxLayout(self)

        # Set up cover image
        self.cover_label = QLabel(self)
        if cover_path:
            self.cover_pixmap = QPixmap(cover_path)
        else:
            # Placeholder for cover
            self.cover_pixmap = QPixmap(110, 150)
            self.cover_pixmap.fill(Qt.GlobalColor.lightGray)
        
        self.cover_label.setPixmap(self.cover_pixmap)
        self.cover_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expand in both dimensions to take up as much space as possible within its layout.
        layout.addWidget(self.cover_label, Qt.AlignmentFlag.AlignHCenter)

        # Set up book title
        self.title_label = QLabel(title, self)
        layout.addWidget(self.title_label, Qt.AlignmentFlag.AlignCenter)

        # Set initial style        
        self.setCursor(QCursor(Qt.PointingHandCursor))  # Set cursor to a pointing hand

        # Set layout
        self.setLayout(layout)

    def mousePressEvent(self, event):
        """Automatically called whenever the user clicks on the BookCard widget."""
        self.clicked.emit(self.title_label.text())        
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setStyleSheet("border: 1px solid lightblue;")  # Highlight border on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("border: 1px solid transparent;")  # Remove highlight when not hovering
        super().leaveEvent(event)