import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import datetime,timedelta
import json




class Book:
    def __init__(self, title, author, book_id):
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
            'title': self.title,
            'author': self.author,
            'book_id': self.id,
            'available': self.available,
            'borrow_date': (self.borrow_date).isoformat() if self.borrow_date != None else None,
            'due_date': (self.due_date).isoformat() if self.due_date != None else None
        }

    def display_info(self):
        print(
            f"Title: {self.title.upper()}\nAuthor: {self.author.upper()}\nBook_id: {self.id}\nAvailable:{self.available}")


class User:
    def __init__(self, name, user_id, password):
        self.name = name
        self.user_id = user_id
        self.user_password = password
        self.borrowed_books = []

    def borrow_book(self, book_title, book_id):
        if len(self.borrowed_books) < 3:
            book_dict = {
                'book_title': book_title,
                'book_id': book_id
            }
            self.borrowed_books.append(book_dict)
            return True,f"Successfully borrowed book:{book_title}\nBook_id:{book_id}"
        else:
            return False,"Can not borrow more than three books."

    def return_book(self, book):

        self.borrowed_books.remove(book)

    def to_dict(self):
        return {
            'user_name': self.name,
            'user_id': self.user_id,
            'user_password': self.user_password,
            'borrowed_books': self.borrowed_books
        }

    def display_user_info(self):
        print(f"User name: {self.name.upper()}\nUser_id: {self.user_id}\nBorrowed Books: {self.borrowed_books}")


class Admin(User):
    def __init__(self, name, user_id, password):
        super().__init__(name, user_id, password)
        self.admin_password = password

    def check_password(self, entered_password):
        if entered_password == self.admin_password:
            return True
        else:
            return False


