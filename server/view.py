import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('chess_games.db')
cursor = conn.cursor()

# # Query to select the first 100 rows from the table
# query = "SELECT * FROM evaluations LIMIT 100"
# cursor.execute(query)

# # Fetch column names
# column_names = [description[0] for description in cursor.description]

# # Print column names
# print("Column Names:", column_names)

# # Fetch and print the first 100 rows of data
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# Query to count the number of rows in the table
query = "SELECT COUNT(*) FROM evaluations"
cursor.execute(query)

# Fetch and print the row count
row_count = cursor.fetchone()[0]
print("Total number of rows:", row_count)

# Close the connection
conn.close()

# Close the connection
conn.close()