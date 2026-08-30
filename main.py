from auth import register, login
from teacher import teacher_menu
from student import student_menu
from admin import admin_menu


def main():

    while True:

        print("\n==============================")
        print(" ONLINE EXAM MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()

        elif choice == "2":

            user = login()

            if user:

                if user["role"] == "admin":
                    print("\nWelcome Admin")
                    admin_menu()

                elif user["role"] == "teacher":
                    print("\nWelcome", user["name"])
                    teacher_menu(user)

                elif user["role"] == "student":
                    print("\nWelcome", user["name"])
                    student_menu(user)

        elif choice == "3":
            print("\nThank you!")
            break

        else:
            print("Invalid choice")


main()