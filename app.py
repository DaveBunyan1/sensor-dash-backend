from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': '10.250.66.171',
    'port': '5432',
    'user': 'postgres',
    'password': 'password',
    'database': 'sensordata'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_most_recent_reading(table_name):
    query = f"SELECT time, value FROM {table_name} ORDER BY time DESC LIMIT 1"
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                colnames = [desc[0] for desc in cursor.description]
                return dict(zip(colnames, result))
            else:
                return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def get_all_data(table_name):
    query = f"SELECT time, value FROM {table_name}"
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                colnames = [desc[0] for desc in cursor.description]
                return [dict(zip(colnames, row)) for row in result]
            else:
                return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

@app.route('/', methods=['GET'])
def hello():
    return "Hello, world!"

@app.route('/temperature', methods=['GET'])
def get_latest_temperature():
    result = get_most_recent_reading('temperature')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404

@app.route('/gas', methods=['GET'])
def get_latest_gas():
    print("Getting gas data")
    result = get_most_recent_reading('gas')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404

@app.route('/humidity/', methods=['GET'])
def get_latest_humidity():
    result = get_most_recent_reading('humidity')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404

@app.route('/pressure/', methods=['GET'])
def get_latest_pressure():
    result = get_most_recent_reading('pressure')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404
    
@app.route('/temperature/all', methods=['GET'])
def get_all_temperature():
    result = get_all_data('temperature')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404
    
@app.route('/humidity/all', methods=['GET'])
def get_all_humidity():
    result = get_all_data('humidity')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404
    
@app.route('/gas/all', methods=['GET'])
def get_all_gas():
    result = get_all_data('gas')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404
    
@app.route('/pressure/all', methods=['GET'])
def get_all_pressure():
    result = get_all_data('pressure')
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "No data found"}), 404
