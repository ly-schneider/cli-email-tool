import os
import re

def print_message():
    print("|")
    print("|  Willkommen zum CLI E-Mail Tool")
    print("--------------------------------------------------------------------------------------")
    print("|")
    print("|  © 2024 by Levyn Schneider and David Meer")
    print("| (Unterstützt nur Gmail)")
    print("|")

def get_email_and_code(text):
    # Delete settings.txt if it exists to avoid conflicts
    if os.path.exists('settings.txt'):
        os.remove('settings.txt')

    print(f"|  {text}")
    email = None

    # Repeat until a valid email is entered
    while email is None:
        email = input("|  Bitte geben Sie Ihre E-Mail Adresse ein: ")
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) and email.endswith("@gmail.com"):
            with open('settings.txt', 'w') as f:
                f.write(email + '\n')

            password = None

            # Repeat until a valid password is entered
            while password is None:
                password = input("|  Bitte geben Sie Ihren Gmail App-Code ein: ")

                if password == "":
                    print("|")
                    print("|  Der Gmail App-Code darf nicht leer sein")
                    password = None
                    continue

                with open('settings.txt', 'a') as f:
                    f.write(password + '\n')

                print("|")
                print("|  E-Mail Adresse und Gmail App-Code erfolgreich konfiguriert")
                print("|")
                print("--------------------------------------------------------------------------------------")
                print()
        else:
            print("|")
            print("|  Diese E-Mail Adresse ist ungültig. Bitte geben Sie eine gültige E-Mail Adresse ein.")
            email = None

def main():
    print_message()

    # Check if file exists
    if not os.path.exists('settings.txt'):
        get_email_and_code("Bitte geben Sie Ihre E-Mail Adresse und Gmail App Code ein um fortzufahren")
    else:
        with open('settings.txt', 'r') as f:
            content = f.readlines()

        # Check if the content has two lines
        if len(content) != 2:
            get_email_and_code("Falsche Konfiguration; Bitte geben Sie Ihre E-Mail Adresse und Gmail App Code ein um fortzufahren")

        email = content[0].strip()
        password = content[1].strip()

        if email and password:
            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) and email.endswith("@gmail.com"):
                print(f"|  Konfigurierte Sender E-Mail Adresse: {email}")
                print("|")
                print("--------------------------------------------------------------------------------------")
                print()
            else:
                get_email_and_code("Deine Konfigurierte E-Mail Adresse ist ungültig. Bitte gib eine gültige E-Mail Adresse ein")
        else:
            get_email_and_code("Bitte geben Sie Ihre E-Mail Adresse und Gmail App Code ein um fortzufahren")

    # Menu Selector
    print("Bitte wählen Sie eine Option:")
    print("1 (E-Mail Einstellungen)")
    print("2 (E-Mail Senden)")
    print("3 (E-Mail Empfangen)")
    print("4 (Exit)")
    print()

    option = input("Option wählen: ")

    if option == '1':
        os.system('python3 settings.py')
    elif option == '2':
        os.system('python3 send.py')
    elif option == '3':
        os.system('python3 receive.py')
    elif option == '4':
        print()
        print("Auf Wiedersehen!")
    else:
        print("Ungültige Option")

if __name__ == "__main__":
    main()
