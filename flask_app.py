from flask import Flask, render_template, request
import sqlite3
import random

q = ""
app = Flask(__name__)
with open('questions.txt', 'r') as file:
    questions = file.readlines()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/question')
def question():
    global q
    q = random.choice(questions)
    return render_template('question.html', q=q, has_received_before=False)


@app.route('/process', methods=['POST'])
def process():
    global q
    q = random.choice(questions)
    out = dict(request.form)
    print(out)
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS responses (question VARCHAR(255), response VARCHAR(255))""")
    cursor.execute("INSERT INTO responses VALUES (?, ?)", (q, out['resp']))
    return render_template('question.html', q=q, has_received_before=True)


if __name__ == '__main__':
    app.run()