class Library:
    def __init__(self):
        self.list_of_books = []
        self.list_of_users = []
        self.admin = Admin("Leul Eyasu", 0, "leuleyasu123")
        self.load_data()

    def add_book(self,title,author):
        if not title or not author:
            return False,"Enter a valid input."
        new_book_id = [i.id for i in self.list_of_books]
        book_id = 1 if new_book_id == [] else max(new_book_id) + 1
        new_book = Book(title.lower(), author.lower(), book_id)
        self.list_of_books.append(new_book)
        self.save_data()
        return True,f"You have successfully added to the library.\nTitle: {title}\nAuthor: {author}\nBook_id: {book_id}"


    def remove_book(self,entered_book_id):
        found_book = self.find_book_by_id(entered_book_id)
        if not found_book:
            return False,"Book Id not found."

        if not found_book.available:
            return False,"Book is not available right now."

        self.list_of_books.remove(found_book)
        self.save_data()
        return True,f"You have removed the book\nTitle:{found_book.title}\nAuthor:{found_book.author}\nbook_id:{found_book.id}"

    def register_user(self,name,password):
        if not name or not password:
            return False,"Enter a valid input.",None
        new_user_id = [i.user_id for i in self.list_of_users]
        user_id = 1 if new_user_id == [] else max(new_user_id) + 1
        new_user = User(name, user_id, password)
        self.list_of_users.append(new_user)
        self.save_data()
        return True,f"You have successfully registered to the library.",new_user


    def lend_book(self,book_id,user_id,user_password):

        found_user = self.find_user_by_id(user_id)
        found_book = self.find_book_by_id(book_id)

        if not found_book:
            return False,"Book id not found."
        if not found_user:
            return False,"User_id not found."
        if found_user.user_password != user_password:
            return False,"Incorrect password."
        if not found_book.available:
            return False,"Book is not available right now."

        condition,message = found_user.borrow_book(found_book.title, found_book.id)
        if not condition:
            return False,message
        found_book.mark_borrowed()
        self.save_data()
        return True,message

    def accept_return(self,book_id,user_id,user_password):
        found_user = self.find_user_by_id(user_id)
        found_book = self.find_book_by_id(book_id)
        if not found_book:
            return False,"Book Id not found."
        if not found_user:
            return False,"User_id not found."
        if found_user.user_password != user_password:
            return False,"Incorrect password."
        if found_book.id not in [i.get('book_id') for i in found_user.borrowed_books]:
            return False,f"you haven't borrowed any\nbook named: {found_book.title} with book_id {book_id}"
        for i in found_user.borrowed_books:
            if i.get('book_id') == book_id:
                found_user.return_book(i)
                found_book.mark_returned()
                self.save_data()
                return True,f"User: {found_user.name} returned the book\n{found_book.title} with book_id: {found_book.id}"


    def search_book_by_title(self,title):
        if title.lower() in [i.title for i in self.list_of_books]:
            for i in self.list_of_books:
                if i.title.lower() == title.lower():
                    return True,f"Book Title: {title.upper()}\nAuthor: {i.author.upper()}\nBook_id: {i.id}\nAvailable: {i.available}\n"
        else:
            return False,f"No book with title: {title} was found."


    def save_data(self):
        # code to save the books
        list_books = [i.to_dict() for i in self.list_of_books]
        with open('books.json', 'w') as file:
            json.dump(list_books, file, indent=4)
        # code to load the users
        list_users = [i.to_dict() for i in self.list_of_users]
        with open('users.json', 'w') as file:
            json.dump(list_users, file, indent=4)

    def load_data(self):
        try:
            # cose to load the books
            with open('books.json', 'r') as file:
                data = json.load(file)
            for i in data:
                load_book = Book(i.get('title'), i.get('author'), i.get('book_id'))
                load_book.available = i.get('available')
                load_book.borrow_date = datetime.fromisoformat(i.get('borrow_date')) if i.get('borrow_date') != None else i.get('borrow_date')
                load_book.due_date = datetime.fromisoformat(i.get('due_date')) if i.get('due_date') != None else i.get(
                    'due_date')
                self.list_of_books.append(load_book)

            # code to load the user
            with open('users.json', 'r') as file2:
                data2 = json.load(file2)
            for j in data2:
                load_user = User(j.get('user_name'), j.get('user_id'), j.get('user_password'))
                load_user.borrowed_books = j.get('borrowed_books')
                self.list_of_users.append(load_user)
        except (json.JSONDecodeError,FileNotFoundError):
            print("Error while loading data.")
            return

    def check_overdue(self):
        time_now = datetime.now()
        found_overdue = False
        for book in self.list_of_books:
            if not book.available and time_now > book.due_date:
                for user in self.list_of_users:
                    if book.id in [i.get('book_id') for i in user.borrowed_books]:
                        found_overdue = True
                        return True,f"user:{user.name} borrowed:\nbook:{book.title}\nbook_id: {book.id}\nfor 7 days."
        if not found_overdue:
            return True,"NO overdue right now"


    def find_user_by_id(self, user_id):
        '''find the user object with the specified id'''
        for i in self.list_of_users:
            if user_id == i.user_id:
                return i
        return None

    def find_book_by_id(self, book_id):
        '''find the book object with the specified id'''
        for i in self.list_of_books:
            if i.id == book_id:
                return i
        return None


luna = Library()


