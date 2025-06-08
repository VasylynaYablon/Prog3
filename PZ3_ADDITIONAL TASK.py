import sqlite3
from datetime import datetime, timedelta

# Підключення до бази даних (або створення нової, якщо її нема)
conn = sqlite3.connect("cybersec_logs.db")
cursor = conn.cursor()

# === Функція створення таблиць ===
def create_tables():
    """
    Створює таблиці для джерел подій, типів подій та самих подій безпеки.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE,
            severity TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY(source_id) REFERENCES EventSources(id),
            FOREIGN KEY(event_type_id) REFERENCES EventTypes(id)
        )
    """)
    conn.commit()

# === Функція вставки стандартних типів подій ===
def insert_default_event_types():
    default_types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]
    for type_name, severity in default_types:
        try:
            cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        except sqlite3.IntegrityError:
            pass  # Якщо вже є, не вставляємо повторно
    conn.commit()

# === Функція додавання джерела подій ===
def add_event_source():
    """
    Запитує дані джерела у користувача та додає їх у таблицю EventSources.
    """
    name = input("Назва джерела: ").strip()
    location = input("Місце розташування/IP: ").strip()
    type_ = input("Тип джерела: ").strip()
    try:
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", (name, location, type_))
        conn.commit()
        print("Джерело подій додано успішно.")
    except sqlite3.IntegrityError:
        print("Джерело з такою назвою вже існує.")

# === Функція додавання типу події ===
def add_event_type():
    """
    Запитує назву і серйозність типу події та додає їх у таблицю EventTypes.
    """
    type_name = input("Назва типу події: ").strip()
    severity = input("Серйозність (Informational, Warning, Critical): ").strip()
    try:
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        conn.commit()
        print("Тип події додано успішно.")
    except sqlite3.IntegrityError:
        print("Тип події з такою назвою вже існує.")

# === Функція додавання нової події безпеки ===
def add_security_event():
    """
    Запитує дані події, автоматично додає timestamp, і зберігає у таблицю SecurityEvents.
    """
    # Виводимо існуючі джерела подій для вибору
    cursor.execute("SELECT id, name FROM EventSources")
    sources = cursor.fetchall()
    if not sources:
        print("Спочатку додайте хоча б одне джерело подій.")
        return
    print("Доступні джерела подій:")
    for id_, name in sources:
        print(f"{id_}: {name}")
    try:
        source_id = int(input("Введіть ID джерела подій: ").strip())
    except ValueError:
        print("Некоректний ввід.")
        return
    cursor.execute("SELECT id, type_name FROM EventTypes")
    types = cursor.fetchall()
    if not types:
        print("Спочатку додайте типи подій.")
        return
    print("Доступні типи подій:")
    for id_, type_name in types:
        print(f"{id_}: {type_name}")
    try:
        event_type_id = int(input("Введіть ID типу події: ").strip())
    except ValueError:
        print("Некоректний ввід.")
        return
    message = input("Повідомлення події: ").strip()
    ip_address = input("IP-адреса (можна залишити порожнім): ").strip()
    username = input("Ім'я користувача (можна залишити порожнім): ").strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO SecurityEvents
        (timestamp, source_id, event_type_id, message, ip_address, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, source_id, event_type_id, message, ip_address or None, username or None))
    conn.commit()
    print("Подію безпеки додано.")

# === Функція отримання всіх 'Login Failed' за останні 24 години ===
def query_login_failed_last_24h():
    """
    Виводить всі події з типом 'Login Failed' за останні 24 години.
    """
    time_24h_ago = datetime.now() - timedelta(hours=24)
    cursor.execute("""
        SELECT se.id, se.timestamp, es.name, et.type_name, se.message
        FROM SecurityEvents se
        JOIN EventSources es ON se.source_id = es.id
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.type_name = 'Login Failed' AND se.timestamp >= ?
        ORDER BY se.timestamp DESC
    """, (time_24h_ago.strftime("%Y-%m-%d %H:%M:%S"),))
    rows = cursor.fetchall()
    if not rows:
        print("За останні 24 години подій 'Login Failed' не знайдено.")
        return
    print("Події 'Login Failed' за останні 24 години:")
    for r in rows:
        print(f"ID: {r[0]}, Час: {r[1]}, Джерело: {r[2]}, Тип: {r[3]}, Повідомлення: {r[4]}")

