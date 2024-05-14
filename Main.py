#Jack Starr simple login program for Gelos (14.05.24)

import random
import time
import string
import sys
import os

# Constants
FILE_NAME = "accounts.txt"
DEFAULT_PASSWORD_LENGTH = 10

class User:
    # User class to store username and password
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    # UserManager class to manage user operations
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        # Load users from file
        try:
            with open(self.filename, "r") as file:
                return {line.strip().split()[0]: User(*line.strip().split()) for line in file if len(line.strip().split()) == 2}
        except FileNotFoundError:
            self.create_user_creds_file()
            return {}

    def create_user_creds_file(self):
        # Create a new file if not found
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def write_user_creds(self):
        # Write user credentials to file
        with open(self.filename, "w") as file:
            file.write('\n'.join(f"{user.username} {user.password}" for user in self.users.values()))

    def register(self):
        # Register a new user
        username = self.get_input("Enter your username: ", "Username cannot be empty.")
        if username in self.users:
            print("This username already exists. Please choose another.")
            return
        password = self.get_input("Enter your password: ", "Password cannot be empty.") if input(
            "Would you like to enter your own password (Y) or generate one (N)? ").upper() == "Y" else self.genpass()
        self.users[username] = User(username, password)
        self.write_user_creds()
        print("Registration successful! Your new password is : " + password)
        time.sleep(2)

    def login(self):
        # Login a user
        username = self.get_input("Enter your username: ", "Username cannot be empty.")
        password = self.get_input("Enter your password: ", "Password cannot be empty.")
        if self.users.get(username) and self.users[username].password == password:
            print("Login successful! Welcome, " + username + "!")
            return True, username
        else:
            print("Invalid username or password. Please try again.")
            return False, None

    def genpass(self):
        # Generate a password
        length = int(
            self.get_input(f"Please enter the length you would like your password to be (the default generated is {DEFAULT_PASSWORD_LENGTH}): ", "Length cannot be empty.") or DEFAULT_PASSWORD_LENGTH)
        include_characters = {
            "numbers": input("Include numbers? (Y/N): ").lower() == "y",
            "symbols": input("Include symbols? (Y/N): ").lower() == "y",
            "lowercase": input("Include lowercase letters? (Y/N): ").lower() == "y",
            "uppercase": input("Include uppercase letters? (Y/N): ").lower() == "y"
        }
        character_sets = {
            "numbers": string.digits,
            "symbols": string.punctuation,
            "lowercase": string.ascii_lowercase,
            "uppercase": string.ascii_uppercase
        }
        pass_chars = ''.join(character_sets[char_type] for char_type in include_characters if include_characters[char_type])

        # Check if pass_chars is empty
        while not pass_chars:
            print("You must include at least one character type.")
            include_characters = {
                "numbers": input("Include numbers? (Y/N): ").lower() == "y",
                "symbols": input("Include symbols? (Y/N): ").lower() == "y",
                "lowercase": input("Include lowercase letters? (Y/N): ").lower() == "y",
                "uppercase": input("Include uppercase letters? (Y/N): ").lower() == "y"
            }
            pass_chars = ''.join(character_sets[char_type] for char_type in include_characters if include_characters[char_type])

        password = ''.join(random.choice(pass_chars) for _ in range(length))
        print("Your generated password is: " + password)
        return password

    def viewacc(self):
        # View all registered usernames
        print("Registered Usernames:")
        for username in self.users.keys():
            print(username)

    def changepass(self, username):
        # Change a user's password
        print("Would you like to enter your own password or have one automatically generated for you?")
        choice = input("Enter 'Y' to enter your own password, or 'N' to have one generated for you: ").upper()
        if choice == "Y":
            new_password = self.get_input("Enter your new password: ", "Password cannot be empty.")
        elif choice == "N":
            new_password = self.genpass()
        else:
            print("Invalid choice. Password remains unchanged.")
            return

        self.users[username].password = new_password
        self.write_user_creds()
        print("Password changed successfully! Your new password is : " + new_password)
        time.sleep(2)

    def get_input(self, prompt, error_message):
        # Get valid input from the user
        while True:
            value = input(prompt)
            if value:
                return value
            else:
                print(error_message)

# Create a UserManager instance
user_manager = UserManager(FILE_NAME)

# Main menu
while True:
    print("\nWelcome to the Gelos Login System")
    print("1. Register")
    print("2. Login")
    print("3. View all accounts")  # New option to view all accounts
    print("4. Exit")

    choice = input("Select an option: ").upper()

    if choice == "1":
        user_manager.register()
    elif choice == "2":
        logged_in, username = user_manager.login()
        if logged_in:
            if username.lower() == "admin":
                print("Welcome Admin!")
                while True:
                    print("\nAdmin Menu:")
                    print("1. View Accounts")
                    print("2. Logout")
                    sub_choice = input("Select an option: ").lower()
                    if sub_choice == "1":
                        user_manager.viewacc()
                    elif sub_choice == "2":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please select again.")
            else:
                print("Welcome to Gelos")
                while True:
                    print("\nLogged In Menu:")
                    print("1. Change Password")
                    print("2. Logout")
                    sub_choice = input("Select an option: ").lower()
                    if sub_choice == "1":
                        user_manager.changepass(username)
                    elif sub_choice == "2":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please select again.")
    elif choice == "3":  # Option to view all accounts
        user_manager.viewacc()
    elif choice == "4":
        print("Exiting in 2")
        time.sleep(1)
        print("Exiting in 1")
        time.sleep(1)  # Adding a delay of 2 seconds before exiting
        sys.exit()  # Exit the program

    else:
        print("Invalid choice. Please select again.")