import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Book:
    def __init__(self, title, author, subject):
        self.title = title
        self.author = author
        self.subject = subject
        self.availability = True
        # Load and display the image
        image_path = r"C:\Users\Lenovo\OneDrive\Documents\Desktop\DSA Project\library.jpg"  # Replace with the actual image path
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                background_label = tk.Label(self.root, image=photo)
                background_label.pack()
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print("Image file not found!")

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nSubject: {self.subject}\nAvailability: {'Available' if self.availability else 'Not Available'}\n"

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.borrowed_books = []

    def __str__(self):
        return self.username

    def return_book(self, book_title):
        for book in self.borrowed_books:
            if book.title == book_title:
                self.borrowed_books.remove(book)
                return book
        return None

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, title, author, subject):
        book = Book(title, author, subject)
        self.books.append(book)

    def remove_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                return
        messagebox.showinfo("Error", "Book not found!")

    def modify_book(self, title, new_title, new_author, new_subject):
        for book in self.books:
            if book.title == title:
                book.title = new_title
                book.author = new_author
                book.subject = new_subject
                return
        messagebox.showinfo("Error", "Book not found!")

    def search_books(self, query):
        matches = []
        for book in self.books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in book.subject.lower():
                matches.append(book)
        return matches

    def sort_books(self, key):
        if key == "title":
            self.books.sort(key=lambda x: x.title)
        elif key == "author":
            self.books.sort(key=lambda x: x.author)
        else:
            messagebox.showinfo("Error", "Invalid sorting key!")

    def display_books(self):
        if len(self.books) > 0:
            result = ""
            for book in self.books:
                result += str(book)
            return result
        else:
            return "The library catalog is empty!"

    def borrow_book(self, username, book_title):
        for user in self.users:
            if user.username == username:
                for book in self.books:
                    if book.title == book_title:
                        if book.availability:
                            book.availability = False
                            user.borrowed_books.append(book)
                            messagebox.showinfo("Success", f"{username} has borrowed {book.title}")
                            return
                        else:
                            messagebox.showinfo("Error", f"The book '{book.title}' is not available.")
                            return
                messagebox.showinfo("Error", "Book not found!")
                return
        messagebox.showinfo("Error", f"User '{username}' not found!")

    def return_book(self, book_title):
        for user in self.users:
            returned_book = user.return_book(book_title)
            if returned_book:
                for book in self.books:
                    if book.title == book_title:
                        book.availability = True
                        messagebox.showinfo("Success", f"{user.username} has returned {book.title}")
                        return
                messagebox.showinfo("Error", "Book not found!")
                return
        messagebox.showinfo("Error", f"User or book not found!")

    def register_user(self, username, password):
        for user in self.users:
            if user.username == username:
                messagebox.showinfo("Registration Error", "Username already exists!")
                return

        new_user = User(username, password)
        self.users.append(new_user)
        messagebox.showinfo("Registration Successful", "User registration completed!")

    def save_catalog(self, filename):
        with open(filename, "w") as file:
            for book in self.books:
                file.write(f"{book.title},{book.author},{book.subject},{book.availability}\n")

    def load_catalog(self, filename):
        self.books = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 4:
                        title, author, subject, availability = values
                        book = Book(title, author, subject)
                        book.availability = (availability == "True")
                        self.books.append(book)
        except FileNotFoundError:
            messagebox.showinfo("File Not Found", "The library catalog file was not found.")

