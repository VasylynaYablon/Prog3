def filter_ips(input_file_path, output_file_path, allowed_ips):
    """
    Аналізує IP-адреси з лог-файлу:
    - Фільтрує лише дозволені IP
    - Рахує кількість входжень
    - Записує результат у вихідний файл
    """
    result_dict = {}

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Припускаємо, що IP-адреса — перший елемент у рядку
                split_result = line.split()
                if not split_result:
                    continue  # Пропустити порожній рядок
                ip_address = split_result[0]

                if ip_address in allowed_ips:
                    if ip_address in result_dict:
                        result_dict[ip_address] += 1
                    else:
                        result_dict[ip_address] = 1

        # Запис результатів у вихідний файл
        try:
            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                for ip, count in result_dict.items():
                    out_file.write(f"{ip} - {count}\n")
        except IOError as e:
            print(f"Помилка запису до файлу '{output_file_path}': {e}")

    except FileNotFoundError:
        print(f"Файл не знайдено: '{input_file_path}'")
    except IOError as e:
        print(f"Помилка читання файлу '{input_file_path}': {e}")

allowed_ips = ['83.149.9.216', '91.177.205.119', '111.199.235.239']
filter_ips('apache_logs.txt', 'output_file.txt', allowed_ips)
print ("\nРезультат аналізу лог-файлу відображено у файлі output_file")