import os
import re
import sqlite3
import bcrypt

con = sqlite3.connect("accounts.db")
cur = con.cursor()


def get_settings():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            content = f.readlines()
        if len(content) == 2:
            return content[0].strip(), content[1].strip()
    return None, None


def save_settings(email, app_code):
    with open("settings.txt", "w") as f:
        f.write(f"{email}\n{app_code}\n")


def change_email():
    email, current_app_code = get_settings()

    cur.execute("SELECT password, app_code FROM account WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        print("\nEs existiert keinen einen Account mit dieser E-Mail Adresse")
        return

    hashed_password = row[0]

    password = input("Bitte geben Sie Ihr Passwort zur verifizierung ein: ")

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        print("\nDas Passwort ist inkorrekt")
        change_email()

    newEmail = None

    while newEmail is None:
        newEmail = input("Bitte geben Sie eine neue Sender-E-Mail-Adresse ein: ")
        if re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", newEmail
        ) and newEmail.endswith("@gmail.com"):
            save_settings(newEmail, current_app_code)

            cur.execute(
                """
                    UPDATE account SET email = ? WHERE email = ?
                """,
                (
                    newEmail,
                    email,
                ),
            )
            con.commit()

            print(
                "\nE-Mail-Adresse erfolgreich geändert! Ihre neue E-Mail-Adresse ist:",
                newEmail,
            )
            settings_menu()
        else:
            print(
                "\nDiese E-Mail-Adresse ist ungültig. Bitte geben Sie eine gültige E-Mail-Adresse ein."
            )
            newEmail = None


def show_email():
    email, _ = get_settings()
    if email:
        print("\nIhre konfigurierte Sender-E-Mail-Adresse ist:", email)
    settings_menu()


def change_app_code():
    email, _ = get_settings()

    cur.execute("SELECT password, app_code FROM account WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        print("\nEs existiert keinen einen Account mit dieser E-Mail Adresse")
        return

    hashed_password = row[0]

    password = input("Bitte geben Sie Ihr Passwort zur verifizierung ein: ")

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        print("\nDas Passwort ist inkorrekt")
        change_app_code()

    app_code = None
    while app_code is None:
        app_code = input("Bitte geben Sie einen neuen Gmail App-Code ein: ")
        if app_code:
            save_settings(email, app_code)

            cur.execute(
                """
                    UPDATE account SET app_code = ? WHERE email = ?
                """,
                (
                    app_code,
                    email,
                ),
            )
            con.commit()

            print("\nGmail App-Code erfolgreich geändert!")
            settings_menu()
        else:
            print(
                "\nDer Gmail App-Code darf nicht leer sein. Bitte geben Sie einen gültigen Gmail App-Code ein."
            )
            app_code = None


def show_app_code():
    _, app_code = get_settings()
    if app_code:
        print("\nIhr konfigurierter Gmail App-Code ist:", app_code)
    settings_menu()


def change_password():
    email, _ = get_settings()

    cur.execute("SELECT password, app_code FROM account WHERE email = ?", (email,))
    row = cur.fetchone()

    if not row:
        print("\nEs existiert keinen einen Account mit dieser E-Mail Adresse")
        return

    hashed_password = row[0]

    oldPassword = input("Bitte geben Sie Ihr altes Passwort ein: ")

    if not bcrypt.checkpw(oldPassword.encode("utf-8"), hashed_password.encode("utf-8")):
        print("\nDas Passwort ist inkorrekt")
        change_password()

    password = None
    while password is None:
        password = input(
            "Bitte geben Sie Ihr neues Passwort ein. Das Passwort muss mindestens 8 Zeichen lang sein und mindestens einen Grossbuchstaben, einen Kleinbuchstaben, eine Ziffer und ein Sonderzeichen enthalten. (^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$): "
        )
        if re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            password,
        ):
            new_hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            )

            cur.execute(
                """
                    UPDATE account SET password = ? WHERE email = ?
                """,
                (
                    new_hashed_password.decode("utf-8"),
                    email,
                ),
            )
            con.commit()

            print("\nPasswort erfolgreich geändert!")
            settings_menu()
        else:
            print(
                "\nDas Passwort muss mindestens 8 Zeichen lang sein und mindestens einen Grossbuchstaben, einen Kleinbuchstaben, eine Ziffer und ein Sonderzeichen enthalten. (^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$)"
            )
            password = None


def settings_menu():
    print("\nBitte wählen Sie eine Option:")
    print("1 (Sender-E-Mail-Adresse ändern)")
    print("2 (Konfigurierte Sender-E-Mail-Adresse anzeigen)")
    print("3 (Gmail App Code ändern)")
    print("4 (Konfigurierten Gmail App Code anzeigen)")
    print("5 (Passwort ändern)")
    print("6 (Zurück)")
    print("7 (Exit)\n")
    option = input("Option wählen: ")

    if option == "1":
        change_email()
    elif option == "2":
        show_email()
    elif option == "3":
        change_app_code()
    elif option == "4":
        show_app_code()
    elif option == "5":
        change_password()
    elif option == "6":
        os.system("python3 script.py")
        exit()
    elif option == "7":
        print("\nAuf Wiedersehen!")
        exit()
    else:
        print("Ungültige Option")
        settings_menu()


if __name__ == "__main__":
    settings_menu()
