from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_data():
    conn = psycopg2.connect(
        dbname=os.getenv('DBNAME'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),
        port=os.getenv('PORT')
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT
            COUNT(*) AS total_users,
            SUM(CASE WHEN is_approved THEN 1 ELSE 0 END) AS approved_users
        FROM nest_bot.users;
    """)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {
        "total_users": result[0],
        "approved_users": result[1]
    }

@app.route('/data', methods=['GET'])
def aggregated_data():
    data = get_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=56301)
