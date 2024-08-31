from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout,    
    QHBoxLayout,
    QLabel, 
    QPushButton, 
    QListWidget, 
    QListWidgetItem, 
    QInputDialog, 
    QFileDialog, 
    QStackedWidget,
    QTextEdit,
    QScrollArea,
    QDialog
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .custom_widgets import QFlowLayout
from .book_card import BookCard

class BookList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.label = QLabel('Book List')
        self.label.setFont(QFont('Verdana', 16, QFont.Weight.Light))
        layout.addWidget(self.label)  # Add title to the layout.

        # Create QListWidget for displaying book cards.
        self.book_list_widget = QListWidget()
        self.book_list_widget.setFlow(QListWidget.LeftToRight)  # Arrange items horizontally
        self.book_list_widget.setWrapping(True)  # Wrap items to the next line if needed
        self.book_list_widget.setResizeMode(QListWidget.Adjust)  # Adjust size of items automatically
        layout.addWidget(self.book_list_widget)  # Add list widget to the layout.

        self.add_button = QPushButton('Add Book')  # Add book button
        self.add_button.setFixedWidth(400)
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)  # Add button to the layout

        # Center the Add Book button horizontally
        add_button_layout = QHBoxLayout()
        add_button_layout.addStretch()  # Add stretchable space to the left
        add_button_layout.addWidget(self.add_button)  # Add the button in the middle
        add_button_layout.addStretch()  # Add stretchable space to the right
        layout.addLayout(add_button_layout)  # Add the horizontal layout to the main layout

        # Stack to switch between book list and book details
        self.stacked_widget = QStackedWidget()  # Manages multiple child widgets (pages) but displays only one at a time.
        self.page_view = QWidget()  # Container for displaying book details when a book is selected.
        self.stacked_widget.addWidget(self.page_view)
        layout.addWidget(self.stacked_widget)  # Add stack widget to the layout.

        # Initialize the book details view
        self.page_layout = QVBoxLayout(self.page_view)
        self.page_view.setLayout(self.page_layout)

        # For testing, simulate loading books
        self.load_books()

    def load_books(self):
        # Simulate adding books; replace with database fetching logic
        self.add_book_card('Book 1', None)
        self.add_book_card('Book 2', None)
        self.add_book_card('Book 3', None)
        self.add_book_card('Book 4', None)
        self.add_book_card('Book 5', None)
        self.add_book_card('Book 6', None)
        self.add_book_card('Book 7', None)

    def add_book(self):
        title, ok = QInputDialog.getText(self, 'Add Book', 'Enter book title:')
        if ok and title:
            cover_path, _ = QFileDialog.getOpenFileName(self, 'Select Book Cover', '', 'Images (*.png *.xpm *.jpg)')
            self.add_book_card(title, cover_path)

    def add_book_card(self, title, cover_path):
        item = QListWidgetItem()
        book_card = BookCard(title, cover_path if cover_path else None)
        item.setSizeHint(book_card.sizeHint())
        self.book_list_widget.addItem(item)
        self.book_list_widget.setItemWidget(item, book_card)
        book_card.clicked.connect(lambda title=title: self.show_book_pages(title))

    def show_book_pages(self, title):
        self.stacked_widget.setCurrentWidget(self.page_view)
    
        # Clear any existing widgets in the page layout
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
        # Add a label to display the full book title
        title_label = QLabel(title)
        title_label.setWordWrap(True)  # Ensure the title is fully visible
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the font for the title label
        font = QFont('Arial', 12, QFont.Weight.Bold)  # Example: Arial, size 12, bold
        title_label.setFont(font)

        self.page_layout.addWidget(title_label)

        # Create a QScrollArea to hold the page buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(150)  # Set the desired height for the scroll area

        # Create a QWidget to hold buttons for each page
        page_buttons_widget = QWidget()
        page_buttons_layout = QFlowLayout(page_buttons_widget)

        # Set the scroll area's widget
        scroll_area.setWidget(page_buttons_widget)

        # Create a QWidget to hold the content area
        content_area_widget = QWidget()
        content_area_layout = QVBoxLayout(content_area_widget)
        self.page_content_area = content_area_widget        

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Add a button to allow adding new pages
        add_page_button = QPushButton('Add Page')
        add_page_button.clicked.connect(self.add_page)
        add_page_button.setFixedWidth(150)  # Set the desired width
        button_layout.addWidget(add_page_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Add a button to load more pages
        self.load_more_button = QPushButton('Load More Pages')
        self.load_more_button.clicked.connect(self.load_more_pages)
        self.load_more_button.setFixedWidth(150)  # Set the desired width
        button_layout.addWidget(self.load_more_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Add the scroll area with buttons to the main page layout
        self.page_layout.addWidget(scroll_area)
        self.page_layout.addWidget(content_area_widget)

        # Initialize page data
        self.page_buttons_layout = page_buttons_layout  # Save layout for adding new pages later
        self.page_content_layout = content_area_layout  # Save layout for adding new content later
        self.pages = []  # Track pages for dynamic content management
        self.current_page_index = 0  # Track current page index
        self.page_title = title  # Save the current book title

        # Add the button layout to the page layout
        self.page_layout.addLayout(button_layout)

        # Load initial set of pages
        self.load_more_pages()

    def load_more_pages(self):
        # Load a limited number of pages each time
        for i in range(self.current_page_index + 1, self.current_page_index + 41):
            self.add_page_to_view(i, f"Content of Page {i} for {self.page_title}")

        # Update the index for the next set of pages
        self.current_page_index += 40

    def show_page_content(self, page):
        # Create a new dialog window to display the page content
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Page {page}")

        # Create a layout for the dialog
        layout = QVBoxLayout(dialog)

        # Create a QTextEdit widget with the page content
        content_widget = QTextEdit(f"Content of Page {page}.")
        content_widget.setReadOnly(True)

        # Add the QTextEdit widget to the layout
        layout.addWidget(content_widget)

        # Set the dialog layout
        dialog.setLayout(layout)

        # Resize the dialog window and show it
        dialog.resize(500, 400)
        dialog.exec_()

    def add_page(self):
        page_title, ok = QInputDialog.getText(self, 'Add Page', 'Enter page title:')
        if ok and page_title:
            page_content, ok = QInputDialog.getMultiLineText(self, 'Page Content', 'Enter page content:')
            if ok and page_content:
                page_number = len(self.pages) + 1
                self.add_page_to_view(page_number, page_content, page_title)

    def add_page_to_view(self, page_number, content, title=None):
        """Add a new page with a button and content to a view in a PyQt application."""
        if not title:
            title = f"Page {page_number}"

        # Create the button and set the custom font
        button = QPushButton(title)
        button.setFont(QFont('Helvetica', 8, QFont.Weight.Light))  # Set the font to Helvetica, size 12, and bold

        button.clicked.connect(lambda checked, page=page_number: self.show_page_content(page))
        self.page_buttons_layout.addWidget(button)

        # Create the page content area
        page_content = QTextEdit(content)
        page_content.setReadOnly(True)
        page_content.setVisible(False)
        self.page_content_layout.addWidget(page_content)

        # Store the button and content for future reference
        self.pages.append((button, page_content))