#admin window page
def open_admin_page():
    #code to check if there is overdue
    def check_overdue_func():
        condition,message = luna.check_overdue()
        if condition:
            messagebox.showinfo(title="Overdue",message=message)
    #code to show user info in the admin page
    def show_user_info(list_box):
        try:
            for i in luna.list_of_users:
                if list_box.get(list_box.curselection()) == i.name:
                    messagebox.showinfo(title="Success", message=f"User Name: {i.name}\nUser id: {i.user_id}"
                                                                 f"\nBorrowed books:{[k.get('book_title') for k in i.borrowed_books]}")
        except tkinter.TclError:
            messagebox.showerror(title="Error", message="Select user name to see details")

    # code to refresh the books list in the admin page
    def refresh_book_list():
        books_list_box.delete(0, END)
        for m in range(len(luna.list_of_books)):
            books_list_box.insert(m, luna.list_of_books[m].title)
        books_list_box.config(height=5)

    #code to refresh the user list in the admin page
    def refresh_user_list(event):
        users_list_box.delete(0, END)
        for k in range(len(luna.list_of_users)):
            users_list_box.insert(k, luna.list_of_users[k].name)
        users_list_box.config(height=5)

    #opens a window to add a book
    def add_book_window():
        def send_input(event=None):
            book_title0 = book_title.get()
            book_author0 = book_author.get()
            condition,message = luna.add_book(book_title0.lower(),book_author0.lower())
            if not condition:
                messagebox.showerror(title="Error", message=message)
                return
            else:
                messagebox.showinfo(title="Success", message=message)
                add_book_page.destroy()
                refresh_books()
                refresh_book_list()

        add_book_page = Toplevel()
        add_book_page.title("Add Book")
        add_book_page.geometry("320x320")
        labeltop = Label(add_book_page, text="Add Book to the Library",font=('Arial', 13, 'bold','underline'), padx=50,pady=25)
        labeltop.pack()
        frame1 = Frame(add_book_page,pady=20)
        frame1.pack()
        label1 = Label(frame1,text="Book Title:",font=('Arial', 13, 'bold'))
        label1.pack(side="left")
        book_title = Entry(frame1, width=20,font=('Arial', 13))
        book_title.pack(side="right")
        frame2 = Frame(add_book_page,pady=20)
        frame2.pack()
        label2 = Label(frame2,text="Author:",font=('Arial', 13, 'bold'))
        label2.pack(side="left")
        book_author = Entry(frame2, width=20,font=('Arial', 13))
        book_author.pack(side="right")
        frame3 = Frame(add_book_page)
        frame3.pack()
        add_button = Button(frame3,text="Add Book",font=('Arial', 13, 'bold'),command=send_input)
        add_button.pack()
        add_book_page.bind("<Return>",send_input)

    #opens a window to remove a book
    def remove_book_window():
        def send_input(event=None):
            try:
                book_id0 = int(entered_book_id.get())
                condition,message = luna.remove_book(book_id0)
                if not condition:
                    messagebox.showerror(title="Error", message=message)
                    return
                else:
                    messagebox.showinfo(title="Success", message=message)
                    remove_book_page.destroy()
                    refresh_books()
                    refresh_book_list()
            except:
                messagebox.showerror(title="Error", message="Enter a valid book id.")

        remove_book_page = Toplevel()
        remove_book_page.title("Remove Book")
        remove_book_page.geometry("320x250")
        labeltop0 = Label(remove_book_page, text="Remove Book from the Library", font=('Arial', 13, 'bold', 'underline'),padx=50, pady=25)
        labeltop0.pack()
        frame1 = Frame(remove_book_page,pady=20)
        frame1.pack()
        label1 = Label(frame1,text="Book Id:",font=('Arial', 13, 'bold'))
        label1.pack(side="left")
        entered_book_id = Entry(frame1, width=10,font=('Arial', 13))
        entered_book_id.pack(side="right")
        frame2 = Frame(remove_book_page)
        frame2.pack()
        remove_button = Button(frame2,text='Remove Book',font=('Arial',13),command=send_input)
        remove_button.pack()
        remove_book_page.bind("<Return>",send_input)


    admin_name = luna.admin.name
    admin_page = Toplevel()
    admin_page.title("Admin page")
    admin_page.geometry("620x520")
    admin_photo = PhotoImage(file="icons/admin1.png")
    admin_label = Label(admin_page,image=admin_photo, text=f'Admin Name: {admin_name}', font=('Arial', 13, 'bold'),compound='left', padx=50,pady=25)
    admin_label.image = admin_photo
    admin_label.pack()
    frame0 = Frame(admin_page)
    frame0.pack()
    add_book = Button(frame0, text="Add Book",command=add_book_window)
    add_book.pack(side="left")
    remove_book = Button(frame0, text="Remove Book",command=remove_book_window)
    remove_book.pack(side="right")
    check_overdue = Button(frame0, text="Check Overdue",command=check_overdue_func)
    check_overdue.pack(side="right")
    frame1 = Frame(admin_page)
    frame1.pack()
    label1 = Label(frame1,text="Books in the Library:",font=('Arial',13,'bold','underline'),pady=20)
    label1.pack()
    books_list_box = Listbox(frame1,font=('Arial',13,'bold','underline'),width=50)
    books_list_box.pack()
    for m in range(len(luna.list_of_books)):
        books_list_box.insert(i,luna.list_of_books[m].title)
    books_list_box.config(height=5)
    book_info_button = Button(frame1,text='Show Book info',command=lambda:show_book_info(books_list_box))
    book_info_button.pack(side="bottom")
    frame2 = Frame(admin_page)
    frame2.pack()
    label2 = Label(frame2,text="Registered users:",font=('Arial',13,'bold','underline'),pady=20)
    label2.pack()
    users_list_box = Listbox(frame2,font=('Arial',13,'bold','underline'),width=50)
    users_list_box.pack()
    for k in range(len(luna.list_of_users)):
        users_list_box.insert(k,luna.list_of_users[k].name)
    users_list_box.config(height=5)
    user_info_button = Button(frame2,text='Show User info',command=lambda:show_user_info(users_list_box))
    user_info_button.pack(side="bottom")
    admin_page.bind("<Return>",refresh_user_list)

