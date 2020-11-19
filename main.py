
import os  # List of module import statements
import sys  # Each one on a line
import flask
import pysqlite3 as sqlite3
import sqlite3_helper
import config
from datetime import datetime

# ######################################################
# No Module - Level Variables or Statements !
# ONLY FUNCTIONS BEYOND THIS POINT !
# ######################################################

app = flask.Flask(__name__)
app.static_folder = app.root_path
hdb = sqlite3_helper.SqliteDB(db_path=config.PATH_DATABASE, row_type="dict", placeholder="$", commit_every_query=True)

@app.route("/<hashedcode>/profile", methods=['GET', 'POST'])
def profile(hashedcode):
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    posts = hdb.select(['posts'], poster=username)

    return flask.render_template('profile.html', username=username, hashedcode=hashedcode, posts=posts)

@app.route("/<hashedcode>/create", methods=['GET', 'POST'])
def create(hashedcode):
    return flask.render_template('create.html', hashedcode=hashedcode)

@app.route("/register", methods=['GET', 'POST'])
def register():
    return flask.render_template('register.html')

@app.route("/<hashedcode>/posts/<postid>", methods=['GET', 'POST'])
def post(hashedcode,postid):
    row = hdb.select_row(['posts'], id=int(postid))
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    posterHash = hdb.select_row(['users'], username=row['poster'])['hash']
    try:
        userVote = hdb.select_row(['votes'], username=username, postid=postid)['vote']
    except sqlite3_helper.DBItemNotFoundError:
        userVote = 0
    return flask.render_template('post.html', postid=postid, posterHash=posterHash, userHash=hashedcode, userVote=userVote, poster=row['poster'], title=row['title'], content=row['content'], dateposted=row['dateposted'], score=row['score'])

@app.route("/<hashedcode>/feed", methods=['GET', 'POST'])
def feed(hashedcode):
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    return flask.render_template('feed.html', username=username, hashedcode=int(hashedcode))

@app.route("/submit_register", methods=['POST'])
def submit_register():
    try:
        row = hdb.select_row(('users'), username=flask.request.form.get('username'))
    except sqlite3_helper.DBItemNotFoundError:
        hdb.insert(('users'), username=flask.request.form.get('username'), hash=hash(flask.request.form.get('username')))
        row = hdb.select_row(('users'), username=flask.request.form.get('username'))
    # return flask.redirect(flask.url_for(".feed", hashedcode=row['hash']))
    
    #VVVV FOR PHASE 1 DEMO ONLY VVVV
    return flask.redirect(flask.url_for(".profile", hashedcode=row['hash']))

@app.route("/<hashedcode>/submit_post", methods=['POST'])
def submit_post(hashedcode):
    username = hdb.select_row(["users"], what="username", hash=int(hashedcode))['username']
    rowid = hdb.insert("posts", return_row_id=True, poster=username, title=flask.request.form.get('title'), content=flask.request.form.get('content'), score=0, dateposted=datetime.now().isoformat())
    print(hdb.select(['posts'])) # don't get rid of this
    return flask.redirect(flask.url_for(".profile", hashedcode=hashedcode))

@app.route("/vote", methods=['POST'])
def vote():
    username = hdb.select_row(["users"], what="username", hash=int(flask.request.form.get('voterHash')))['username']
    # if len(hdb.select(['votes'], postid=flask.request.form.get('postid'), username=username)) > 0: # if the voter has already voted on this post
    #     hdb.update('votes')
    hdb.upsert('votes', {"postid" : flask.request.form.get('postid'), "username" : username}, postid=flask.request.form.get('postid'), username=username, vote=flask.request.form.get('vote'))
    print(hdb.select(['votes']))
    return "ok"

# This block is optional and can be used for testing .
# We will NOT look into its content .
# ######################################################
if __name__ == "__main__":
    app.run(port=5678, host='127.0.0.1', debug=True, use_evalex=False)
    #app.run()