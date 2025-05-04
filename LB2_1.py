import re

def analyze_log_file(log_file_path):
    """
    Аналізує лог-файл HTTP-сервера.
    Повертає словник з кількістю входжень кожного унікального HTTP-коду відповіді.
    """
    response_codes = {}  # Звичайний словник

    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Пошук коду відповіді HTTP, наприклад: "GET /index.html HTTP/1.1" 200 2326
                match = re.search(r'"\s*(\d{3})\s', line)
                if match:
                    code = match.group(1)
                    # Якщо код уже є — збільшуємо, інакше ініціалізуємо значенням 1
                    if code in response_codes:
                        response_codes[code] += 1
                    else:
                        response_codes[code] = 1

    except FileNotFoundError:
        print(f"ПОМИЛКА! Файл не знайдено: '{log_file_path}'")
        return {}
    except IOError as e:
        print(f"ПОМИЛКА! Неможливо прочитати файл: '{log_file_path}' — {e}")
        return {}

    return response_codes


# Заміни на реальний шлях до твого лог-файлу
file_path = 'apache_logs.txt'
result = analyze_log_file(file_path)
if result:
    print("Кількість входжень HTTP-кодів:")
    for code, count in sorted(result.items()):
        print(f"Код {code}: {count} разів")