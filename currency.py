import requests
import json
import sqlite3

api = 'access_key=a6f880e92131f61f15560e39e5935219'
url = 'http://data.fixer.io/api/latest?'
r = requests.get(url, api)
res = r.json()

# API დაკავშირება, შემოწმება.
# json ფაილის შექმნა და მისი ჩაწერა.


def connection_and_json():
    if r.status_code == 200:
        print("წარმატებით დაკავშირდა, Status code: ", r.status_code)

    print("ვალუტის ბაზა: ", res['base'])
    print("მონაცემების თარიღი: ", res['date'])
    print("ვალუტის კურსები ევროსთან მიმართებაში: ")
    print(json.dumps(res['rates'], indent=2))

    with open('currency.json', 'w') as f:
        json.dump(res, f, indent=4)

# ცხრილის შექმნა და მონაცემებით შევსება


def table():
    rows_list = []
    for each in res['rates']:
        currency = each
        value = res['rates'][each]
        row = (currency, value)
        rows_list.append(row)

    conn = sqlite3.connect('currency.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS currency
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    currency VARCHAR(50),
                    value FLOAT)
        ''')
    cursor.executemany("INSERT INTO currency (currency, value) VALUES (?, ?)", rows_list)
    conn.commit()


connection_and_json()
table()
