# Francesco Finn & Emilio Munguia
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import random
import sqlite3
from backend.elo import EloRating
import os

app = Flask(__name__)
CORS(app)


def get_data():
    database_path = os.path.join(os.path.dirname(__file__), 'starwars.db')
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute("SELECT name, elo FROM characters ORDER BY elo DESC")
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
    cur.execute("SELECT name, image FROM characters WHERE rowid = " +
                str(c1) + " OR rowid = " + str(c2))
    pair_data = cur.fetchall()
    cur.close()
    conn.close()
    return pair_data


def get_elo(name):
    conn = sqlite3.connect('starwars.db')
    cur = conn.cursor()
    cur.execute("SELECT elo FROM characters WHERE name = ?", (name,))
    elo = cur.fetchone()
    x = elo[0]
    conn.close()
    # cur.close()
    return x


@app.route('/update_elo', methods=['POST'])
def update_elo():
    data = request.get_json()
    winner = data['winner']
    loser = data['loser']

    winner_elo = get_elo(winner)
    loser_elo = get_elo(loser)

    result = EloRating(winner_elo, loser_elo, 30, 1)

    winner_elo = result[0]
    loser_elo = result[1]

    conn = sqlite3.connect('starwars.db')
    cur = conn.cursor()

    cur.execute("UPDATE characters SET elo = ? WHERE name = ?",
                (winner_elo, winner))
    cur.execute("UPDATE characters SET elo = ? WHERE name = ?",
                (loser_elo, loser))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'success': True})


@app.route('/api/characters')
def chracters_api():
    data = get_data()

    data_dicts = [{'name': character[0], 'elo': character[1]}
                  for character in data]
    return jsonify(data_dicts)


@app.route('/api/character-pair')
def character_pair_api():
    pair_data = get_character_pair()

    pair_data_dicts = [{'name': character[0], 'image': character[1]}
                       for character in pair_data]

    return jsonify(pair_data_dicts)


def reset_elo(new_elo):

    conn = sqlite3.connect('starwars.db')
    cur = conn.cursor()
    cur.execute("UPDATE characters SET elo = ?", (new_elo))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    data = get_data()
    pair_data = get_character_pair()
    return render_template('index.html', data=data, pair_data=pair_data)


if __name__ == '__main__':
    app.run(debug=True)