#users window page
def open_user_page(user_object):

    #code to process the return of a book
    def return_book_window():
        def send_input(event=None):
            try:
                book_id = int(entered_book_id.get())
                user_id = int(entered_user_id.get())
                password = entered_user_password.get()
                condition,message = luna.accept_return(book_id,user_id,password)
                if not condition:
                    messagebox.showerror(title="Error",message=message)
                    return
                messagebox.showinfo(title="Success",message=message)
                return_window.destroy()
                refresh_borrowed_list()
            except:
                messagebox.showerror(title="Error",message="Invalid Input")
                return
        if list_box.size() == 0:
            messagebox.showerror("Error", "No books found.")
            return
        return_window = Toplevel()
        return_window.title("Return Book")
        return_window.geometry("320x220")
        labeltop = Label(return_window, text="Return Borrowed Book:",font=('Arial',13,'bold','underline'),pady=20)
        labeltop.pack()
        frame0r = Frame(return_window,pady=5)
        frame0r.pack()
        labelr0 = Label(frame0r, text='Book_id:',font=('Arial',13,'bold'))
        labelr0.pack(side="left")
        entered_book_id = Entry(frame0r,font=('Arial',13),width=10)
        entered_book_id.pack(side="right")
        frame1r = Frame(return_window,pady=5)
        frame1r.pack()
        labelr1 = Label(frame1r, text='user_id:',font=('Arial',13,'bold'))
        labelr1.pack(side="left")
        entered_user_id = Entry(frame1r, font=('Arial',13),width=10)
        entered_user_id.pack(side="right")
        frame2r = Frame(return_window,pady=5)
        frame2r.pack()
        labelr2 = Label(frame2r, text='User_password:',font=('Arial',13,'bold'))
        labelr2.pack(side="left")
        entered_user_password = Entry(frame2r, font=('Arial',13),show="*",width=15)
        entered_user_password.pack(side="right")
        frame3r = Frame(return_window,pady=10)
        frame3r.pack()
        submit_button = Button(frame3r, text='Submit',command=send_input)
        submit_button.pack()
        return_window.bind("<Return>",send_input)

    #code to process the lending(borrowing) of a book
    def borrow_book_window():
        def send_input(event=None):
            try:
                book_id = int(entered_book_id.get())
                user_id = int(entered_user_id.get())
                user_password = entered_user_password.get()
                condition,message = luna.lend_book(book_id,user_id,user_password)
                if not condition:
                    messagebox.showerror(title="Error",message=message)
                    return
                messagebox.showinfo(title="Success",message=message)
                borrow_window.destroy()
                refresh_borrowed_list()
            except:
                messagebox.showerror(title="Error", message="Invalid input.")
                return

        borrow_window = Toplevel()
        borrow_window.title("Borrow Book")
        borrow_window.geometry("320x220")
        labeltop = Label(borrow_window, text="Borrow Book:", font=('Arial', 13, 'bold', 'underline'), pady=20)
        labeltop.pack()
        frame0r = Frame(borrow_window, pady=5)
        frame0r.pack()
        labelr0 = Label(frame0r, text='Book_id:', font=('Arial', 13, 'bold'))
        labelr0.pack(side="left")
        entered_book_id = Entry(frame0r, font=('Arial', 13), width=10)
        entered_book_id.pack(side="right")
        frame1r = Frame(borrow_window, pady=5)
        frame1r.pack()
        labelr1 = Label(frame1r, text='user_id:', font=('Arial', 13, 'bold'))
        labelr1.pack(side="left")
        entered_user_id = Entry(frame1r, font=('Arial', 13), width=10)
        entered_user_id.pack(side="right")
        frame2r = Frame(borrow_window, pady=5)
        frame2r.pack()
        labelr2 = Label(frame2r, text='User_password:', font=('Arial', 13, 'bold'))
        labelr2.pack(side="left")
        entered_user_password = Entry(frame2r, font=('Arial', 13), show="*", width=15)
        entered_user_password.pack(side="right")
        frame3r = Frame(borrow_window, pady=10)
        frame3r.pack()
        submit_button = Button(frame3r, text='Submit',command=send_input)
        submit_button.pack()
        borrow_window.bind("<Return>",send_input)

    def refresh_borrowed_list():
        list_box.delete(0, END)
        count0 = 0
        for i in user_object.borrowed_books:
            list_box.insert(count0, f"Book_title: {i.get('book_title')} / Book_id: {i.get('book_id')}")
            count0 += 1
        list_box.config(height=list_box.size())


    user_name = user_object.name
    user_id = user_object.user_id
    user_page = Toplevel()
    user_page.title("User_page")
    user_page.geometry("420x320")
    user_photo = PhotoImage(file='icons/user1.png')
    frame0 = Frame(user_page)
    frame0.pack()
    label = Label(frame0, image=user_photo,text='User_profile',font=('Arial', 13, 'bold'),compound="left",pady=25,padx=30)
    label.image = user_photo
    label.pack()
    frame1 = Frame(user_page)
    frame1.pack()
    label2 = Label(frame1,text=f'User_name: {user_name}\nUser_id: {user_id}\nBorrowed_books:', font=('Arial', 13, 'bold'),padx=50)
    label2.pack()
    frame2 = Frame(user_page,pady=10)
    frame2.pack()
    list_box = Listbox(frame2,width=50,font=('Arial',11,'bold'))
    list_box.pack(side='bottom')
    count = 1
    for i in user_object.borrowed_books:
        list_box.insert(count,f"Book_title: {i.get('book_title')} / Book_id: {i.get('book_id')}")
        count += 1
    list_box.config(height=list_box.size())

    frame3 = Frame(user_page,pady=10)
    frame3.pack()
    borrow_book = Button(frame3,text='Borrow_book',command=borrow_book_window)
    borrow_book.pack(side='left')
    return_book = Button(frame3,text='Return_book',command=return_book_window)
    return_book.pack(side='right')


