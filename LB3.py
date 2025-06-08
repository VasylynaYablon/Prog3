import sqlite3
import hashlib
import datetime

# Підключення до бази даних
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Спроба створити таблицю, якщо ще не існує
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    login TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    birth_year INTEGER
)
''')
conn.commit()

# Хешування пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Додавання користувача
def add_user(login, password, full_name, phone, birth_year):
    try:
        hashed = hash_password(password)
        cursor.execute('''
            INSERT INTO users (login, password, full_name, phone, birth_year)
            VALUES (?, ?, ?, ?, ?)
        ''', (login, hashed, full_name, phone, birth_year))
        conn.commit()
        print("Користувача успішно додано.")
    except sqlite3.IntegrityError:
        print("Користувач з таким логіном вже існує.")

# Оновлення паролю
def update_password(login, new_password):
    hashed = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE login = ?", (hashed, login))
    if cursor.rowcount == 0:
        print("Користувача не знайдено.")
    else:
        conn.commit()
        print("Пароль оновлено.")

# Автентифікація
def authenticate(login):
    password = input("Введіть пароль: ")
    hashed = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, hashed))
    user = cursor.fetchone()
    if user:
        print(f"Аутентифікація пройшла успішно. Ласкаво просимо, {user[2]}!")
    else:
        print("Невірний логін або пароль.")


# Меню
if __name__ == "__main__":
    print("\n1. Додати користувача\n2. Оновити пароль\n3. Автентифікація\n4. Вихід")
    while True:
        choice = input("\nОберіть дію: ")

        match choice:
            case "1":
                login = input("Логін: ")
                password = input("Пароль: ")
                full_name = input("ПІБ: ")
                phone = input("Номер телефону: ")
                birth_year_input = input("Рік народження: ")
                try:
                    birth_year = int(birth_year_input)
                    current_year = datetime.datetime.now().year
                    age = current_year - birth_year

                    if age < 16:
                        print("Користувачеві має бути щонайменше 16 років.")
                    elif birth_year > current_year:
                        print("Рік народження не може бути з майбутнього.")
                    else:
                        add_user(login, password, full_name, phone, birth_year)
                except ValueError:
                    print("Рік народження має бути числом.")

            case "2":
                login = input("Логін: ")
                new_password = input("Новий пароль: ")
                update_password(login, new_password)

            case "3":
                login = input("Логін: ")
                authenticate(login)

            case "4":
                print("Завершення роботи.")
                break

            case _:
                print("Неправильний вибір.")