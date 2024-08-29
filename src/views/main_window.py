from PyQt5.QtWidgets import (
    QMainWindow,    
    QAction,
    QVBoxLayout,
    QWidget
)

from .book_list import BookList
from .book_detail import BookDetail

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Book Manager')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.book_list_view = BookList()
        self.book_detail_view = BookDetail()

        layout.addWidget(self.book_list_view)
        layout.addWidget(self.book_detail_view)

        self.setup_menu_bar()

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        add_book_action = QAction('Add Book', self)
        add_book_action.triggered.connect(self.add_book)
        file_menu.addAction(add_book_action)

        # Add more actions as needed

    def add_book(self):
        pass