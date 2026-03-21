from datetime import datetime,timedelta
import json

class Book:
    def __init__(self,title,author,book_id):
        self.title = title
        self.author = author
        self.id = book_id
        self.available = True
        self.borrow_date = None
        self.due_date = None

    def mark_borrowed(self):
        date_now = datetime.now()
        self.available = False
        self.borrow_date = date_now
        self.due_date = (date_now + timedelta(days=7))

    def mark_returned(self):
        self.available = True
        self.borrow_date = None
        self.due_date = None

    def to_dict(self):
        return {
            'title':self.title,
            'author':self.author,
            'book_id':self.id,
            'available':self.available,
            'borrow_date':self.borrow_date.isoformat() if self.borrow_date != None else None,
            'due_date':self.due_date.isoformat() if self.due_date != None else None
        }
    def display_info(self):
        print(f"Title: {self.title.upper()}\nAuthor: {self.author.upper()}\nBook_id: {self.id}\nAvailable:{self.available}")


class User:
    def __init__(self,name,user_id,password):
        self.name = name
        self.user_id = user_id
        self.user_password = password
        self.borrowed_books = []

    def borrow_book(self,book_title,book_id):
        if len(self.borrowed_books) < 3:
            book_dict = {
                'book_title':book_title,
                'book_id':book_id
            }
            self.borrowed_books.append(book_dict)
            return True
        else:
            print("Can not borrow more than three books.")
            return False
    def return_book(self,book):

        self.borrowed_books.remove(book)

    def to_dict(self):
        return {
            'user_name':self.name,
            'user_id':self.user_id,
            'user_password':self.user_password,
            'borrowed_books':self.borrowed_books
        }

    def display_user_info(self):
        print(f"User name: {self.name.upper()}\nUser_id: {self.user_id}\nBorrowed Books: {self.borrowed_books}")



class Admin(User):
    def __init__(self, name, user_id,password):
        super().__init__(name, user_id,password)
        self.admin_password = password
    def check_password(self,entered_password):
        if entered_password == self.admin_password:
            return True
        else:
            print("Access denied.")
            return False



