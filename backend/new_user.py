from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error
from datetime import datetime

create_party_bp = Blueprint('create_party_bp', __name__)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

# Create Party Endpoint
@create_party_bp.route('/createParty', methods=['POST'])
def create_party():
    party_data = request.json
    if not party_data:
        return jsonify({'error': 'Invalid request data'}), 400
        
    email = party_data.get('contactEmail')
    pswd = party_data.get('password')
    add_line1 = party_data.get('addLine1')
    add_line2 = party_data.get('addLine2')
    city = party_data.get('city')
    state = party_data.get('state')
    zip_no = party_data.get('zip')
    contact_name = party_data.get('contactName')
    contact_phone = party_data.get('phone')
    party_type = party_data.get('partyType')
    party_name = party_data.get('imageName')
    #through imageName, name of the school/company is taken

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the party already exists
        cursor.execute("SELECT * FROM OPT_Party WHERE PTY_ContactEmail = %s OR PTY_Name = %s", (email, party_name))
        existing_party = cursor.fetchone()

        if existing_party:
            return jsonify({'error': f'Party with this contact email or {party_name} already exists!'}), 409  # Conflict

        # Step 1: Insert into OPT_Address
        cursor.execute("""
            INSERT INTO OPT_Address (ADD_Line1, ADD_Line2, ADD_City, ADD_State, ADD_Zip)
            VALUES (%s, %s, %s, %s, %s)
        """, (add_line1, add_line2, city, state, zip_no))

        # Step 2: Get the last inserted ADD_ID
        address_id = cursor.lastrowid

        # Step 3: Insert into SYS_UserType
        cursor.execute("""
            INSERT INTO SYS_UserType (UTP_Name, UTP_ImageName)
            VALUES (%s, %s)
        """, (party_type, party_name))

        # Step 4: Get the last inserted UTP_ID
        user_type_id = cursor.lastrowid

        # Step 5: Insert into OPT_Party
        cursor.execute("""
            INSERT INTO OPT_Party (PTY_PartyType, PTY_Name, PTY_AddressID, PTY_ContactName, PTY_ContactPhone, PTY_IsValid, PTY_ImageName, PTY_ContactEmail) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_type_id, party_name, address_id, contact_name, contact_phone, True, "abcXyz", email))

        # Step 6: Insert into OPT_UserLogin
        cursor.execute("""
            INSERT INTO OPT_UserLogin (ULN_LoginName, ULN_PWD, ULN_UserType, ULN_TSTAMP) 
            VALUES (%s, %s, %s, %s)
        """, (email, pswd, user_type_id, datetime.now()))

        connection.commit()
        return jsonify({'message': 'Party created successfully!'}), 201

    except Error as e:
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
