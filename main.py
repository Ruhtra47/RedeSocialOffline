import sqlite3
from getpass import getpass
from sys import exit
import keyboard

accounts_conn = sqlite3.connect("accounts.db")
accounts_cursor = accounts_conn.cursor()
accounts_cursor.execute('''CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY, email TEXT NOT NULL, password TEXT NOT NULL)''')

posts_conn = sqlite3.connect("posts.db")
posts_cursor = posts_conn.cursor()
posts_cursor.execute('''CREATE TABLE IF NOT EXISTS Posts (id INTEGER PRIMARY KEY, author TEXT NULL, content TEXT NOT NULL)''')

class Intro:
    def menu(self):
        print("""Select your action:\n[1] Login\n[2] Register\n[3] Exit""")
        option = int(input())
        if option == 1:
            self.login()
        elif option == 2:
            self.register()
        elif option == 3:
            exit()
        else:
            print("Unknown option, please try again.")
            self.menu()


    def login(self):
        email = input('Enter your email: ')
        password = getpass("Enter your password: ")

        data = accounts_cursor.execute('''SELECT * FROM Accounts''')

        user_found = False

        for account in data:
            cur_email = account[1]
            cur_passwd = account[2]

            if cur_email == email and cur_passwd == password:
                user_found = True
                main = Main(email)
                main.main()
        if not user_found:
            print("No user found. Want to register? [y/n] ")
            register_option = input().lower()
            if register_option == 'y':
                self.register()
            else:
                self.menu()

    def register(self):
        email = input('Enter your login: ')
        password = getpass("Enter your password: ")

        accounts_cursor.execute(f'''INSERT INTO Accounts (email, password) VALUES ('{email}', '{password}')''')
        accounts_conn.commit()

        self.login()

class Main:
    def __init__(self, email):
        self.email = email

    def main(self):
        print('''What do you want to do?\n[1] Post something\n[2] Check all posts\n[3] Logout\n[4] Exit''')
        option = int(input())
        if option == 1:
            self.post()
        elif option == 2:
            self.check()
        elif option == 3:
            intro = Intro()
            intro.menu()
        elif option == 4:
            exit()
        else:
            print("Unknown option selected, please try again.")
            self.main()

    def post(self):
        content = input("Enter the content of the post: ")
        posts_cursor.execute(f'''INSERT INTO Posts (author, content) VALUES ('{self.email}', '{content}')''')
        posts_conn.commit()

    def check(self):
        posts = posts_cursor.execute('''SELECT * FROM Posts''')
        
        for row in posts:
            cur_author = row[1]
            cur_content = row[2]

            print()
            print(f'Author: {cur_author}')
            print(cur_content)
            
            input()
        
        main()

if __name__ == "__main__":
    intro = Intro()
    intro.menu()
