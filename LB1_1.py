def count_words(text):

    # Перетворюємо всі літери у нижній регістр, щоб уникнути дублювання через регістр
    text = text.lower()

    # Видаляємо розділові знаки
    for char in "!""#$%&'()*+,-./:;<=>?@[]^_`{|}~":
        text = text.replace(char, '')

    # Розбиваємо текст на окремі слова
    words = text.split()

    # Створюємо словник для підрахунку слів
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

print("Введіть 1 для обробки власного тексту (інакше використовується текст за замовчуванням): ")
a = input ()

if a == "1":
    # Отримуємо введений текст від користувача
    text_input = input("Введіть текст: ")
    print ("\n")
else:
    # Застосовуємо текст за замовчуванням
    text_input = "Python is an easy to learn, powerful programming language.\nThe elegant syntax, the dynamic typing of Python make it an ideal language for scripting and rapid application development.\nThe Python interpreter and the extensive standard library are freely available from the Python web site.\n"
    print(text_input)

# Викликаємо функцію для підрахунку слів
word_frequencies = count_words(text_input)

# Створюємо список слів, які зустрічаються більше 3 разів
frequent_words = [word for word, count in word_frequencies.items() if count > 3]

# Виводимо результат
print("Словник з підрахунком слів:", word_frequencies)
print("Слова, що зустрічаються більше 3 разів:", frequent_words)