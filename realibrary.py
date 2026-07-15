
name=input("Whats your name")
userid=147
print("Welcome to our library", name, "Your user id is", userid)
userid=int(input("Verification before you can begin what is your id "))
if userid==147:
    print("You can move on ")
elif userid!=147:
    print("This is not your user ID.")
    userid=int(input("Try again. What is your id"))
    
    
class pickbook:
    quantity=0
    books="hello"
    available_books = {
        1: "The Hobbit",
        2: "1984",
        3: "To Kill a Mockingbird",
        4: "Pride and Prejudice",
        5: "The Great Gatsby",
        6: "Fahrenheit 451",
        7: "Moby Dick",
        8: "The Catcher in the Rye",
        9: "Brave New World",
        10: "War and Peace"
    }
    def borrow_book(self):
        while True:
            try:
                self.quantity=int(input("How many books would you like"))
            except ValueError:
                    print("Not a valid number")
                    continue
            
            if self.quantity>=6:
                    print("You can only borrow 5 books at a time")
                    continue
            elif self.quantity<=0:
                    print("If you don't want a book, please exit the library")
                    exit()
            else:
                break
        print("\nHere are the books available:")
        for number, title in self.available_books.items():
            print(f"{number}. {title}")

        self.book=[]
        
        for i in range(self.quantity):
             while True:
                try:
                     choice = int(input(f"\nEnter the number of your book number {i+1}"))
                except ValueError:
                    print("Enter a number")
                    continue
                if choice in self.available_books:
                    self.books.append(self.available_books[choice])
                    break
                else:
                     print("That number isn't on the list. Enter a valid number")
        print(f"You picked: {', '.join(self.books)}.")

                
        
        
     
library=pickbook()
library.borrow_book()