class LibraryGUI:
    def __init__(self):
        self.library = Library()
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.set_background_image("lib.jpg")

        self.title_label = tk.Label(self.root, text="Library Management System", font=("Times New Roman", 18, "bold"))
        self.title_label.pack(pady=10)

        self.login_button = tk.Button(self.root, text="User Login", command=self.show_user_login)
        self.login_button.pack(pady=5)

        self.staff_login_button = tk.Button(self.root, text="Staff Login", command=self.show_staff_login)
        self.staff_login_button.pack(pady=5)

        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", "Fiction")
        self.library.add_book("1984", "George Orwell", "Fiction")
        self.library.add_book("Pride and Prejudice", "Jane Austen", "Fiction")
        self.library.add_book("The Catcher in the Rye", "J.D. Salinger", "Fiction")
        self.library.add_book("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy")
        self.library.add_book("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy")
        self.library.add_book("The Chronicles of Narnia", "C.S. Lewis", "Fantasy")
        self.library.add_book("The Da Vinci Code", "Dan Brown", "Mystery")
        self.library.add_book("The Hobbit", "J.R.R. Tolkien", "Fantasy")
        self.library.add_book("The Alchemist", "Paulo Coelho", "Fiction")
        self.library.add_book("The Hunger Games", "Suzanne Collins", "Young Adult")
        self.library.add_book("Moby-Dick", "Herman Melville", "Fiction")
        self.library.add_book("Brave New World", "Aldous Huxley", "Science Fiction")
        self.library.add_book("The Odyssey", "Homer", "Classics")

        self.root.mainloop()

    def set_background_image(self, image_path):
        if os.path.exists(image_path):
            try:
                image = tk.PhotoImage(file=image_path)
                background_label = tk.Label(self.root, image=image)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
            except tk.TclError:
                messagebox.showinfo("Error", "Failed to load image!")
        else:
            messagebox.showinfo("Error", "Image file not found!")


    def show_user_login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("User Login")

        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(login_window, text="Login", command=lambda: self.user_login(username_entry.get(), password_entry.get(), login_window))
        login_button.pack(pady=5)

    def user_login(self, username, password, window):
        for user in self.library.users:
            if user.username == username and user.password == password:
                messagebox.showinfo("Success", "User login successful!")
                self.show_user_options()
                window.destroy()
                return

        messagebox.showinfo("Error", "Invalid username or password!")

    def show_user_options(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("User Options")

        search_label = tk.Label(options_window, text="Search Query:")
        search_label.pack()
        search_entry = tk.Entry(options_window)
        search_entry.pack(pady=5)

        search_button = tk.Button(options_window, text="Search Books", command=lambda: self.search_books_user(search_entry.get()))
        search_button.pack(pady=5)

        display_button = tk.Button(options_window, text="Display Books", command=self.display_books_user)
        display_button.pack(pady=5)

        borrow_button = tk.Button(options_window, text="Borrow Book", command=self.show_borrow_book)
        borrow_button.pack(pady=5)

        return_button = tk.Button(options_window, text="return Book", command=self.show_return_book)
        return_button.pack(pady=5)


    def search_books_user(self, query):
        if query:
            matches = self.library.search_books(query)
            if len(matches) > 0:
                result = ""
                for book in matches:
                    status = "Available" if book.availability else "Not Available"
                    result += f"Title: {book.title}\nAuthor: {book.author}\nSubject: {book.subject}\nAvailability: {status}\n\n"
                messagebox.showinfo("Match Found", result)
            else:
                messagebox.showinfo("No Match", "No books found")
        else:
            messagebox.showinfo("Error", "Please enter a search query!")

    def display_books_user(self):
        result = self.library.display_books()
        messagebox.showinfo("Book Details", result)

    def show_borrow_book(self):
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Borrow Book")

        username_label = tk.Label(borrow_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(borrow_window)
        username_entry.pack(pady=5)

        title_label = tk.Label(borrow_window, text="Book Title:")
        title_label.pack()
        title_entry = tk.Entry(borrow_window)
        title_entry.pack(pady=5)

        borrow_button = tk.Button(borrow_window, text="Borrow", command=lambda: self.borrow_book(username_entry.get(), title_entry.get(), borrow_window))
        borrow_button.pack(pady=5)

    def borrow_book(self, username, book_title, window):
        if username and book_title:
            self.library.borrow_book(username, book_title)
            window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter the username and book title!")
    def show_return_book(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")

        username_label = tk.Label(return_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(return_window)
        username_entry.pack(pady=5)

        title_label = tk.Label(return_window, text="Book Title:")
        title_label.pack()
        title_entry = tk.Entry(return_window)
        title_entry.pack(pady=5)

        return_button = tk.Button(return_window, text="Return", command=lambda: self.return_book(username_entry.get(), title_entry.get(), return_window))
        return_button.pack(pady=5)

    def return_book(self, username, book_title, window):
        if username and book_title:
            for user in self.library.users:
                if user.username == username:
                    returned_book = user.return_book(book_title)
                    if returned_book:
                        for book in self.library.books:
                            if book.title == book_title:
                                book.availability = True
                                messagebox.showinfo("Success", f"{username} has returned {book.title}")
                                window.destroy()
                                return
                        messagebox.showinfo("Error", "Book not found!")
                    else:
                        messagebox.showinfo("Error", "The user did not borrow this book.")
                    window.destroy()
                    return
            messagebox.showinfo("Error", f"User '{username}' not found!")
        else:
            messagebox.showinfo("Error", "Please enter the username and book title!")

 

    def show_staff_login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Staff Login")

        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(login_window, text="Login", command=lambda: self.staff_login(username_entry.get(), password_entry.get(), login_window))
        login_button.pack(pady=5)

    def staff_login(self, username, password, window):
        if username == "staff" and password == "password":
            messagebox.showinfo("Success", "Staff login successful!")
            self.show_staff_options()
            window.destroy()
        else:
            messagebox.showinfo("Error", "Invalid username or password!")

    def show_staff_options(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Staff Options")

        add_button = tk.Button(options_window, text="Add New Book", command=self.show_add_book)
        add_button.pack(pady=5)

        remove_button = tk.Button(options_window, text="Remove Book", command=self.show_remove_book)
        remove_button.pack(pady=5)

        modify_button = tk.Button(options_window, text="Modify Book", command=self.show_modify_book)
        modify_button.pack(pady=5)

        search_button = tk.Button(options_window, text="Search Books", command=lambda: self.search_books_user(self.search_entry.get()))
        search_button.pack(pady=5)

        sort_button = tk.Button(options_window, text="Sort Books", command=self.show_sort_books)
        sort_button.pack(pady=5)

        display_button = tk.Button(options_window, text="Display Books", command=self.display_books_staff)
        display_button.pack(pady=5)

        borrow_button = tk.Button(options_window, text="Borrow Book", command=self.show_borrow_book)
        borrow_button.pack(pady=5)

        register_button = tk.Button(options_window, text="Register User", command=self.show_user_registration)
        register_button.pack(pady=5)


    def show_add_book(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")

        title_label = tk.Label(add_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack(pady=5)

        author_label = tk.Label(add_window, text="Author:")
        author_label.pack()
        author_entry = tk.Entry(add_window)
        author_entry.pack(pady=5)

        subject_label = tk.Label(add_window, text="Subject:")
        subject_label.pack()
        subject_entry = tk.Entry(add_window)
        subject_entry.pack(pady=5)

        add_button = tk.Button(add_window, text="Add", command=lambda: self.add_book(title_entry.get(), author_entry.get(), subject_entry.get(), add_window))
        add_button.pack(pady=5)

    def add_book(self, title, author, subject, window):
        if title and author and subject:
            self.library.add_book(title, author, subject)
            messagebox.showinfo("Success", "Book added successfully!")
            window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter all book details!")

    def show_remove_book(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Book")

        title_label = tk.Label(remove_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(remove_window)
        title_entry.pack(pady=5)

        remove_button = tk.Button(remove_window, text="Remove", command=lambda: self.remove_book(title_entry.get(), remove_window))
        remove_button.pack(pady=5)

    def remove_book(self, title, window):
        if title:
            self.library.remove_book(title)
            messagebox.showinfo("Success", "Book removed successfully!")
            window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter the book title!")

    def show_modify_book(self):
        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modify Book")

        title_label = tk.Label(modify_window, text="Title:")
        title_label.pack()
        title_entry = tk.Entry(modify_window)
        title_entry.pack(pady=5)

        new_title_label = tk.Label(modify_window, text="New Title:")
        new_title_label.pack()
        new_title_entry = tk.Entry(modify_window)
        new_title_entry.pack(pady=5)

        author_label = tk.Label(modify_window, text="Author:")
        author_label.pack()
        author_entry = tk.Entry(modify_window)
        author_entry.pack(pady=5)

        subject_label = tk.Label(modify_window, text="Subject:")
        subject_label.pack()
        subject_entry = tk.Entry(modify_window)
        subject_entry.pack(pady=5)

        modify_button = tk.Button(modify_window, text="Modify", command=lambda: self.modify_book(title_entry.get(), new_title_entry.get(), author_entry.get(), subject_entry.get(), modify_window))
        modify_button.pack(pady=5)

    def modify_book(self, title, new_title, author, subject, window):
        if title:
            self.library.modify_book(title, new_title, author, subject)
            messagebox.showinfo("Success", "Book modified successfully!")
            window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter the book title!")

    def show_sort_books(self):
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Books")

        sort_label = tk.Label(sort_window, text="Sort by:")
        sort_label.pack()

        sort_variable = tk.StringVar(sort_window)
        sort_variable.set("title")
        sort_optionmenu = tk.OptionMenu(sort_window, sort_variable, "title", "author")
        sort_optionmenu.pack(pady=5)

        sort_button = tk.Button(sort_window, text="Sort", command=lambda: self.sort_books(sort_variable.get(), sort_window))
        sort_button.pack(pady=5)

    def sort_books(self, key, window):
        self.library.sort_books(key)
        messagebox.showinfo("Success", "Books sorted successfully!")
        window.destroy()

    def display_books_staff(self):
        result = self.library.display_books()
        messagebox.showinfo("Book Details", result)

    def show_user_registration(self):
        registration_window = tk.Toplevel(self.root)
        registration_window.title("User Registration")

        username_label = tk.Label(registration_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(registration_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(registration_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(registration_window, show="*")
        password_entry.pack(pady=5)

        register_button = tk.Button(registration_window, text="Register", command=lambda: self.register_user(username_entry.get(), password_entry.get(), registration_window))
        register_button.pack(pady=5)

    def register_user(self, username, password, window):
        if username and password:
            self.library.register_user(username, password)
            window.destroy()
        else:
            messagebox.showinfo("Error", "Please enter a username and password!")
    def show_return_book(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")

        username_label = tk.Label(return_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(return_window)
        username_entry.pack(pady=5)

        title_label = tk.Label(return_window, text="Book Title:")
        title_label.pack()
        title_entry = tk.Entry(return_window)
        title_entry.pack(pady=5)

        return_button = tk.Button(return_window, text="Return", command=lambda: self.return_book(username_entry.get(), title_entry.get(), return_window))
        return_button.pack(pady=5)

    def return_book(self, username, book_title, window):
        if username and book_title:
            for user in self.library.users:
                if user.username == username:
                    returned_book = user.return_book(book_title)
                    if returned_book:
                        for book in self.library.books:
                            if book.title == book_title:
                                book.availability = True
                                messagebox.showinfo("Success", f"{username} has returned {book.title}")
                                window.destroy()
                                return
                        messagebox.showinfo("Error", "Book not found!")
                    else:
                        messagebox.showinfo("Error", "The user did not borrow this book.")
                    window.destroy()
                    return
            messagebox.showinfo("Error", f"User '{username}' not found!")
        else:
            messagebox.showinfo("Error", "Please enter the username and book title!")

 

if __name__ == "__main__":
    gui = LibraryGUI()
    gui.root.mainloop()
