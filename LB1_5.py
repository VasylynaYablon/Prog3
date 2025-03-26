import hashlib

# Функція для хешування пароля
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Створення єдиного словника користувачів
users = {
    "ann_89": {
        "password": hash_password("77BEAUTY_Ann88"),  # Зашифрований пароль
        "full_name": "Anna Stepanivna Romanenko"
    },
    "sydorenko2363": {
        "password": hash_password("63IvanSyd_"),  # Зашифрований пароль
        "full_name": "Ivan Ivanovych Sydorenko"
    },
    "maria_petrivna": {
        "password": hash_password("MpPetrenko*8A24n"),  # Зашифрований пароль
        "full_name": "Maria Petrivna Petrenko"
    }
}

# Функція для перевірки паролю
def password_verifying(login, entered_password):
    if login in users:
        if users[login]["password"] == hash_password(entered_password):
            # Виведення успішної перевірки паролю
            print("Correct password! Welcome, " + users[login]["full_name"] + "!")
        else:
            # Виведення помилки при неправильному паролі
            print("Incorrect password!")
    else:
        # Виведення помилки при відсутності користувача
        print("User with this login does not exist!")

# Основна програма
login_input = input("Enter your login: ")
password_input = input("Enter your password: ")

password_verifying(login_input, password_input)