# === Функція виявлення IP з >5 невдалими входами за годину ===
def detect_brute_force_ips():
    """
    Визначає IP-адреси, з яких за останню годину було більше 5 невдалих спроб входу.
    """
    one_hour_ago = datetime.now() - timedelta(hours=1)
    cursor.execute("""
        SELECT se.ip_address, COUNT(*) as fail_count
        FROM SecurityEvents se
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.type_name = 'Login Failed' 
          AND se.timestamp >= ?
          AND se.ip_address IS NOT NULL
        GROUP BY se.ip_address
        HAVING fail_count > 5
    """, (one_hour_ago.strftime("%Y-%m-%d %H:%M:%S"),))
    rows = cursor.fetchall()
    if not rows:
        print("IP-адрес з >5 невдалими спробами входу за останню годину не виявлено.")
        return
    print("Потенційні IP для атаки підбору пароля:")
    for ip, count in rows:
        print(f"IP: {ip}, Кількість невдалих входів: {count}")

# === Функція отримання критичних подій за останній тиждень, згрупованих за джерелом ===
def query_critical_events_last_week():
    """
    Виводить критичні події за останній тиждень, згруповані за джерелом.
    """
    one_week_ago = datetime.now() - timedelta(days=7)
    cursor.execute("""
        SELECT es.name, COUNT(se.id) as critical_count
        FROM SecurityEvents se
        JOIN EventSources es ON se.source_id = es.id
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE et.severity = 'Critical' AND se.timestamp >= ?
        GROUP BY es.name
        ORDER BY critical_count DESC
    """, (one_week_ago.strftime("%Y-%m-%d %H:%M:%S"),))
    rows = cursor.fetchall()
    if not rows:
        print("Критичних подій за останній тиждень не знайдено.")
        return
    print("Критичні події за останній тиждень (згруповані за джерелом):")
    for name, count in rows:
        print(f"Джерело: {name}, Кількість критичних подій: {count}")

# === Функція пошуку подій за ключовим словом у повідомленні ===
def search_events_by_keyword():
    """
    Шукає всі події, у повідомленнях яких міститься задане ключове слово.
    """
    keyword = input("Введіть ключове слово для пошуку в повідомленнях: ").strip()
    cursor.execute("""
        SELECT se.id, se.timestamp, es.name, et.type_name, se.message
        FROM SecurityEvents se
        JOIN EventSources es ON se.source_id = es.id
        JOIN EventTypes et ON se.event_type_id = et.id
        WHERE se.message LIKE ?
        ORDER BY se.timestamp DESC
    """, (f"%{keyword}%",))
    rows = cursor.fetchall()
    if not rows:
        print("Подій із таким ключовим словом не знайдено.")
        return
    print(f"Події, що містять '{keyword}':")
    for r in rows:
        print(f"ID: {r[0]}, Час: {r[1]}, Джерело: {r[2]}, Тип: {r[3]}, Повідомлення: {r[4]}")

# === Основне меню користувача ===
def main_menu():
    """
    Головне меню програми з навігацією за допомогою match-case.
    """
    print("\n=== Головне меню ===")
    print("1. Додати нове джерело подій")
    print("2. Додати новий тип події")
    print("3. Додати нову подію безпеки")
    print("4. Показати всі 'Login Failed' події за останні 24 години")
    print("5. Виявити IP-адреси з >5 невдалими входами за годину")
    print("6. Показати критичні події за останній тиждень, згруповані за джерелом")
    print("7. Пошук подій за ключовим словом у повідомленні")
    print("8. Вихід")
    while True:

        choice = input("\nВведіть номер опції: ").strip()

        match choice:
            case "1":
                add_event_source()
            case "2":
                add_event_type()
            case "3":
                add_security_event()
            case "4":
                query_login_failed_last_24h()
            case "5":
                detect_brute_force_ips()
            case "6":
                query_critical_events_last_week()
            case "7":
                search_events_by_keyword()
            case "8":
                print("Вихід з програми. До побачення!")
                break
            case _:
                print("Невірний вибір, спробуйте ще раз.")

# === Точка входу програми ===
if __name__ == "__main__":
    create_tables()               # Створити таблиці, якщо їх ще немає
    insert_default_event_types()  # Вставити базові типи подій
    main_menu()                   # Запустити меню
    conn.close()                  # Закрити підключення при виході
