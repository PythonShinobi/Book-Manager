import qtawesome as qta
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QMainWindow,    
    QAction,
    QVBoxLayout,
    QWidget
)

from .book_list import BookList

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)

        self.book_list_view = BookList()
        layout.addWidget(self.book_list_view)

        self.setup_menu_bar()

        self.setWindowTitle('Book Manager')
        self.setGeometry(300, 100, 720, 600)
        
        # Set the minimum size to default size
        self.setMinimumSize(QSize(720, 600))

        # Set the window icon to a distinct icon
        self.setWindowIcon(qta.icon('fa.archive')) # Set the library icon

        self.setCentralWidget(self.central_widget)

    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        add_book_action = QAction('Add Book', self)
        add_book_action.triggered.connect(self.add_book)
        file_menu.addAction(add_book_action)

        # Add more actions as needed

    def add_book(self):
        self.book_list_view.add_book()