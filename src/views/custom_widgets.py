import qtawesome as qta
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize, QPoint, QRect
from PyQt5.QtWidgets import (
    QLayout, QSizePolicy, QDialog, QTextEdit,
    QVBoxLayout, QPushButton, QHBoxLayout, QLabel
)

class QFlowLayout(QLayout):
    """This custom layout allows the buttons to wrap around automatically when they 
    reach the edge of the container. It arranges the widgets in a flow, similar to how 
    text wraps in a document."""
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.item_list = []

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize(0, 0)
        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.spacing(), 2 * self.spacing())
        return size

    def doLayout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.item_list:
            wid = item.widget()
            space_x = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            space_y = self.spacing() + wid.style().layoutSpacing(
                QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
    
class CustomInputDialog(QDialog):
    """
    The `CustomInputDialog` class creates a dialog with a `QTextEdit` widget for multi-line text input and an "OK" button. 
    
    - **Initialization**: Sets the dialog's title and minimum size.
    - **Layout Management**: Uses a vertical layout to place the `QTextEdit` for user input.
    - **Button Layout**: Uses a horizontal layout to position the "OK" button, which closes the dialog when clicked.
    
    The dialog allows users to input and confirm text, which can be retrieved using the `get_text()` method.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Page Content')
        self.setMinimumSize(600, 400)  # Set a larger minimum size for the dialog
        
        layout = QVBoxLayout()
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Enter page content:')
        layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_text(self):
        return self.text_edit.toPlainText()    
    
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        self.setFixedSize(400, 300)  # Adjusted size to give more space for content

        # Set an icon for the dialog window
        self.setWindowIcon(qta.icon('fa.info-circle'))

        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout()

        # Set up the information label with improved font and padding
        info_label = QLabel(
            "Book Manager is a desktop application designed to help users manage their book collection.\n\n"
            "Features include:\n"
            "- Adding books to the collection\n"
            "- Add pages for a specific book\n"
            "- Deleting the pages of a book\n"
            "- Deleting books from the collection\n\n"
            "This application is ideal for recording the information you read in books.\n\n"
            "Note: To save book covers, you should manually edit the covers to fit the specified size: "
            "110 width and 150 height."
        )
        info_label.setFont(QFont('Merriweather', 11, QFont.Weight.Normal))  # Set a more elegant font
        info_label.setStyleSheet("padding: 10px; color: #333;")  # Add padding and set text color
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Add a separator line (optional)
        separator = QLabel()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #cccccc; margin: 10px 0;")
        layout.addWidget(separator)

        # Set up the OK button with custom styling
        ok_button = QPushButton("OK")
        ok_button.setFont(QFont('Merriweather', 10, QFont.Weight.Bold))
        ok_button.setStyleSheet(
            "QPushButton {"
            "background-color: #007BFF;"  # Bootstrap primary blue color
            "color: white;"
            "border-radius: 5px;"
            "padding: 8px 16px;"
            "}"
            "QPushButton:hover {"
            "background-color: #0056b3;"
            "}"
            "QPushButton:pressed {"
            "background-color: #004085;"
            "}"
        )
        ok_button.clicked.connect(self.accept)  # Close the dialog when clicked
        ok_button.setFixedWidth(80)  # Set a fixed width for the button
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)  # Change cursor to pointing hand on hover
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the button horizontally

        self.setLayout(layout)