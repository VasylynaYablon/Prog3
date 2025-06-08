import hashlib
from datetime import datetime

# Функція для хешування пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Базовий клас користувача
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = hash_password(password)
        self.is_active = is_active

    def verify_password(self, password):
        return self.password_hash == hash_password(password)

    def view_attributes(self):
        print(f"Ім'я користувача: {self.username}")
        print(f"Статус: {'Активний' if self.is_active else 'Неактивний'}")

    def update_password(self, new_password):
        confirm = input("Підтвердіть новий пароль: ").strip()
        if new_password != confirm:
            print("Паролі не збігаються. Пароль не змінено.")
            return
        self.password_hash = hash_password(new_password)
        print(f"Пароль користувача {self.username} було успішно змінено.")

# Клас адміністратора
class Administrator(User):
    def __init__(self, username, password, email=None):
        super().__init__(username, password)
        self.email = email
        self.privileges = ["manage_users", "view_logs", "shutdown_system"]
        self.activity_log = []
        self.access_level = 10
        self.department = "System Administration"

    def log_action(self, action):
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.activity_log.append(f"[{time}] {action}")

    def deactivate_user(self, user):
        if user.is_active:
            user.is_active = False
            self.log_action(f"Deactivated user: {user.username}")
            print(f"Користувача {user.username} деактивовано.")
        else:
            print(f"Користувач {user.username} вже неактивний.")

    def view_privileges(self):
        print("Привілеї адміністратора:")
        for privilege in self.privileges:
            print(f"- {privilege}")
        print(f"Відділ: {self.department}")

    def view_contact_info(self):
        print(f"Email: {self.email if self.email else 'Не вказано'}")

    def update_contact_info(self, email=None):
        if email:
            self.email = email
        print("Контактні дані було успішно оновлено.")

# Клас звичайного користувача
class RegularUser(User):
    def __init__(self, username, password, email=None, phone_number=None):
        super().__init__(username, password)
        self.email = email
        self.phone_number = phone_number
        self.user_data = {}
        self.account_creation_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.membership_status = "Silver"
        self.last_login = None

    def update_user_data(self, key, value):
        self.user_data[key] = value
        print(f"Дані користувача {self.username} було успішно оновлено.")

    def view_user_data(self):
        print(f"Дані користувача {self.username}:")
        for key, value in self.user_data.items():
            print(f"{key}: {value}")
        print(f"Дата створення: {self.account_creation_date}")
        print(f"Статус членства: {self.membership_status}")
        print(f"Email: {self.email if self.email else 'Не вказано'}")
        print(f"Телефон: {self.phone_number if self.phone_number else 'Не вказано'}")
        print(f"Останній вхід: {self.last_login if self.last_login else 'Це перший вхід'}")

    def update_contact_info(self, email=None, phone_number=None):
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number
        print("Контактні дані було успішно оновлено.")

    def update_last_login(self):
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M")

    def update_membership_status(self, new_status):
        valid_statuses = ["Silver", "Gold", "Platinum"]
        if new_status in valid_statuses:
            self.membership_status = new_status
            print(f"Рівень підписки змінено на {new_status}.")
        else:
            print("Невірний рівень підписки.")

# Клас гостя
class GuestUser(User):
    def __init__(self, username, password):
        super().__init__(username, password, is_active=True)
        self.read_only = True
        self.session_duration = 15
        self.last_access_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    def view_attributes(self):
        print(f"Ім'я користувача: {self.username}")
        print(f"Статус: {'Активний' if self.is_active else 'Неактивний'}")
        print("Гість має лише обмежений доступ.")
        print(f"Останній доступ: {self.last_access_time}")

# Система доступу
class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            print(f"Вітаємо, {username}!")
            return user
        print("Невірний логін або пароль.")
        return None

    def register_new_user(self, username, password, email=None, phone_number=None):
        if username in self.users:
            print(f"Користувач {username} вже існує.")
            return None
        confirm = input("Підтвердіть пароль: ").strip()
        if password != confirm:
            print("Паролі не збігаються. Реєстрацію скасовано.")
            return None
        new_user = RegularUser(username, password, email, phone_number)
        self.add_user(new_user)
        print(f"Користувач {username} зареєстрований.")
        return new_user

