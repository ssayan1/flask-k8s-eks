from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.environ["MYSQL_HOST"],
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DB"]
    )

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    return jsonify({"status": "ok", "mysql_version": version[0]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
