from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout,    
    QLabel, 
    QPushButton, 
    QListWidget, 
    QListWidgetItem, 
    QInputDialog, 
    QFileDialog, 
    QStackedWidget,
    QTextEdit,
    QScrollArea
)

from .custom_widgets import QFlowLayout
from .book_card import BookCard

class BookList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.label = QLabel('Book List')
        layout.addWidget(self.label)

        # Create QListWidget for displaying book cards
        self.book_list_widget = QListWidget()
        self.book_list_widget.setFlow(QListWidget.LeftToRight)  # Arrange items horizontally
        self.book_list_widget.setWrapping(True)  # Wrap items to the next line if needed
        self.book_list_widget.setResizeMode(QListWidget.Adjust)  # Adjust size of items automatically

        # Create QScrollArea and set the QListWidget as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.book_list_widget)
        layout.addWidget(scroll_area)

        self.add_button = QPushButton('Add Book')  # Add book button
        self.add_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_button)

        # Stack to switch between book list and book details
        self.stacked_widget = QStackedWidget()  # Manages multiple child widgets (pages) but displays only one at a time.
        self.page_view = QWidget()  # Container for displaying book details when a book is selected.
        self.stacked_widget.addWidget(self.page_view)
        layout.addWidget(self.stacked_widget)

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
    
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
        self.page_layout.addWidget(QLabel(f'Pages for {title}'))
    
        # Create a QWidget to hold buttons for each page
        page_buttons_widget = QWidget()  # Acts as a container for the buttons that represent different pages.
        page_buttons_layout = QFlowLayout(page_buttons_widget)
    
        # Create a QWidget to hold the content area
        content_area_widget = QWidget()
        content_area_layout = QVBoxLayout(content_area_widget)
        self.page_content_area = content_area_widget
    
        # Add buttons for each page
        for i in range(1, 20):  # Simulated pages
            button = QPushButton(f'Page {i}')
            button.clicked.connect(lambda checked, page=i: self.show_page_content(page))
            page_buttons_layout.addWidget(button)
    
            # Add a QTextEdit for each page content (initially hidden)
            page_content = QTextEdit(f"Content of Page {i} for {title}.")
            page_content.setReadOnly(True)
            page_content.setVisible(False)
            content_area_layout.addWidget(page_content)
    
        self.page_layout.addWidget(page_buttons_widget)
        self.page_layout.addWidget(content_area_widget)

    def show_page_content(self, page_number):
        # Initially hide all page contents.
        for i in range(self.page_content_area.layout().count()):
            widget = self.page_content_area.layout().itemAt(i).widget()
            if isinstance(widget, QTextEdit):
                widget.setVisible(False)

        # Show the selected page content
        content_widget = self.page_content_area.layout().itemAt(page_number - 1).widget()
        if isinstance(content_widget, QTextEdit):
            content_widget.setVisible(True)

    def add_page(self):
        page_title, ok = QInputDialog.getText(self, 'Add Page', 'Enter page title:')
        if ok and page_title:
            page_content, ok = QInputDialog.getMultiLineText(self, 'Page Content', 'Enter page content:')
            if ok and page_content:
                self.page_layout.addWidget(QLabel(f'{page_title}: {page_content}'))