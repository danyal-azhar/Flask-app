from flask import Blueprint, request, jsonify
from extensions import mysql


main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    return 'Hello World!'


@main.route('/insert', methods=['POST'])
def insert():
    try:
        name = request.json['name']
        if not name:
            return jsonify({'error': 'Name field is empty'}), 400
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'User added successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


@main.route('/fetch', methods=['GET'])
def fetch():
    try:
        name = request.json.get('name')
        if not name:
            return jsonify({'error': 'Name field is empty'}), 400
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT name FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return jsonify({'name': user[0]}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@main.route ('/update', methods=['PUT'])
def update():
    try:

        current_name= request.json.get('current_name')
        updated_name = request.json.get('updated_name')
        if not current_name or not updated_name:
            return jsonify({'error': 'Name fields are required'}), 400
        else:
            cursor= mysql.connection.cursor()
            cursor.execute("UPDATE users set name = %s WHERE name = %s", (updated_name, current_name))
            if cursor.rowcount == 0:
                return jsonify({'error': 'User not found'}), 404
            mysql.connection.commit()
            cursor.close()
            return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@main.route('/remove', methods=['DELETE'])
def remove():
    try:
        name = request.json['name']
        if not name:
            return jsonify({'error': 'Name field is empty'}), 400
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM users WHERE name=%s", (name,))
            mysql.connection.commit()
            if cursor.rowcount==0:
                return jsonify({'message': 'Entered name not found'}, 404)
            cursor.close()
            return jsonify({'message': 'User delete successfully'}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

