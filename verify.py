import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('zomato.db')

# Create a new SQLite cursor
cur = conn.cursor()

# Query the database
cur.execute('SELECT * FROM restaurants LIMIT 5')

# Fetch all results from the executed query
rows = cur.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()


