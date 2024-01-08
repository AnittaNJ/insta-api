import sqlite3
from flask import Flask, request, jsonify, g

DATABASE = "insta.db"
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/get-user/<user_id>")
def get_user(user_id):
    cursor = get_db().cursor()
    rows = cursor.execute(
        "SELECT id, name FROM user WHERE id = ?", (user_id,)).fetchall()

    return jsonify(rows), 200


@app.route("/get_feed/<pic_id>")
def get_feed(pic_id):
    cursor = get_db().cursor()
    rows = cursor.execute(
        "SELECT id, pic FROM picture WHERE id = ?", (pic_id,)).fetchall()

    return jsonify(rows), 200


@app.route("/delete-picture/<pic_id>", methods=["DELETE"])
def delete_picture(pic_id):
    cursor = get_db().cursor()
    cursor.execute(
        "DELETE FROM picture WHERE id = ?",
        (pic_id,))
    row = cursor.execute(
        "SELECT * FROM picture").fetchall()

    return jsonify(row), 201


@app.route("/update/<p_id>", methods=["PATCH"])
def update(p_id):
    data = request.get_json()
    new_name = data["name"]
    cursor = get_db().cursor()
    cursor.execute(
        "UPDATE user SET name = ? WHERE id = ?",
        (new_name, p_id)
    )
    rows = cursor.execute(
        "SELECT id, name FROM user").fetchall()
    return jsonify(rows), 201


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    cursor = get_db().cursor()
    new_id = data["id"]
    new_name = data["name"]
    # cursor.execute("drop table user")
    cursor.execute("INSERT INTO user VALUES (?,?)", (new_id, new_name))
    get_db().commit()

    database_users = cursor.execute(
        "SELECT id,name FROM user").fetchall()
    print(database_users)
    return jsonify(database_users), 201


@app.route("/create-picture", methods=["post"])
def create_picture():
    data = request.get_json()
    cursor = get_db().cursor()
    new_id = data["id"]
    new_pic = data["picture"]
    cursor.execute("INSERT INTO picture VALUES (?,?)", (new_id, new_pic))
    get_db().commit()

    database_users = cursor.execute(
        "SELECT id,pic FROM picture").fetchall()
    print(database_users)
    return jsonify(database_users), 201


if __name__ == "__main__":
    app.run(debug=True)
