print("This is our library!")

#Book class and methods
class Book:
    id = 0
    name = ""
    quantity = 5
    def __init__(self, id, name, quantity)
        self.id = id
        self.name = name
        self.quantity = quantity
    def askbook(self):
        input("Which book would you like. We have any book you could imagine!")
    def display_profile(self):
        return f"Book: {self.name} | Quantity: {self.quantity} | ID: {self.id}"
    def borrow_book(self):
        if self.quantity > 0:
            self.quantity -= 1
            return f"You have borrowed {self.name}. Remaining quantity: {self.quantity}"
        else:
            return f"Sorry, {self.name} is currently unavailable."
    def return_book(self):
        self.quantity += 1
        return f"You have returned {self.name}. Current quantity: {self.quantity}"
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        return f"Quantity of {self.name} updated to {self.quantity}"
    def check_availability(self):
        if self.quantity > 0:
            return f"{self.name} is available. Quantity: {self.quantity}"
        else:
            return f"{self.name} is currently unavailable."



#User class and methods
class User:
    id = 0
    name = ""
    borrowed_books = []
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.borrowed_books = []
    def display_profile(self):
        return f"User: {self.name} | ID: {self.id} | Borrowed Books: {[book.name for book in self.borrowed_books]}"
    def borrow_book(self, book):
        if book.quantity > 0:
            book.borrow_book()
            self.borrowed_books.append(book)
            return f"{self.name} has borrowed {book.name}."
        else:
            return f"Sorry, {book.name} is currently unavailable."
    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return f"{self.name} has returned {book.name}."
        else:
            return f"{self.name} did not borrow {book.name}."
