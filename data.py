import requests
import sqlite3

# Create SQLite database and table
conn = sqlite3.connect('starwars.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        name TEXT,
        height TEXT,
        mass TEXT,
        hair_color TEXT,
        skin_color TEXT,
        eye_color TEXT,
        birth_year TEXT,
        gender TEXT
    )
''')

def fetch_and_insert(url):
    response = requests.get(url)
    data = response.json()
    
    for character in data['results']:
        cursor.execute('''
            INSERT INTO characters (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (character['name'], character['height'], character['mass'], character['hair_color'],
              character['skin_color'], character['eye_color'], character['birth_year'], character['gender']))

    conn.commit()

    # Check if there's a next page and fetch its data
    if data['next']:
        fetch_and_insert(data['next'])

# Starting URL
fetch_and_insert('https://swapi.dev/api/people/')

conn.close()

conn = sqlite3.connect('starwars.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM characters")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

