import os
import re

def display_menu():
    print()
    print("Bitte wählen Sie eine Option:")
    print("1 (Sender-E-Mail-Adresse ändern)")
    print("2 (Konfigurierte Sender-E-Mail-Adresse anzeigen)")
    print("3 (Gmail App Code ändern)")
    print("4 (Konfigurierten Gmail App Code anzeigen)")
    print("5 (Zurück)")
    print("6 (Exit)")
    print()

def get_settings():
    if os.path.exists('settings.txt'):
        with open('settings.txt', 'r') as f:
            content = f.readlines()
        if len(content) == 2:
            return content[0].strip(), content[1].strip()
    return None, None

def save_settings(email, password):
    with open('settings.txt', 'w') as f:
        f.write(f"{email}\n{password}\n")

def change_email():
    _, current_password = get_settings()
    email = None
    while email is None:
        email = input("Bitte geben Sie eine neue Sender-E-Mail-Adresse ein: ")
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) and email.endswith("@gmail.com"):
            save_settings(email, current_password)
            print("\nE-Mail-Adresse erfolgreich geändert! Ihre neue E-Mail-Adresse ist:", email)
            settings_menu()
        else:
            print("\nDiese E-Mail-Adresse ist ungültig. Bitte geben Sie eine gültige E-Mail-Adresse ein.")
            email = None

def show_email():
    email, _ = get_settings()
    if email:
        print("\nIhre konfigurierte Sender-E-Mail-Adresse ist:", email)
    settings_menu()

def change_password():
    current_email, _ = get_settings()
    password = None
    while password is None:
        password = input("Bitte geben Sie einen neuen Gmail App-Code ein: ")
        if password:
            save_settings(current_email, password)
            print("\nGmail App-Code erfolgreich geändert!")
            settings_menu()
        else:
            print("\nDer Gmail App-Code darf nicht leer sein. Bitte geben Sie einen gültigen Gmail App-Code ein.")
            password = None

def show_password():
    _, password = get_settings()
    if password:
        print("\nIhr konfigurierter Gmail App-Code ist:", password)
    settings_menu()

def exit_program():
    print("\nAuf Wiedersehen!")
    exit()

def settings_menu():
    display_menu()
    option = input("Option wählen: ")
    
    if option == '1':
        change_email()
    elif option == '2':
        show_email()
    elif option == '3':
        change_password()
    elif option == '4':
        show_password()
    elif option == '5':
        os.system('python3 script.py')
    elif option == '6':
        exit_program()
    else:
        print("Ungültige Option")
        settings_menu()

if __name__ == "__main__":
    settings_menu()
