from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

DATABASE_PATH = '/var/lib/power/tank.sqlite'
TABLE_NAME = 'tank'


# Ensure the database and table exist
def initialize_database():
    if not os.path.exists(DATABASE_PATH):
        create_table_sql = f'CREATE TABLE {TABLE_NAME} (time TIMESTAMP NOT NULL PRIMARY KEY, pressure INTEGER);'
        subprocess.run(['sqlite3', DATABASE_PATH, create_table_sql])


@app.route('/pressure/<int:pressure>', methods=['GET'])
def log_pressure(pressure):
    insert_sql = f"INSERT INTO {TABLE_NAME} (time, pressure) VALUES (unixepoch(), {pressure});"
    try:
        subprocess.run(['sqlite3', DATABASE_PATH, insert_sql], check=True)
        return 'Pressure logged successfully\n', 200
    except subprocess.CalledProcessError as e:
        return f'Error logging pressure: {e}\n', 500


if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=8001)
