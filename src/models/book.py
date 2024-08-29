# This model will handle book data and interaction with the backend (if applicable in the future).
class Book:
    def __init__(self, title, image_path, pages) -> None:
        self.title = title
        self.image_path = image_path
        self.pages = pages

    def add_page(self, page_content):
        self.pages.append(page_content)

    def update_page(self, index, new_content):
        if 0 <= index < len(self.pages):
            self.pages[index] = new_content

    def delete_page(self, index):
        if 0 <= index < len(self.pages):
            del self.pages[index]