# Меню для RegularUser
def regular_user_menu(user):
    user.update_last_login()
    menu = """
Виберіть дію:
1. Переглянути атрибути користувача
2. Переглянути свої дані
3. Змінити свої дані
4. Змінити рівень підписки
5. Змінити пароль
6. Вийти"""
    print(menu)
    while True:
        choice = input("Ваш вибір: ").strip()
        match choice:
            case "1":
                user.view_attributes()
            case "2":
                user.view_user_data()
            case "3":
                key = input("Ключ (наприклад, email): ").strip()
                value = input(f"Значення для {key}: ").strip()
                user.update_user_data(key, value)
            case "4":
                status = input("Новий статус (Silver, Gold, Platinum): ").strip()
                user.update_membership_status(status)
            case "5":
                new_pass = input("Новий пароль: ").strip()
                user.update_password(new_pass)
            case "6":
                break
            case _:
                print("Невірна опція. Спробуйте ще раз.")

# Меню для Administrator
def admin_menu(admin, system):
    menu = """
Виберіть дію:
1. Переглянути атрибути
2. Переглянути привілеї
3. Деактивувати користувача
4. Змінити пароль
5. Змінити контактні дані
6. Показати всіх користувачів
7. Показати власний журнал дій
8. Вийти"""
    print(menu)
    while True:
        choice = input("Ваш вибір: ").strip()
        match choice:
            case "1":
                admin.view_attributes()
            case "2":
                admin.view_privileges()
            case "3":
                name = input("Кого деактивувати: ").strip()
                target = system.users.get(name)
                match target:
                    case None:
                        print("Користувача не знайдено.")
                    case _:
                        admin.deactivate_user(target)
            case "4":
                new_pass = input("Новий пароль: ").strip()
                admin.update_password(new_pass)
            case "5":
                email = input("Новий email: ").strip()
                admin.update_contact_info(email=email)
            case "6":
                print("\nСписок усіх користувачів:\n" + "-" * 40)
                for user in system.users.values():
                    print(f"\n ➡ Користувач: {user.username}")
                    print(f"   Статус: {'Активний' if user.is_active else 'Неактивний'}")
                    match user:
                        case RegularUser():
                            user.view_user_data()
                        case Administrator():
                            user.view_attributes()
                            user.view_contact_info()
                        case GuestUser():
                            user.view_attributes()
                    print("-" * 40)
            case "7":
                print(f"\nЖурнал дій адміністратора {admin.username}:")
                match admin.activity_log:
                    case []:
                        print("   Немає записів.")
                    case _:
                        for entry in admin.activity_log:
                            print(f"   {entry}")
            case "8":
                break
            case _:
                print("Невірна опція. Спробуйте ще раз.")
# Основна програма
if __name__ == "__main__":
    system = AccessControl()

    # Додаємо користувачів
    system.add_user(Administrator("admin", "admin123", email="admin@system.com"))
    system.add_user(RegularUser("john", "qwerty", email="john@example.com", phone_number="1234567890"))
    system.add_user(GuestUser("guest01", "guest"))

    action = input("Ви вже зареєстровані? (yes/no): ").strip().lower()
    if action == "no":
        username = input("Ім'я користувача: ").strip()
        password = input("Пароль: ").strip()
        email = input("Email: ").strip()
        phone = input("Телефон: ").strip()
        phone = phone if phone else None
        new_user = system.register_new_user(username, password, email, phone)
        if new_user:
            regular_user_menu(new_user)
    else:
        username = input("Логін: ").strip()
        password = input("Пароль: ").strip()
        user = system.authenticate(username, password)
        if user:
            if isinstance(user, Administrator):
                admin_menu(user, system)
            elif isinstance(user, RegularUser):
                regular_user_menu(user)
            elif isinstance(user, GuestUser):
                user.view_attributes()