import json
import requests

nbu_response = requests.get("https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250327&end=20250402&valcode=eur&sort=exchangedate&order=desc&json")

converted_response = json.loads(nbu_response.content)

exchange_dates = []
exchange_rates = []

for item in converted_response:
    exchange_dates.append(item['exchangedate'])
    exchange_rates.append(item['rate'])

exchange_dates.reverse()
exchange_rates.reverse()

import matplotlib.pyplot as plt

for date, rate in zip(exchange_dates, exchange_rates):
    print(date, "  -  ", rate)

plt.plot(exchange_dates, exchange_rates, marker="o", linestyle="-", color="b")
plt.xlabel("Дата")
plt.ylabel("Курс EUR")
plt.title("Курс EUR за останній тиждень")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()




