
import os  # List of module import statements
import sys  # Each one on a line
import flask
import pysqlite3 as sqlite3
import sqlite3_helper
import config

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
    return flask.render_template('profile.html', username=username)

@app.route("/create", methods=['GET', 'POST'])
def create():
    return flask.render_template('create.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    return flask.render_template('register.html')

@app.route("/<hashedcode>/feed", methods=['GET', 'POST'])
def feed(hashedcode):
    username = hdb.select(["users"], what="username", hash=int(hashedcode))[0]['username']
    return flask.render_template('feed.html', username=username, hashedcode=int(hashedcode))

@app.route("/submit", methods=['POST'])
def submit_register():
    if len(hdb.select(["users"], what="username", username=flask.request.form.get('username'))) == 0:
        hashedcode = hash(flask.request.form.get('username'))
        hdb.insert("users", username=flask.request.form.get('username'), hash=hashedcode)
        # print(hdb.select(['users']))
    else:
        hashedcode = hdb.select(["users"], what="hash", username=flask.request.form.get('username'))[0]['hash']
    print(hdb.select(['users']))
    return flask.redirect(flask.url_for(".feed", hashedcode=str(hashedcode)))

# @app.route("/form_submit", methods=['POST'])
# def submit_form():
#     if flask.request.method == 'POST':
#         conn = sqlite3.connect("data/company.db")
#         s = "INSERT INTO employees VALUES ('" + str(flask.request.form.get('first')) +"','" + str(flask.request.form.get('last')) + "','" + str(flask.request.form.get('id')) + "','" + str(flask.request.form.get('position')) + "')"
#         conn.execute(s)
#         conn.commit()
#         conn.close()
#         return flask.redirect(flask.url_for(".home"))
#
# @app.route("/delete", methods=['POST'])
# def delete():
#     if flask.request.method == 'POST':
#         conn = sqlite3.connect("data/company.db")
#         s = "DELETE FROM employees WHERE id=" + str(flask.request.args.get('emp_id')) + ";"
#         conn.execute(s)
#         conn.commit()
#         conn.close()
#         return flask.redirect(flask.url_for(".home"))
#
# @app.route("/view", methods=['GET'])
# def view():
#     conn = sqlite3.connect("data/company.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM employees WHERE id=" + str(flask.request.args.get('emp_id')) + ";")
#     record = cur.fetchall()[0]
#     first_name = record[0]
#     last_name = record[1]
#     id = record[2]
#     position = record[3]
#     return flask.render_template("view.html", first_name = first_name,  last_name = last_name, position = position, id = str(id))
#
# @app.route("/view/<emp_id>", methods=['GET'])
# def view2(emp_id):
#     conn = sqlite3.connect("data/company.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM employees WHERE id=" + str(emp_id) + ";")
#     record = cur.fetchall()[0]
#     first_name = record[0]
#     last_name = record[1]
#     id = record[2]
#     position = record[3]
#     return flask.render_template("view.html", first_name = first_name,  last_name = last_name, position = position, id = str(id))
#
# @app.route("/view_all", methods=['GET'])
# def view_all():
#     conn = sqlite3.connect("data/company.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM employees")
#     records = cur.fetchall()
#     return flask.render_template("view_all.html", records = records)


# This block is optional and can be used for testing .
# We will NOT look into its content .
# ######################################################
if __name__ == "__main__":
    # hdb.insert("users", username='sriniv62', hash="", id=5)
    # print(hdb.select(["users"], what="*", order="id DESC", limit=1))
    app.run()