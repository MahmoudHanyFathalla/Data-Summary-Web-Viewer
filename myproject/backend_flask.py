from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql.cursors
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='tmsa7',
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)

def fetch_table_data(start_date, end_date, user_name=None):
    try:
        with connection.cursor() as cursor:
            if user_name:
                sql = "SELECT * FROM data_summary WHERE start_date >= %s AND end_date <= %s AND username = %s"
                cursor.execute(sql, (start_date, end_date, user_name))
            else:
                sql = "SELECT * FROM data_summary WHERE start_date >= %s AND end_date <= %s"
                cursor.execute(sql, (start_date, end_date))
            data = cursor.fetchall()
            for row in data:
                row['start_time'] = str(row['start_time']) if row['start_time'] else None
                row['end_time'] = str(row['end_time']) if row['end_time'] else None
                duration_hours = int(row['duration_hours']) if row['duration_hours'] else 0
                duration_minutes = int(row['duration_minutes']) if row['duration_minutes'] else 0
                row['duration'] = f"{duration_hours} hours {duration_minutes} minutes"
                row['start_date'] = str(row['start_date']) if row['start_date'] else None
                row['end_date'] = str(row['end_date']) if row['end_date'] else None
            return data
    except Exception as e:
        print("Error fetching data from MySQL:", e)
        return []

@app.route('/api/table_data')
def get_table_data():
    start_date_str = request.args.get('start_date', datetime.now().date().isoformat())
    end_date_str = request.args.get('end_date', datetime.now().date().isoformat())
    user_name = request.args.get('name')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    data = fetch_table_data(start_date, end_date, user_name)
    return jsonify(data)


def get_unique_usernames():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT username FROM data_summary"
            cursor.execute(sql)
            result = cursor.fetchall()
            usernames = [row['username'] for row in result]
            return usernames
    except Exception as e:
        print("Error fetching usernames from MySQL:", e)
        return []

@app.route('/api/usernames')
def get_usernames():
    usernames = get_unique_usernames()
    return jsonify(usernames)


if __name__ == '__main__':
    app.run(debug=True)