class Library:
    def __init__(self):
        self.list_of_books = []
        self.list_of_users = []
        self.admin = Admin("Leul Eyasu",0,"leuleyasu123")
        self.load_data()
        
    def add_book(self):
        password = input("Enter password: ")
        if self.admin.check_password(password):
            title = input("Enter the title of book: ")
            author = input("Enter the author of the book: ")
            new_book_id = [i.id for i in self.list_of_books]
            book_id = 1 if new_book_id == [] else max(new_book_id) + 1
            new_book = Book(title.lower(),author.lower(),book_id)
            self.list_of_books.append(new_book)
            print(f"\nyou have successfully added a book.")
            print(f"Title: {title}\nAuthor: {author}\nBook_id: {book_id}")

    def remove_book(self):
        password = input('Enter password: ')
        if self.admin.check_password(password):
            entered_book_id = int(input("Enter the book_id: "))
            found_book = self.find_book_by_id(entered_book_id)
            if not found_book:
                print("Book Id not found.")
                return
            if not found_book.available:
                print("Book is not available right now.")
                return
            
            print(f"You have removed the book:{found_book.title} by {found_book.author} with the book_id:{found_book.id}")
            self.list_of_books.remove(found_book)



    def register_user(self):
        user_name = input("Enter your name: ")
        user_password = input("Enter your password: ")
        new_user_id = [i.user_id for i in self.list_of_users]
        user_id = 1 if new_user_id == [] else max(new_user_id) + 1
        new_user = User(user_name,user_id,user_password)
        self.list_of_users.append(new_user)
        print("\nYou have successfully registered!")
        print(f"User_name: {user_name}\nUser_id: {user_id}")

    def lend_book(self):
        entered_book_id = int(input("Enter book_id: "))
        entered_user_id = int(input("Enter user_id: "))
        entered_user_password = input("Enter user_password: ")
        found_user = self.find_user_by_id(entered_user_id)
        found_book = self.find_book_by_id(entered_book_id)

        if not found_book:
            print("Book id not found.")
            return
        if not found_user:
            print("User id not found.")
            return
        if found_user.user_password != entered_user_password:
            print("Incorrect password.")
            return
        if not found_book.available:
            print("Book is not available right now.")
            return
        
        if found_user.borrow_book(found_book.title,found_book.id):
            print(f"User: {found_user.name} borrowed the book: {found_book.title},book_id: {found_book.id}")
            found_book.mark_borrowed()
        
    def accept_return(self):
        entered_book_id = int(input("Enter the book_id: "))
        entered_user_id = int(input("Enter user_id: "))
        entered_user_password = input("Enter user_password: ")
        found_user = self.find_user_by_id(entered_user_id)
        found_book = self.find_book_by_id(entered_book_id)
        if not found_book:
            print("Book id not found.")
            return
        if not found_user:
            print("User id not found.")
            return
        if found_user.user_password != entered_user_password:
            print("Incorrect password.")
            return
        if found_book.id not in [i.get('book_id') for i in found_user.borrowed_books]:
            print(f"you haven't borrowed any book named: {found_book.title} with book_id {entered_book_id}")
            return
        for i in found_user.borrowed_books:
            if i.get('book_id') == entered_book_id:
                print(f"User: {found_user.name} returned the book {found_book.title} with book_id: {found_book.id}")
                found_user.return_book(i)
                found_book.mark_returned()
                break

    def search_book_by_title(self):
        title = input("Enter the title of the book you want to find: ").lower()
        if title in [i.title for i in self.list_of_books]:
            print("\nResult:")
            print('='*10)
            for i in self.list_of_books:
                if i.title.lower() == title:
                    print(f"Book Title: {title.upper()}\nAuthor: {i.author}\nBook_id: {i.id}\nAvailable: {i.available}\n")
        else:
            print(f"\nNo book with title: {title} was found.")

    def save_data(self):
        #code to save the books
        list_books = [i.to_dict() for i in self.list_of_books ]
        with open('books.json','w') as file:
            json.dump(list_books,file,indent=4)
        #code to load the users
        list_users = [i.to_dict() for i in self.list_of_users]
        with open('users.json','w') as file:
            json.dump(list_users,file,indent=4)
    def load_data(self):
        try:
            # cose to load the books 
            with open('books.json','r') as file:
               data = json.load(file)
            for i in data:
                load_book = Book(i.get('title'),i.get('author'),i.get('book_id'))
                load_book.available = i.get('available')
                load_book.borrow_date = datetime.fromisoformat(i.get('borrow_date')) if i.get('borrow_date') != None else i.get('borrow_date')
                load_book.due_date = datetime.fromisoformat(i.get('due_date')) if i.get('due_date') != None else i.get('due_date')
                self.list_of_books.append(load_book)

            #code to load the user
            with open('users.json','r') as file2:
                data2 = json.load(file2)
            for j in data2:
                load_user = User(j.get('user_name'),j.get('user_id'),j.get('user_password'))
                load_user.borrowed_books = j.get('borrowed_books')
                self.list_of_users.append(load_user)
        except (json.JSONDecodeError,FileNotFoundError):
            print("Error while loading json file.")

    def check_overdue(self):
        password = input("Enter password: ")
        if self.admin.check_password(password):
            time_now = datetime.now()
            found_overdue = False
            for book in self.list_of_books:
                if not book.available and time_now > book.due_date:
                    for user in self.list_of_users:
                        if book.id in [i.get('book_id') for i in user.borrowed_books]:
                            print(f"user:{user.name} borrowed the book:{book.title},book_id: {book.id} for 7 days.")
                            found_overdue = True
            if not found_overdue:
                print("No overdue right now.")

    def show_books(self):
        print("="*20)
        print("Books in the Library.")
        print("="*20) 
        for i in self.list_of_books:
            i.display_info()
            print()


    def display_info(self):
        password = input("Enter password: ")
        if self.admin.check_password(password):    
            print("="*20)
            print("Admin of the Library.")
            print("="*20) 
            print(f"Admin_name: {self.admin.name}\n")

            print("="*20)
            print("Books in the Library.")
            print("="*20)
            for i in self.list_of_books:
                i.display_info()
                print()
            print("="*20)
            print("Registered users.")
            print("="*20)
            for i in self.list_of_users:
                i.display_user_info()
                print()
    

    def find_user_by_id(self,user_id):
        '''find the user object with the specified id'''
        for i in self.list_of_users:
            if user_id == i.user_id:
                return i
        return None
            
    def find_book_by_id(self,book_id):
        '''find the book object with the specified id'''
        for i in self.list_of_books:
            if i.id == book_id:
                return i
        return None





luna = Library()


def menu(option):
    if option == 1:
        luna.register_user()
    elif option == 2:
        luna.lend_book()
    elif option == 3:
        luna.accept_return()
    elif option == 4:
        luna.search_book_by_title()
    elif option == 5:
        luna.show_books()
    elif option == 6:
        luna.remove_book()
    elif option == 7:
        luna.add_book()
    elif option == 8:
       luna.check_overdue()
    elif option == 9:
        luna.display_info()
    elif option == 10:
        luna.save_data()
    else:
        print("Not recognized.")
print("Menu for Library Class")
while True:
    print("\nThese are the options you can use:")
    print("1.Register user\n2.Borrow book\n3.Return book\n4.Search book\n5.Show all books\n6.Remove a book(Admin)\n7.Add book(Admin)\n8.Check for overdue(Admin)\n9.Show library status(Admin)\n10.Save and Exit.\n")
    try:
        user_option = int(input("Enter the number on  your desired option: "))
        print()
        if user_option == 10:
            menu(user_option)
            break
        else:
            menu(user_option)
    except ValueError:
        print("Invalid Input.")
