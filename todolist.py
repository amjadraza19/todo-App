import mysql.connector

HOST = 'localhost'
USER = 'root'
PASSWORD = 'Amjad1912@'
DATABASE = 'user_management'

conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    );
""")
conn.commit()

class TodoList:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        if username in self.users:
            print("Username is already Exist.Please select different username")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            self.users[username] = password
            print("User created successfully!")

    def login(self, username, password):
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        print("\n")
        print("\n")
        print("Hey congrats....Now you are in the Todo App.\n")
        if user:
            return user
        else:
            print("Invalid username or password")
            return None

    def main_menu(self):
        while True:
            print("\n Select your choice: ")
            print("1. Create new User ")
            print("2. Login a existing user")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                username = input("Enter a username: ")
                password = input("Enter the password: ")
                self.create_user(username, password)
            elif choice == '2':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.login(username, password)
                if user:
                    self.user_menu(user)
            elif choice == '3':
                print("Now you are Exit.Good Bye....")
                break
            else:
                print("Invalid choice...Please try Again.")

    def user_menu(self, user):
        while True:
            print("\n Enter the number")
            print("A. Create a List")
            print("B. Update List")
            print("C. Delete List")
            print("D. view todo list")
            print("E. Exit")

            choice = input("Enter your choice: ")
            if choice == 'A':
                self.create_list(user)
            elif choice == 'B':
                self.update_list(user)
            elif choice == 'C':
                self.delete_list(user)
            elif choice == 'D':
                self.view_lists(user)
            elif choice == 'E':
                print("Now you are exit....")
                break
            else:
                print("Invalid choice...Please try again.")

    def create_list(self, user):
        list_name = input("Enter new list: ")
        cursor.execute("INSERT INTO todo_lists (user_id, name) VALUES (%s, %s)", (user[0], list_name))
        conn.commit()
        print("Todo list added succesfully...")

    def update_list(self, user):
        list_id = input("Enter list id: ")
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE todo_lists SET name = %s WHERE id = %s AND user_id = %s", (new_name, list_id, user[0]))
        conn.commit()
        print("Succesfully updated list item.")

    def delete_list(self, user):
        list_id = input("Enter list id: ")
        cursor.execute("DELETE FROM todo_lists WHERE id = %s AND user_id = %s", (list_id, user[0]))
        conn.commit()
        print("Delete list item..")

    def view_lists(self, user):
        cursor.execute("SELECT * FROM todo_lists WHERE user_id = %s", (user[0],))
        view_lists = cursor.fetchall()
        for todo_lists in view_lists:
            print(f"Lists :{todo_lists[1]}")

if __name__ == '__main__':
    todo_lists = TodoList()
    todo_lists.main_menu()
    conn.close()