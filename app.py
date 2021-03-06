import sqlite3
from flask import Flask, g, request, jsonify

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return "Hello, world!"

@app.route('/pokemons', methods = ['GET'])
def pokemons():
    rows = query_db("select name, number, type1, type2 from pokemon",[],one=False)
    return jsonify({'pokemons':rows})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')
