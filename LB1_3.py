# Створюємо список продажів, де кожен запис містить продукт, кількість та ціну
sales = []

# Отримуємо введені дані від користувача
while True:
    i = 1
    print (i, ".\t")
    product = input("Enter product name or 'stop' to finish: ")
    if product.lower() == "stop":
        break

    try:
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per unit: "))
        sales.append({"product": product, "quantity": quantity, "price": price})
        i = i+1
    except ValueError:
        print("Please enter valid numeric values for quantity and price!")


# Функція для обчислення загального доходу по кожному продукту
def calculate_gains(sales):

    gains = {}
    for sale in sales:
        product = sale["product"]
        total = sale["quantity"] * sale["price"]
        if product in gains:
            gains[product] += total
        else:
            gains[product] = total
    return gains


# Обчислюємо загальний дохід
total_gain = calculate_gains(sales)

# Створюємо список продуктів, що принесли дохід більше ніж 1000
high_gain_products = [product for product, total in total_gain.items() if total > 1000]

print("\n")
# Виводимо результати
print("Total revenue per product:", total_gain)
print("Products with revenue over 1000:", high_gain_products)
