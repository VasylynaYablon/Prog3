import hashlib  # Імпортуємо модуль hashlib для обчислення SHA-256 хешів

def generate_file_hashes(*file_paths):
    """
    Обчислює SHA-256 хеші для переданих файлів.
    Параметри:
      *file_paths — будь-яка кількість шляхів до файлів.
    Повертає:
      Словник {шлях_до_файлу: хеш_у_hex_форматі}
    """
    hashes = {}  # Створюємо порожній словник для збереження результатів

    # Перебираємо кожен шлях до файлу, який передано у функцію
    for path in file_paths:
        try:
            # Відкриваємо файл у бінарному режимі для читання (важливо для хешування)
            with open(path, 'rb') as file:
                file_content = file.read()  # Зчитуємо весь вміст файлу як байти
                # Обчислюємо SHA-256 хеш і конвертуємо його у шістнадцятковий формат
                sha256_hash = hashlib.sha256(file_content).hexdigest()
                hashes[path] = sha256_hash  # Додаємо результат у словник

        # Обробка помилки, якщо файл не знайдено
        except FileNotFoundError:
            print(f"Файл не знайдено: '{path}'")

        # Обробка помилки вводу/виводу
        except IOError as e:
            print(f"Помилка читання файлу '{path}': {e}")

    return hashes  # Повертаємо словник з результатами

# передаємо три назви файлів
hashes = generate_file_hashes("file1.txt", "file2.txt", "file3.txt")

# виводимо результати у форматі шлях - хеш
for path, hash_value in hashes.items():
    print(f"{path} - {hash_value}")