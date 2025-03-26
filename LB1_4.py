# Створюємо словник для збереження задач і їх статусів
tasks = {}

# Можливі статуси задач
STATUS_OPTIONS = {"1": "очікує", "2": "в процесі", "3": "виконано"}


# Функція для додавання нової задачі
def add_task(name, status="очікує"):
    tasks[name] = status
    print(f"Задача '{name}' додана зі статусом '{status}'.")


# Функція для видалення задачі
def remove_task(name):
    if name in tasks:
        del tasks[name]
        print(f"Задача '{name}' видалена.")
    else:
        print(f"Задача '{name}' не знайдена.")


# Функція для зміни статусу задачі
def update_task_status(name, status):
    if name in tasks:
        tasks[name] = status
        print(f"Статус задачі '{name}' оновлено до '{status}'.")
    else:
        print(f"Задача '{name}' не знайдена.")


# Функція для отримання списку задач зі статусом "очікує"
def get_pending_tasks():
    pending_tasks = [task for task, status in tasks.items() if status == "очікує"]
    print("Задачі в очікуванні: ", pending_tasks)
    return pending_tasks

print("\n-----МЕНЮ ЗАДАЧ-----")
print("1. Додати задачу")
print("2. Видалити задачу")
print("3. Оновити статус задачі")
print("4. Показати задачі в очікуванні")
print("5. Вийти")

# Інтерактивне меню для користувача
while True:
    choice = input("\nВиберіть опцію: ")

    if choice == "1":
        name = input("Введіть назву задачі: ")
        print("Оберіть статус:")
        for key, value in STATUS_OPTIONS.items():
            print(f"{key}. {value}")
        status_choice = input("Виберіть номер статусу: ")
        status = STATUS_OPTIONS.get(status_choice, "очікує")
        add_task(name, status)
    elif choice == "2":
        name = input("Введіть назву задачі для видалення: ")
        remove_task(name)
    elif choice == "3":
        name = input("Введіть назву задачі для редагування статусу: ")
        print("Оберіть новий статус:")
        for key, value in STATUS_OPTIONS.items():
            print(f"{key}. {value}")
        status_choice = input("Виберіть номер статусу: ")
        status = STATUS_OPTIONS.get(status_choice, "очікує")
        update_task_status(name, status)
    elif choice == "4":
        get_pending_tasks()
    elif choice == "5":
        print("Вихід з програми.")
        print("Задачі: ", tasks)
        get_pending_tasks()
        break
    else:
        print("Невідома опція. Спробуйте ще раз.")