# Francesco Finn & Emilio Munguia
from flask import Flask, render_template
import random
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('starwars.db')
    cur = conn.cursor()
    cur.execute("SELECT name, elo FROM characters ORDER BY elo")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_character_pair():
    c1 = random.randint(1, 82)
    c2 = 0

    while c1 == c2 or c2 == 0:
        c2 = random.randint(1, 82) 
    
    conn = sqlite3.connect('starwars.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM characters WHERE rowid = " + str(c1) + " OR rowid = " + str(c2))
    pair_data = cur.fetchall()
    cur.close()
    conn.close()
    return pair_data

@app.route('/')
def index():
    data = get_data()
    pair_data = get_character_pair()
    return render_template('index.html', data=data, pair_data=pair_data)

if __name__ == '__main__':
    app.run(debug=True)