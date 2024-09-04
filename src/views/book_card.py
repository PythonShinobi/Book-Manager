from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor, QFont, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton, QSpacerItem, QGraphicsDropShadowEffect

class BookCard(QWidget):
    clicked = pyqtSignal(str)  # Signal to emit book title on click
    delete_requested = pyqtSignal(str)

    def __init__(self, title, cover_path=None):
        super().__init__()

        self.full_title = title  # Store the full title

        # Set fixed size for the BookCard
        self.setFixedSize(150, 250)  # Width: 150, Height: 250, adjust as needed

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Set margins around the layout
        layout.setSpacing(10)  

        # Set up cover image
        self.cover_label = QLabel(self)
        self.cover_label.setFixedSize(110, 150)  # Fixed size for cover image
        self.cover_label.setPixmap(self.load_cover(cover_path))
        self.cover_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fixed size policy
        layout.addWidget(self.cover_label, Qt.AlignmentFlag.AlignHCenter)

        # Set up book title with placeholder text
        self.title_label = QLabel(self)  # Create the label first
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expand horizontally, but fixed height
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align text to the left
        self.title_label.setWordWrap(True)  # Enable word wrapping if needed
        self.title_label.setFont(QFont('Merriweather', 10, QFont.Weight.Light))
        layout.addWidget(self.title_label, Qt.AlignmentFlag.AlignLeft)  # Align left in layout

        # Add spacer item before the button to center it
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(70)
        self.delete_button.setStyleSheet(
            "QPushButton {"
            "border-radius: 5px;"  # Reduced border-radius for a tighter look
            "padding: 3px;"  # Reduced padding to ensure hover effect stays within button height
            "background-color: darkgray;"
            "}"
            "QPushButton:hover {"
            "background-color: gray;"
            "}"
            "QPushButton:pressed {"
            "background-color: darkgray;"
            "}"
        )
        self.delete_button.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.delete_button, Qt.AlignmentFlag.AlignHCenter)  # Center button horizontally

        # Add spacer item after the button to center it
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set initial style        
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Set cursor to a pointing hand

        # Apply shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)  # Adjust blur radius as needed
        shadow_effect.setOffset(5, 5)    # Adjust offset for shadow position
        shadow_effect.setColor(QColor(0, 0, 0, 160))  # Set shadow color and transparency
        self.setGraphicsEffect(shadow_effect)

        # Set layout
        self.setLayout(layout)

        # Update the title label with ellipsized text
        self.update_title(self.full_title)

        # Set the tooltip to the full title
        self.title_label.setToolTip(self.full_title)

    def load_cover(self, cover_path):
        """Load cover image or use placeholder if not available."""
        if cover_path:
            pixmap = QPixmap(cover_path)
        else:
            pixmap = QPixmap(110, 150)
            pixmap.fill(Qt.GlobalColor.lightGray)
        return pixmap

    def elide_title(self, title):
        """Ellipsizes the title to fit within the label's width, considering the number of characters."""
        max_characters = 15  # Define the maximum number of characters to display

        # If the title exceeds the character limit, truncate and append ellipsis
        if len(title) > max_characters:
            truncated_title = title[:max_characters] + '...'
        else:
            truncated_title = title

        # Now perform the ellipsis based on the width if needed
        metrics = self.title_label.fontMetrics()
        elided_text = metrics.elidedText(truncated_title, Qt.TextElideMode.ElideRight, self.title_label.width())
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

    def on_delete_clicked(self):
        self.delete_requested.emit(self.full_title)
