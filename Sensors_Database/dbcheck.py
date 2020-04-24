import sqlite3


conn = sqlite3.connect('sensorsData.db')
curs = conn.cursor()
curs.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
print('List of tables ',curs.fetchall())
for row in curs.execute("SELECT * FROM VSL_data ORDER BY timestamp DESC LIMIT 1"):
    time = str(row[0])
    temp = row[1]
    hum = row[2]
print(time, temp, hum)
conn.close()
