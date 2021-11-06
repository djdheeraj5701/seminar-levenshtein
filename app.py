import os
from os.path import join, dirname
from dotenv import load_dotenv
import time
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
import matplotlib.pyplot as plt
import numpy as np
import sys
from flask import *
import sqlalchemy as db
import seminar.seminar_code_1 as sm1
import seminar.seminar_code_2 as sm2
import seminar.seminar_code_3 as sm3
import seminar.seminar_code_4 as sm4

SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
engine=db.create_engine(SQLALCHEMY_DATABASE_URI,connect_args={"check_same_thread":False})
connection = engine.connect()
metadata = db.MetaData()


app = Flask(__name__)


class Data:
    def __init__(self):
        self.title="Easy, Efficient Spell Checker using Levenshtein Edit Distance and Trie"
        self.loaded,self.perform,self.compare="#a00",False,False
        self.display=False
        self.headers = ["word", "worst", "better", "best"]
        self.records=[]


o=Data()


@app.route('/createtables')
def create_tables():
    connection.execute(
        """CREATE TABLE words
        (
          word VARCHAR(50) NOT NULL,
          worst FLOAT NOT NULL,
          better FLOAT NOT NULL,
          best FLOAT NOT NULL,
          PRIMARY KEY (word)
        )
        """
    )
    return url_for('index')


@app.route('/droptables')
def drop_tables():
    connection.execute("drop table words")
    return url_for('index')


@app.route('/')
def index():
    return render_template("index.html", o=o)


@app.route('/worst',methods=['POST','GET'])
def worst():
    o.perform,o.compare=True,False
    o.display = False
    o.operation='worst'
    try:
        word=request.form['word']
        sm2.words_append()
        o.matches,o.time_gap=sm2.l.solve_dp(word)
        query = f'select * from words where word=?'
        result_proxy = connection.execute(query,word)
        if result_proxy.fetchall():
            query = 'UPDATE words SET worst=? WHERE word=?'
            connection.execute(query, (o.time_gap, word))
        else:
            query = 'INSERT INTO words VALUES (?,?,?,?)'
            connection.execute(query, (word, o.time_gap,0, 0))
    except Exception as e:
        print(e)
    return render_template("index.html", o=o)


@app.route('/better',methods=['POST','GET'])
def better():
    o.perform, o.compare = True, False
    o.display = False
    o.operation = 'better'
    try:
        word=request.form['word']
        sm3.words_append()
        o.matches,o.time_gap=sm3.solver(word)
        query = f'select * from words where word=?'
        result_proxy = connection.execute(query,word)
        if result_proxy.fetchall():
            query = 'UPDATE words SET better=? WHERE word=?'
            connection.execute(query, (o.time_gap, word))
        else:
            query = 'INSERT INTO words VALUES (?,?,?,?)'
            connection.execute(query, (word,0,o.time_gap,0))
    except Exception as e:
        print(e)
    return render_template("index.html", o=o)

@app.route('/best',methods=['POST','GET'])
def best():
    o.perform, o.compare = True, False
    o.display = False
    o.operation = 'best'
    try:
        word=request.form['word']
        sm4.words_append()
        o.matches,o.time_gap=sm4.solver(word)
        query = f'select * from words where word=?'
        result_proxy = connection.execute(query,word)
        if result_proxy.fetchall():
            query = 'UPDATE words SET best=? WHERE word=?'
            connection.execute(query, (o.time_gap, word))
        else:
            query = 'INSERT INTO words VALUES (?,?,?,?)'
            connection.execute(query, (word,0,0,o.time_gap))
    except Exception as e:
        print(e)
    return render_template("index.html", o=o)


@app.route('/compare')
def compare():
    o.perform, o.compare = False, True
    o.display = False
    query = f'select * from words'
    result_proxy = connection.execute(query)
    result = result_proxy.fetchall()
    x=[]
    barWidth = 0.25
    br1 = np.arange(len(result))
    br2 = [x1 + barWidth for x1 in br1]
    br3 = [x1 + barWidth for x1 in br2]
    worst_l = []
    better_l = []
    best_l = []
    for i in result:
        x.append(i[0])
        worst_l.append(i[1])
        better_l.append(i[2])
        best_l.append(i[3])
    print(x,worst_l,better_l,best_l)
    plt.bar(br1,worst_l,
             label="worst",width=barWidth,color="red")
    plt.bar(br2,better_l,
             label="better",width=barWidth,color="blue")
    plt.bar(br3,best_l,
             label="best",width=barWidth,color="green")
    plt.xticks([r + barWidth for r in range(len(x))],
               x)
    # plt.legend()
    plt.savefig('static/compare.png')
    return render_template("index.html", o=o)


@app.route('/display')
def display():
    o.perform, o.compare = False, False
    o.display = True
    query = f'select * from words'
    result_proxy = connection.execute(query)
    o.records = result_proxy.fetchall()
    print(o.records)
    return render_template("index.html", o=o)


# @app.route('/load')
# def load():
#     o.loaded="#0a0"
#     sm2.words_append()
#     sm3.words_append()
#     sm4.words_append()
#     return render_template("index.html", o=o)


if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=os.environ.get("PORT"))


