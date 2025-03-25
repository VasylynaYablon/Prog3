# Створюємо словник з продуктами та їх кількістю на складі
storage = {
    "apples": 10,
    "lemons": 3,
    "cinnamon buns": 5,
    "bread": 7,
    "chocolate": 2,
    "eggs": 12
}

# Функція для оновлення кількості продукту
def update_storage(product, quantity):

    if product in storage:
        storage[product] += quantity
        if storage[product] < 0:
            storage[product] = 0  # Запобігаємо від'ємним значенням
    else:
        storage[product] = max(0, quantity)  # Додаємо новий продукт, якщо його немає в словнику

print ("\n-----UPDATING INFORMATION IN THE STORAGE-----")

# Отримуємо введені дані від користувача
while True:
    product = input("Enter the product name or 'stop' to exit: ")
    if product.lower() == "stop":
        break  # Виходимо з циклу, якщо користувач вводить 'stop'

    try:
        quantity = int(input("Enter the quantity (positive to add, negative to remove): "))
        update_storage(product, quantity)  # Оновлюємо склад
    except ValueError:
        print("Please enter a valid number!")  # Якщо користувач ввів не число

# Створюємо список продуктів, яких менше ніж 5
low_number_of_products = [product for product, qty in storage.items() if qty < 5]

print("\n")
# Виводимо результати
print("Updated storage:", storage)  # Оновлений склад
print("Products with less than 5 items:", low_number_of_products)  # Продукти, яких менше ніж 5
