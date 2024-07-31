import sqlite3
import pandas as pd

data = pd.read_csv('zomato.csv', encoding='ISO-8859-1')


print(data.head())


conn = sqlite3.connect('zomato.db')


cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    restaurant_name TEXT,
    country_code INTEGER,
    city TEXT,
    address TEXT,
    locality TEXT,
    locality_verbose TEXT,
    longitude REAL,
    latitude REAL,
    cuisines TEXT,
    average_cost_for_two INTEGER,
    currency TEXT,
    has_table_booking TEXT,
    has_online_delivery TEXT,
    is_delivering_now TEXT,
    switch_to_order_menu TEXT,
    price_range INTEGER,
    aggregate_rating REAL,
    rating_color TEXT,
    rating_text TEXT,
    votes INTEGER
)
''')


data.to_sql('restaurants', conn, if_exists='replace', index=False)


conn.commit()


conn.close()

print("Data loaded successfully!")
