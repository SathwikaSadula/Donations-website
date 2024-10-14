from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__)
CORS(auth_bp)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

@auth_bp.route('/validateLogin', methods=['POST'])
def validate_login():
    data = request.json
    username = data.get('email')
    password = data.get('pswd')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT ULN_ID, ULN_UserType FROM OPT_UserLogin
                WHERE ULN_LoginName = %s AND ULN_PWD = %s
            """, (username, password))
            user = cursor.fetchone()

            if user:
                user_id = user['ULN_UserType']
                cursor.execute("SELECT PTY_ID, PTY_ImageName FROM OPT_Party WHERE PTY_PartyType = %s", (user_id,))
                party_row = cursor.fetchone()
                if party_row:
                    party_id = int(party_row['PTY_ID'])
                    party_name = party_row['PTY_ImageName']
                else:
                    return jsonify({'error': f'Party not found.'}), 404
                
                cursor.execute("SELECT UTP_Name FROM SYS_UserType where UTP_ID = %s", (user_id,))
                user_type_row = cursor.fetchone()
                if user_type_row:
                    user_type = user_type_row['UTP_Name']
                else:
                    return jsonify({'error': f'User Type not found.'}), 404

                return jsonify({
                    'message': 'Login successful!',
                    'partyId': party_id,
                    'userType': user_type,
                    'party_name': party_name
                }), 200
            else:
                return jsonify({'error': 'Invalid username or password.'}), 401  # Unauthorized

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