#admin login page
def admin_login():
    def send_input(event=None):
        password = entered_password.get()
        if luna.admin.check_password(password):
            messagebox.showinfo(title="Login Successful", message="You have successfully logged in")
            admin_login_page.destroy()
            open_admin_page()
            return
        messagebox.showerror(title="Error", message="Access Denied")
        entered_password.delete(0, END)



    admin_login_page = Toplevel()
    admin_login_page.title("Admin Login Page")
    admin_login_page.geometry("320x250")
    frame = Frame(admin_login_page)
    frame.pack()
    label = Label(frame, text='Admin login:', font=('Arial', 13, 'bold','underline'), pady=50)
    label.pack()
    frame1 = Frame(admin_login_page)
    frame1.pack()
    label1 = Label(frame1,text='password:',font=('Arial',13,'bold'))
    label1.pack(side="left")
    entered_password = Entry(frame1,font=('Arial',13),show='*')
    entered_password.pack(side="right")
    frame2 = Frame(admin_login_page,pady=30)
    frame2.pack()
    login_button = Button(frame2,text='Log in',font=('Arial',13),command=send_input)
    login_button.pack(side="right")
    admin_login_page.bind("<Return>",send_input)

    return admin_login_page


#user singup window
def user_signup():

    def send_input(event=None):
        name = user_name.get()
        password = user_password.get()
        condition,message,user_object= luna.register_user(name,password)
        if not condition:
            messagebox.showerror(title="Error", message=message)
            return
        messagebox.showinfo(title="Success", message=message)
        user_signup_page.destroy()
        open_user_page(user_object)

    user_signup_page = Toplevel()
    user_signup_page.title("User sign-up Page")
    user_signup_page.geometry("320x320")
    label = Label(user_signup_page, text='Register here:', font=('Arial', 13, 'bold', 'underline'), pady=50)
    label.pack()
    frame = Frame(user_signup_page)
    frame.pack()
    label2 = Label(frame, text='User name:', font=('Arial', 13, 'bold'))
    label2.pack(side="left")
    user_name = Entry(frame,font=('Arial',13))
    user_name.pack(side="right")
    frame1 = Frame(user_signup_page,pady=20)
    frame1.pack()
    label1 = Label(frame1, text='Password:', font=('Arial', 13, 'bold'))
    label1.pack(side="left")
    user_password = Entry(frame1,font=('Arial',13),show='*')
    user_password.pack(side="right")
    frame2 = Frame(user_signup_page,padx=50,pady=10)
    frame2.pack()
    signup_button = Button(frame2,text='Sign up',font=('Arial',13),command=send_input)
    signup_button.pack(side="top")
    frame3 = Frame(user_signup_page,padx=50,pady=15)
    frame3.pack()
    label3 = Label(frame3, text='Already registered:', font=('Arial', 10))
    label3.pack(side="left")
    signing_button = Button(frame3, text='Login', font=('Arial', 13), command=lambda:user_login(user_signup_page))
    signing_button.pack(side="right")
    user_signup_page.bind("<Return>",send_input)
    return user_signup_page

