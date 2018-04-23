import sqlite3
from time import time
from codec import to_emoji, from_emoji
from flask import Flask, request, render_template, redirect

# config part
app = Flask('emojilink', static_folder='lib')
db = 'emojilinks.db'
host = 'http://localhost:8080/'

@app.route('/make', strict_slashes=False, methods=['POST'])
def create_link():
    form = request.form
    if 'linktype' not in form.keys() or 'uri' not in form.keys():
        return redirect('/', 200, Response(302, 'Malformed payload :C'))
    if form['linktype'] == 'permanent':
        link = host + '/p/' + to_emoji(form['uri'])  # todo except Exception from codec
        return f'Your link: <a href="{link}">{link}</a>'
    else:
        link = host + form['clink']
        if form['linktype'] == 'oneshot':
            lifetime = int(time()-1)
        elif form['linktype'] == 'temporary':
            lifetime = int(time())+86400
        else:
            return redirect('/', 200) # TODO: fix error responses
        conn = sqlite3.connect(db)
        c = conn.cursor()
        check = c.execute(f"SELECT * FROM links WHERE custom='{form['clink']}'").fetchone()
        if check is not None:
            return redirect('/')  # TODO: error resp
        c.execute(f"INSERT INTO links VALUES ('{form['uri']}', '{form['clink']}', '{lifetime}')")
        conn.commit()
        conn.close()
        return f'Your link: <a href="{link}">{link}</a>'

@app.route('/<string:link>/', strict_slashes=False, methods=['GET'])
def temp_link(link):
    # first priority -- link for one-shot or saved
    conn = sqlite3.connect(db)
    c = conn.cursor()
    ret = c.execute(f"select * from links where custom='{link}'").fetchone()
    if ret is None:
        return redirect('/', code=404)
    if int(time()) > ret[2]:
        c.execute(f"delete from links where custom='{link}'")
    conn.commit()
    conn.close()
    return redirect(ret[0])

@app.route('/p/<string:purl>', strict_slashes=False, methods=['GET'])
def permanent_redirect(purl):
    URL = from_emoji(purl)
    return redirect(URL)

@app.route('/help', strict_slashes=False, methods=['GET'])
def help_view():
    return render_template('help.html', **dict(test='ffffa'))

@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)



app.run(host='0.0.0.0', port=8080, debug=True)