# ENV
# DEBUG
# SECRET
# HOST

import sqlite3
from time import time
from codec import to_emoji, from_emoji
from flask import Flask, request, render_template, redirect, send_from_directory
from toydiscover import report
import os
# config part
app = Flask('emojilink', static_folder='templates/static')
app.secret_key = os.getenv('SECRET', 'test')
db = 'emojilinks.db'
host = os.getenv('HOST', 'http://localhost:8080/')

@app.route('/make', strict_slashes=False, methods=['POST'])
def create_link():
    if request.json is None or 'url' not in request.json.keys() or 'short' not in request.json.keys():
        return {'url': 'No dice.', 'message': 'I am an error'}
    url = request.json.get('url')
    short = request.json.get('short')
    oneshot = request.json.get('oneshot', False)

    if oneshot:
        lifetime = int(time() - 1)
    else:
        lifetime = int(time()) + 86400

    conn = sqlite3.connect(db)
    c = conn.cursor()
    check = c.execute(f"SELECT * FROM links WHERE short='{short}'").fetchone()
    if check is not None:
        return {'result': 'Link is taken', 'message': "Error"}
    c.execute(f"INSERT INTO links VALUES ('{url}', '{short}', '{lifetime}')")
    conn.commit()
    conn.close()
    return {'result': host + short, 'message': 'Your URL'}

@app.route('/encode', strict_slashes=False, methods=['POST'])
def encode_link():
    url = request.json.get('url')
    if url is None or url.__len__() == 0:
        return {'result': 'No URL?', 'message': 'Errord'}
    return {'message': 'Your URL', 'result': host+to_emoji(url)}


@app.route('/<string:link>', strict_slashes=False, methods=['GET'])
def serve_link(link):
    if link == 'make':
        return create_link()  # fixme this is horrendous
    if link == 'encode':
        return encode_link()  # fixme too
    conn = sqlite3.connect(db)
    c = conn.cursor()
    ret = c.execute(f"select * from links where short='{link}'").fetchone()
    if ret is None:
        try:
            URL = from_emoji(link)
            return redirect(URL)
        except Exception:   # fixme
            return redirect('/', code=404)
    if int(time()) > ret[2]:
        c.execute(f"delete from links where short='{link}'")
    conn.commit()
    conn.close()
    return redirect(ret[0])


@app.route('/', strict_slashes=False, methods=['GET'])
def index_view():
    return render_template('index.html')


if __name__ == '__main__':
    tdr = report.ToyDiscoverReporter('emojiurl', 'Emoji URL', 'A URL shortener which uses emoji! Neat!')
    tdr.ioloop()
    app.run(host='0.0.0.0', port=80, debug=(os.getenv('DEBUG', '') != ''))