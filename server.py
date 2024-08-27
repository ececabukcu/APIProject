from flask import Flask, request, jsonify
import logging
import sqlite3

logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('C:\\sqlite\\customersDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def save_customer_data(customer_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO Customers (key, name, customerCity, email)
            VALUES (?, ?, ?, ?)
        ''', (customer_data['key'], customer_data['name'], customer_data['customerCity'], customer_data['email']))
        conn.commit()
        conn.close()
        logging.info(f"Customer with key '{customer_data['key']}' updated successfully.")
        return True
    except Exception as e:
        logging.error(f"Error updating customer with key '{customer_data['key']}'. Error: {str(e)}")
        return False

@app.route('/customers/<string:key>', methods=['PUT'])
def update_customer(key):
    data = request.get_json()

    if not data or not all(k in data for k in ('name', 'variables')):
        logging.error(f"Invalid data received for customer with key '{key}'.")
        return jsonify({"message": "Invalid data"}), 400

    customer_data = {
        'key': key,
        'name': data.get('name'),
        'customerCity': data['variables'].get('customerCity'),
        'email': data['variables'].get('email')
    }

    if save_customer_data(customer_data):
        return jsonify({"message": "Customer updated successfully", "customer": customer_data}), 200
    else:
        return jsonify({"message": "Error updating customer"}), 500

@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    customers = {row['key']: dict(row) for row in cursor.fetchall()}
    conn.close()
    logging.info(f"GET request received. Returning {len(customers)} customer records.")
    return jsonify(customers), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
