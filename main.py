# TODO: 1. Do pagination
#       2. Do other extra credit
#       3. Update JIRA to show everything's done and record hours spent
#       4. Fix voting


import os  # List of module import statements
import sys  # Each one on a line
import flask
import pysqlite3 as sqlite3
import sqlite3_helper
import config
from datetime import datetime
import json
import math

# ######################################################
# No Module - Level Variables or Statements !
# ONLY FUNCTIONS BEYOND THIS POINT !
# ######################################################

app = flask.Flask(__name__)
app.static_folder = app.root_path
hdb = sqlite3_helper.SqliteDB(db_path=config.PATH_DATABASE, row_type="dict", placeholder="$", commit_every_query=True)


def getDatePosted(dateposted):
    dateposted = dateposted[:10] + " " + dateposted[11:]
    totalSeconds = int((datetime.now() - datetime.strptime(dateposted, "%Y-%m-%d %H:%M:%S.%f")).total_seconds())
    days = int(totalSeconds / (60 * 60 * 24))
    hours = int(totalSeconds / (60 * 60))
    minutes = int(totalSeconds / 60)
    if days:
        return str(days) + " days ago"
    elif hours:
        if minutes >= 30:
            return str(hours) + " hours and 30 minutes ago"
        else:
            return str(hours) + " hours ago"
    elif minutes >= 30:
        return "30 minutes ago"
    else:
        return "Posted just now"


@app.route("/<hashedcode>/profile", methods=['GET', 'POST'])
def profile(hashedcode):
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    profilePicture = hdb.select(["users"], what="profilePicture", hash=int(hashedcode))[0]['profilePicture']
    posts = hdb.select(['posts'], poster=username, order="dateposted DESC")
    for post in posts:
        post['dateposted'] = getDatePosted(post['dateposted'])

        try:
            post['userVote'] = hdb.select_row('votes', what="vote", username=username, postid=post['id'])['vote']
        except sqlite3_helper.DBItemNotFoundError:
            post['userVote'] = 0
    postsJSON = json.dumps(posts)
    return flask.render_template('profile.html', username=username, userHash=hashedcode, posts=posts,
                                 postsJSON=postsJSON, profilePicture=profilePicture)


@app.route("/<hashedcode>/create", methods=['GET', 'POST'])
def create(hashedcode):
    return flask.render_template('create.html', hashedcode=hashedcode)


@app.route("/register", methods=['GET', 'POST'])
def register():
    return flask.render_template('register.html')


@app.route("/<hashedcode>/posts/<postid>", methods=['GET', 'POST'])
def post(hashedcode, postid):
    row = hdb.select_row(['posts'], id=int(postid))
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    posterHash = hdb.select_row(['users'], username=row['poster'])['hash']
    try:
        userVote = hdb.select_row('votes', username=username, postid=int(postid))['vote']
    except sqlite3_helper.DBItemNotFoundError:
        userVote = 0
    return flask.render_template('post.html', postid=postid, posterHash=posterHash, userHash=hashedcode,
                                 userVote=userVote, poster=row['poster'], title=row['title'], content=row['content'],
                                 dateposted=getDatePosted(row['dateposted']), score=row['score'])


@app.route("/<hashedcode>/feed/<pagenum>", methods=['GET', 'POST'])
def feed(hashedcode, pagenum):
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    allPosts = hdb.select(['posts'], order=["dateposted DESC"], where={'poster': username}, notEqual=True)
    posts = allPosts[(int(pagenum) - 1) * 5 : (int(pagenum) - 1) * 5 + 5]
    for post in posts:
        post['dateposted'] = getDatePosted(post['dateposted'])
        post['username'] = hdb.select_row(['users'], username=post['poster'])['username']
        posterHash = hdb.select_row(['users'], username=post['poster'])['hash']
        post['profilePicture'] = hdb.select_row(["users"], what="profilePicture", hash=posterHash)['profilePicture']
        try:
            post['userVote'] = hdb.select_row('votes', username=username, postid=post['id'])['vote']
        except sqlite3_helper.DBItemNotFoundError:
            post['userVote'] = 0
    postsJSON = json.dumps(posts)
    return flask.render_template('feed.html', username=username, userHash=hashedcode,
                                 posts=posts, postsJSON=postsJSON,
                                 currPage=int(pagenum), numPages=math.ceil((len(allPosts) / 5)))


@app.route("/submit_register", methods=['POST'])
def submit_register():
    profilePicture = flask.request.form.get('option')
    try:
        row = hdb.select_row(('users'), username=flask.request.form.get('username'))
    except sqlite3_helper.DBItemNotFoundError:
        hdb.insert(('users'), username=flask.request.form.get('username'),
                   hash=hash(flask.request.form.get('username')), profilePicture=profilePicture)
        row = hdb.select_row(('users'), username=flask.request.form.get('username'))
    # return flask.redirect(flask.url_for(".feed", hashedcode=row['hash']))

    # VVVV FOR PHASE 1 DEMO ONLY VVVV
    return flask.redirect(flask.url_for(".feed", hashedcode=row['hash'], pagenum=1))


@app.route("/<hashedcode>/submit_post", methods=['POST'])
def submit_post(hashedcode):
    username = hdb.select_row(["users"], what="username", hash=int(hashedcode))['username']
    rowid = hdb.insert("posts", return_row_id=True, poster=username, title=flask.request.form.get('title'),
                       content=flask.request.form.get('content'), score=0, dateposted=datetime.now().isoformat())
    print(hdb.select(['posts']))  # don't get rid of this
    return flask.redirect(flask.url_for(".profile", hashedcode=hashedcode))


@app.route("/vote", methods=['POST'])
def vote():
    print("vote")
    username = hdb.select_row(["users"], what="username", hash=int(flask.request.form.get('voterHash')))['username']
    hdb.upsert('votes', {"postid": flask.request.form.get('postid'), "username": username},
               postid=int(flask.request.form.get('postid')), username=username, vote=flask.request.form.get('vote'))
    newScore = hdb.select_row('votes', what="sum(vote)", postid=int(flask.request.form.get('postid')))['sum(vote)']
    hdb.update('posts', {'score': newScore}, id=int(flask.request.form.get('postid')))
    print(hdb.select(['posts']))  # don't get rid of this
    return "ok"


@app.route("/delete", methods=['POST'])
def delete():
    postid = int(flask.request.form.get('postid'))
    hdb.delete("votes", where={"postid": postid})
    hdb.delete("posts", where={"id": postid})
    return "ok"


# This block is optional and can be used for testing .
# We will NOT look into its content .
# ######################################################
if __name__ == "__main__":
    app.run(port=5678, host='127.0.0.1', debug=True, use_evalex=False)
    # app.run()
