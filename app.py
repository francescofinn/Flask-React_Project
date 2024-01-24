# Francesco Finn & Emilio Munguia
from flask import Flask, render_template
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

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)