#user login window
def user_login(old_window):
    #close the sing_up window
    old_window.destroy()
    def send_input(event=None):
        try:
            x_id = int(user_id.get())
            found_user = luna.find_user_by_id(x_id)
            if not found_user:
                messagebox.showerror(title="Login Error", message="User_id not found")
                return
            if found_user.user_password != user_password.get():
                messagebox.showerror(title="Login Error", message="Password incorrect")
                return
            messagebox.showinfo(title="Login Successful", message="Login Successful")
            open_user_page(found_user)
            user_login_page.destroy()
        except:
            messagebox.showerror(title="Error",message="Invalid user id")
            return

    user_login_page = Toplevel()
    user_login_page.geometry("320x320")
    user_login_page.title("User Log-in Page")
    label = Label(user_login_page, text='Log-in:', font=('Arial', 13, 'bold', 'underline'), pady=50)
    label.pack()
    frame0 = Frame(user_login_page)
    frame0.pack()
    label2 = Label(frame0, text='Enter id:', font=('Arial', 13, 'bold'))
    label2.pack(side="left")
    user_id = Entry(frame0,font=('Arial',13))
    user_id.pack(side="right")
    frame1 = Frame(user_login_page,pady=25)
    frame1.pack()
    label1 = Label(frame1, text='Password:', font=('Arial', 13, 'bold'))
    label1.pack(side="left")
    user_password = Entry(frame1,font=('Arial',13),show='*')
    user_password.pack(side="right")
    frame2 = Frame(user_login_page,padx=50,pady=25)
    frame2.pack()
    signing_button = Button(frame2, text='Login', font=('Arial', 13),command=send_input)
    signing_button.pack(side="right")
    user_login_page.bind("<Return>",send_input)


