import sqlite3 as lite
import sys

con = lite.connect('sensorsData.db')

with con:
    cur = con.cursor
    cur.execute("DROP TABLE IF EXISTS VSL_data")
    cur.execute("CREATE TABLE VSL_data(timestamp DATETIME, tem NUMERIC, hum NUMERIC)")

