import sqlite3
from datetime import date
import os

conn = sqlite3.connect("test.db")

c = conn.cursor()

def enter_data():
    cal = input("Enter Calories: ")
    intensity = input("Enter training intensity: ")
    current_date = date.today().strftime("%Y%m%d")
    c.execute("INSERT INTO fitdata (date, calories, training) VALUES (?,?,?)", (current_date, cal, intensity))

# create table
def main():
    c.execute("""CREATE TABLE IF NOT EXISTS fitdata (date text primary key, calories integer, training integer)""")
    enter_data()
    conn.commit()
    print("These values are saved:")
    for row in c.execute("SELECT * FROM fitdata"):
        print(row)
    conn.close()

main()    