def show_book_info(list_box):
    try:
        for book in luna.list_of_books:
            if list_box.get(list_box.curselection()) == book.title:
                messagebox.showinfo(title="Book details:", message=f"Book title: {book.title}\nAuthor: {book.author}\n"
                                                               f"Book id: {book.id}\nAvailable: {book.available}")
                return
            if list_box.get(list_box.curselection()) not in [book.title for book in luna.list_of_books]:
                messagebox.showinfo(title='Failed',message="Book was not found,must be removed.")
                return
    except tkinter.TclError:
        messagebox.showerror(title="Error:",message="Select a book from the list to see the details")

def refresh_books():
    list_of_books.delete(0,END)
    for i in range(len(luna.list_of_books)):
        list_of_books.insert(i,luna.list_of_books[i].title)
    list_of_books.config(height=list_of_books.size())

def search_book(title):
    title = title.get()
    condition,message = luna.search_book_by_title(title.lower())
    if not condition:
        messagebox.showerror(title="Error:",message=message)
        return
    messagebox.showinfo(title=title,message=message)
def update(event):
    window_width = window.winfo_width()
    button_width = 90
    admin_profile.place(x=(window_width - button_width),y=0)

#Main window


window = Tk()

window.title("Smart Library")
window.geometry("720x520")
logo = PhotoImage(file='icons/library.png')
window.iconphoto(True,logo)
window.config()
window.update_idletasks()
profile_photo = PhotoImage(file='icons/user1.png')
book_photo = PhotoImage(file="icons/books1.png")
admin_photo = PhotoImage(file='icons/admin1.png')
search_icon = PhotoImage(file='icons/search2.png')

user_profile = Button(window,text='Profile',image=profile_photo,compound="left",width=90,command=user_signup,)
user_profile.image = profile_photo
user_profile.place(x=0,y=0)

logo_label = Label(window,image=book_photo,text="Smart Library",font=('Arial',18,'bold'),compound="left")
logo_label.image = book_photo
logo_label.pack()

admin_profile = Button(window,image=admin_photo,text='Admin',compound="right",width=90,command=admin_login)
admin_profile.image = admin_photo
admin_profile.place(x=window.winfo_width() - 90,y=0)

comment = Label(window,text='Books in our library:',font=('Arial',15,'underline','bold'),pady=50)
comment.pack(side="top")

search_bar = Frame(window)
search_bar.pack()

search_input = Entry(search_bar,width=25,font=('Arial',15),bg="#ffffff")
search_input.pack(side="left")

search_button = Button(search_bar,image=search_icon,command=lambda:search_book(search_input))
search_button.image = search_icon
search_button.pack(side="right")

frame = Frame(window)
frame.pack()
list_of_books = Listbox(frame,font=('Arial',15),width=50)
list_of_books.pack()
for i in range(len(luna.list_of_books)):
    list_of_books.insert(i,luna.list_of_books[i].title)
list_of_books.config(height=list_of_books.size())
info_button = Button(frame,text='Show info',command=lambda:show_book_info(list_of_books))
info_button.pack()
window.bind("<Configure>",update)
window.mainloop()