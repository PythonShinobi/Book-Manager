from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

class BookCard(QWidget):
    clicked = pyqtSignal(str)  # Signal to emit book title on click

    def __init__(self, title, cover_path=None):
        super().__init__()

        self.full_title = title  # Store the full title

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

        # Set up book title with placeholder text
        self.title_label = QLabel(self)  # Create the label first
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expand horizontally, but fixed height
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align text to center
        self.title_label.setWordWrap(False)  # Disable word wrapping
        layout.addWidget(self.title_label, Qt.AlignmentFlag.AlignCenter)

        # Set initial style        
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Set cursor to a pointing hand

        # Set layout
        self.setLayout(layout)

        # Update the title label with ellipsized text
        self.update_title(self.full_title)

        # Set the tooltip to the full title
        self.title_label.setToolTip(self.full_title)

    def elide_title(self, title):
        """Ellipsizes the title to fit within the label's width."""
        metrics = self.title_label.fontMetrics()
        elided_text = metrics.elidedText(title, Qt.TextElideMode.ElideRight, self.title_label.width())
        return elided_text

    def update_title(self, title):
        """Update the label text with ellipsized version."""
        self.title_label.setText(self.elide_title(title))

    def resizeEvent(self, event):
        """Recalculate elided text on resize."""
        self.update_title(self.full_title)
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Automatically called whenever the user clicks on the BookCard widget."""
        self.clicked.emit(self.full_title)  # Emit the full title
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setStyleSheet("border: 1px solid lightblue;")  # Highlight border on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("border: 1px solid transparent;")  # Remove highlight when not hovering
        super().leaveEvent(event)