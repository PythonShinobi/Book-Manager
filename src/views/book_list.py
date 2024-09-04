import logging
import qtawesome as qta
from sqlalchemy.exc import SQLAlchemyError
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,QVBoxLayout,QHBoxLayout,QLabel, QPushButton, 
    QListWidget,QListWidgetItem, QInputDialog, QScrollArea,
    QFileDialog, QStackedWidget, QTextEdit, QDialog, QMessageBox
)

from database.database import Session, Book, Page
from .custom_widgets import QFlowLayout, CustomInputDialog
from .book_card import BookCard

logging.basicConfig(level=logging.DEBUG)  # Set the logging level to DEBUG

class BookList(QWidget):
    def __init__(self):
        super().__init__()

        self.current_page_number = None

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
        self.add_button.clicked.connect(self.add_book_dialog)
        self.add_button.setIcon(qta.icon('fa.book'))  # Use the book icon        
        add_button_layout = QHBoxLayout()  # Center the Add Book button horizontally
        add_button_layout.addStretch()  # Add stretchable space to the left
        add_button_layout.addWidget(self.add_button)  # Add the button in the middle
        add_button_layout.addStretch()  # Add stretchable space to the right
        layout.addLayout(add_button_layout)  # Add the horizontal layout to the main layout

        # Stack to switch between book list and book details
        self.stacked_widget = QStackedWidget()  # Manages multiple child widgets (pages) but displays only one at a time.
        self.page_view = QWidget()  # Container for displaying the book's title and pages.
        self.page_layout = QVBoxLayout(self.page_view)
        self.page_view.setLayout(self.page_layout)
        self.stacked_widget.addWidget(self.page_view)
        layout.addWidget(self.stacked_widget)  # Add stack widget to the layout.

        self.load_books()

    def load_books(self):
        """Load books from the database."""
        try:
            # Create a new session for interacting with the database.
            session = Session()

            # Query the database to retrieve all records from the 'Book' table.
            # The result is a list of 'Book' objects.
            books = session.query(Book).all()

            # Iterate through each book retrieved from the database.
            for book in books:
                # Add a book card to the UI for each book, using its title and cover image path.
                self.add_book_card(book.title, book.cover_path)

        # Handle any SQLAlchemy-related errors that may occur during the process.
        except SQLAlchemyError as e:
            # Print an error message to the console if an exception occurs.
            print(f"Error loading books: {e}")

    def add_book_dialog(self):
        # Open a dialog to get text input from the user. 
        # The dialog has a title 'Add Book' and prompts the user to 'Enter book title:'.
        # 'title' will store the user's input, and 'ok' will be True if the user presses 'OK' and False if they cancel.
        title, ok = QInputDialog.getText(self, 'Add Book', 'Enter book title:')
        
        # Check if the user pressed 'OK' and entered a non-empty title.
        if ok and title:
            # Open a file dialog for the user to select a book cover image.
            # 'cover_path' stores the path to the selected file, and the second value is ignored (hence the '_').
            # The dialog title is 'Select Book Cover', and it filters files to show only image formats (png, xpm, jpg).
            cover_path, _ = QFileDialog.getOpenFileName(self, 'Select Book Cover', '', 'Images (*.png *.xpm *.jpg)')
            
            # Call the method to save the book's title and cover image path to the database.
            self.save_book_to_db(title, cover_path)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("An error occurred")
        msg_box.setInformativeText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()            

    def save_book_to_db(self, title, cover_path):
        """Save book to the databse."""
        session = Session()
        try:
            book = Book(title=title, cover_path=cover_path)
            session.add(book)
            session.commit()
            self.add_book_card(title, cover_path)
        except SQLAlchemyError as e:
            self.show_error_message(f"Error saving book to database: {e}")
        finally:
            session.close()            

    def add_book_card(self, title, cover_path):
        # Create a new QListWidgetItem, which is a container item for adding widgets to QListWidget.
        item = QListWidgetItem()

        # Create a new instance of BookCard, passing the title and cover_path.
        # If cover_path is not provided (None), pass None to the BookCard.
        book_card = BookCard(title, cover_path if cover_path else None)        

        # Set the size of the QListWidgetItem to match the size of the book_card widget.
        item.setSizeHint(book_card.sizeHint())

        # Add the QListWidgetItem (item) to the book_list_widget, which is presumably a QListWidget.
        self.book_list_widget.addItem(item)

        # Set the book_card widget to be displayed inside the item in the QListWidget.
        self.book_list_widget.setItemWidget(item, book_card)

        # Connect the clicked signal of the book_card to a function that shows the book pages.
        # The lambda function is used to pass the title of the book to the show_book_pages method.
        book_card.clicked.connect(lambda title=title: self.show_book_pages(title))

        # Connect the delete_requested signal to the delete_book method
        book_card.delete_requested.connect(lambda title=title: self.delete_book(title))

    def show_book_pages(self, title):
        # Clear any existing widgets from the page layout to prepare for new content.
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
        # Create and configure a QLabel to display the book title.
        title_label = QLabel(title)
        title_label.setWordWrap(True)  # Ensure the title wraps if it's too long for one line.
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the title.
    
        # Set the font of the title label (Arial, size 12, bold).
        font = QFont('Arial', 12, QFont.Weight.Bold)
        title_label.setFont(font)
    
        # Add the title label to the page layout.
        self.page_layout.addWidget(title_label)
    
        # Create a QScrollArea for displaying buttons that allow navigation through the pages.
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its content.
        scroll_area.setFixedHeight(150)  # Set the height of the scroll area.
    
        # Create a QWidget to hold the buttons, with a QFlowLayout to manage their arrangement.
        page_buttons_widget = QWidget()
        page_buttons_layout = QFlowLayout(page_buttons_widget)
    
        # Assign the page buttons widget to the scroll area.
        scroll_area.setWidget(page_buttons_widget)
    
        # Create a QWidget to serve as the content area where the page content will be displayed.
        content_area_widget = QWidget()
        content_area_layout = QVBoxLayout(content_area_widget)
    
        # Create a horizontal layout for the action buttons (Add Page, Load More Pages).
        button_layout = QHBoxLayout()
    
        # Create and configure an "Add Page" button, and connect it to the add_page method.
        add_page_button = QPushButton('Add Page')
        add_page_button.clicked.connect(self.add_page)
        add_page_button.setFixedWidth(150)  # Set a fixed width for the button.
        add_page_button.setIcon(qta.icon('fa.plus'))  # Set an icon for the button.
        button_layout.addWidget(add_page_button, alignment=Qt.AlignmentFlag.AlignLeft)
    
        # Create and configure a "Load More Pages" button, and connect it to the load_more_pages method.
        self.load_more_button = QPushButton('Load More Pages')
        self.load_more_button.clicked.connect(self.load_more_pages)
        self.load_more_button.setFixedWidth(150)  # Set a fixed width for the button.
        self.load_more_button.setIcon(qta.icon('fa.refresh'))  # Set an icon for the button.
        button_layout.addWidget(self.load_more_button, alignment=Qt.AlignmentFlag.AlignRight)
    
        # Add the scroll area (with page buttons) and the content area to the page layout.
        self.page_layout.addWidget(scroll_area)
        self.page_layout.addWidget(content_area_widget)
    
        # Initialize variables to track page data and layout:
        self.page_buttons_layout = page_buttons_layout  # Store the layout for adding buttons later.
        self.page_content_layout = content_area_layout  # Store the layout for displaying content.
        self.pages = []  # Initialize an empty list to track pages for dynamic management.
        self.current_page_index = -1  # Start before the first page
        self.page_title = title  # Store the current book title for reference.
    
        # Add the action button layout to the page layout.
        self.page_layout.addLayout(button_layout)
    
        # Load the initial set of pages from the database.
        self.load_more_pages()

    def add_page(self):
        page_title, ok = QInputDialog.getText(self, 'Add Page', 'Enter page title:')
        if ok and page_title:
            dialog = CustomInputDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                page_content = dialog.get_text()
                if page_content:
                    self.save_page_to_db(page_title, page_content)

    def save_page_to_db(self, title, content):
        try:
            session = Session()

            # Queries the Book table for a book with the title that matches self.page_title. 
            book = session.query(Book).filter(Book.title == self.page_title).one()

            # Queries the Page table for pages associated with the book.id and counts them.
            # The result is incremented by 1 to determine the page number for the new page.
            page_number = session.query(Page).filter(Page.book_id == book.id).count() + 1

            # Creates a new Page object with the provided number, content, title, and book_id.
            page = Page(number=page_number, content=content, title=title, book_id=book.id)

            # Adds the newly created Page object to the session, marking it 
            # to be inserted into the database upon commit.
            session.add(page)

            # Commits the transaction, making all changes made in the session permanent in the database.
            session.commit()
            self.add_page_to_view(page_number, content, title)
        except SQLAlchemyError as e:
            self.show_error_message(f"Error saving book to database: {e}")

    def load_more_pages(self):
        try:
            # Create a new session for interacting with the database.
            session = Session()
    
            # Query the database to find the book with the title matching 'self.page_title'.
            # Retrieve a single 'Book' object.
            book = session.query(Book).filter(Book.title == self.page_title).one()
    
            # Query the database for all pages associated with the book's ID,
            # ordered by the page number in ascending order.
            pages = session.query(Page).filter(Page.book_id == book.id).order_by(Page.number).all()
                        
            total_pages = len(pages)                   

            # Ensure there are pages to load
            if total_pages > 0:
                start_index = self.current_page_index + 1
                end_index = min(start_index + 40, total_pages)        
    
                # Loop through the pages, starting from the next page after the current one,
                # up to the next 40 pages or until the end of the list of pages.
                for i in range(start_index, end_index):                    
                    page = pages[i]
    
                    # Add the page content to the view using its number, content, and title.                    
                    self.add_page_to_view(page.number, page.content, page.title)                    
    
                # Update the current page index to reflect that more pages have been loaded.
                self.current_page_index = end_index - 1            
    
        # Handle any SQLAlchemy-related errors that may occur during the process.
        except SQLAlchemyError as e:        
            self.show_error_message(f"Error saving book to database: {e}")

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

    def show_page_content(self, page_number):
        """Display the content of a specific page in a dialog."""
        try:
            session = Session()

            # Query the database to find the page with the given number and the current book title.
            page = session.query(Page).filter(Page.number == page_number,
                                              Page.book.has(Book.title == self.page_title)).first()

            # Ensure exactly one result is found
            if not page:
                # Show a message dialog if the page is not found
                QMessageBox.warning(self, 'Page Not Found', f'Page {page_number} not found.')
                return
    
            # Set the current page number
            self.current_page_number = page_number
    
            # Create a new dialog window to display the page content
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Page {page_number}")

            # Create a layout for the dialog
            layout = QVBoxLayout(dialog)

            # Create a QTextEdit widget with the page content
            content_widget = QTextEdit(page.content)
            content_widget.setReadOnly(True)

            # Add the QTextEdit widget to the layout
            layout.addWidget(content_widget)
    
            # Create buttons for editing and closing the dialog
            button_box = QHBoxLayout()
            edit_button = QPushButton('Edit')
            delete_button = QPushButton('Delete')
            close_button = QPushButton('Close')
            button_box.addWidget(edit_button)
            button_box.addWidget(delete_button)
            button_box.addWidget(close_button)
            layout.addLayout(button_box)
    
            # Connect buttons to their respective slots
            edit_button.clicked.connect(lambda: self.enable_editing(content_widget, edit_button))
            delete_button.clicked.connect(lambda: self.delete_page(page, dialog))
            close_button.clicked.connect(dialog.accept)
            
            dialog.setLayout(layout)
            dialog.resize(500, 400)
            dialog.exec_()
    
        except SQLAlchemyError as e:
            self.show_error_message(f"Error saving book to database: {e}")

    def enable_editing(self, content_widget, edit_button):
        # Enable editing and change the button text to "Save"
        content_widget.setReadOnly(False)
        edit_button.setText('Save')
        edit_button.clicked.disconnect()  # Disconnect previous slot
        edit_button.clicked.connect(lambda: self.save_page_content(content_widget, edit_button))

    def save_page_content(self, content_widget, edit_button):
        """Save the edited content of a page to the database."""
        if self.current_page_number is None:
            QMessageBox.warning(self, 'No Page Selected', 'No page is currently selected for editing.')
            return

        new_content = content_widget.toPlainText()

        try:
            session = Session()

            # Find the page to update
            page = session.query(Page).filter(Page.number == self.get_current_page_number(),
                                              Page.book.has(Book.title == self.page_title)).first()

            if not page:
                QMessageBox.warning(self, 'Page Not Found', f'Page {self.current_page_number} not found.')
                return

            # Update the page content
            page.content = new_content
            session.commit()

            # Set the QTextEdit back to read-only
            content_widget.setReadOnly(True)
            edit_button.setText('Edit')
            edit_button.clicked.disconnect()
            edit_button.clicked.connect(lambda: self.enable_editing(content_widget, edit_button))

            QMessageBox.information(self, 'Success', 'Page content updated successfully.')

        except SQLAlchemyError as e:
            self.show_error_message(f"Error saving edited page: {e}")
    
    def get_current_page_number(self):
        """This method should return the current page number being edited/viewed"""      
        return self.current_page_number        

    def delete_page(self, page, dialog):
        """Delete the specified page and close the dialog."""
        try:
            # Create a new session for deletion
            delete_session = Session()
            
            # Query the page to ensure it's still valid and not attached
            page_to_delete = delete_session.query(Page).filter(Page.id == page.id).one()
            
            if page_to_delete:
                # Delete the page
                delete_session.delete(page_to_delete)
                delete_session.commit()

                QMessageBox.information(self, 'Page Deleted', f'Page {page.number} has been deleted.')

                # Remove the page content from the view
                for button, content in self.pages:
                    if button.text() == page.title:
                        button.deleteLater()
                        content.deleteLater()
                        self.pages.remove((button, content))
                        break

                dialog.accept()  # Close the dialog after deletion

                self.load_more_pages()
            else:
                self.show_error_message('Page not found')
    
        except SQLAlchemyError as e:
            delete_session.rollback()  # Rollback the session in case of error
            self.show_error_message(f"Error deleting page from database: {e}")
        finally:
            delete_session.close()  # Close the session after operations
    
    def delete_book(self, title):
        """Delete a book in the database."""
        reply = QMessageBox.question(self, 'Delete Book', f"Are you sure you want to delete '{title}'?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                session = Session()
                book = session.query(Book).filter(Book.title == title).one()
                session.delete(book)
                session.commit()                
                self.remove_book_card(title)  # Remove the book card from the UI
            except SQLAlchemyError as e:
                self.show_error_message(f"Error deleting book from database: {e}")    

    def remove_book_card(self, title):
        """Remove card from the Book List view."""
        for index in range(self.book_list_widget.count()):
            item = self.book_list_widget.item(index)
            book_card = self.book_list_widget.itemWidget(item)
    
            if book_card and hasattr(book_card, 'full_title') and book_card.full_title == title:
                self.book_list_widget.takeItem(index)  # Remove item from the QListWidget
                break