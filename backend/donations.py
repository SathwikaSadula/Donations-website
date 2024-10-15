from flask import Blueprint, jsonify, request
import requests
import mysql.connector
from mysql.connector import Error

donations_bp = Blueprint('donations', __name__)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

# Create New Donation Endpoint
@donations_bp.route('/createNewDonation', methods=['POST'])
def create_new_donation():
    donation_data = request.json
    print(donation_data)
    party_id = donation_data.get('partyId')
    item_type = donation_data.get('itemType')
    quantity = donation_data.get('quantity')

    # Validate input
    if not party_id or not item_type or not quantity:
        return jsonify({'error': 'Party ID, item type, and quantity are required.'}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT ITP_ID FROM SYS_ItemType WHERE ITP_Name = %s", (item_type,))
            item_row = cursor.fetchone()

            if not item_row:
                return jsonify({'error': 'Item not found.'}), 404
            item_id = item_row[0]   
            # Insert a new donation
            cursor.execute("""
                INSERT INTO OPT_ItemDonations (ITD_Party, ITD_ItemType, ITD_Quantity)
                VALUES (%s, %s, %s)
            """, (party_id, item_id, quantity))

            connection.commit()
            
            requests.post('http://localhost:3000/fulfillDonations', json={'partyId': party_id})
            return jsonify({'message': 'Donation created successfully!'}), 201

    except Error as e:
        print(e)
        if connection.is_connected():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()

@donations_bp.route('/getDonationsbyParty/<int:party_id>', methods=['GET'])
def get_donations_by_party(party_id):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for easier access

            # Fetch data from OPT_FilledDonations
            cursor.execute("""
                SELECT 
                    it.ITP_Name AS Item_Name,
                    SUM(fd.FDS_Quantity) AS Quantity_Donated
                FROM 
                    OPT_FilledDonations fd
                JOIN 
                    SYS_ItemType it ON fd.FDS_ItemType = it.ITP_ID
                WHERE 
                    fd.FDS_FromParty = %s
                GROUP BY 
                    it.ITP_Name
            """, (party_id,))
            filled_donations = cursor.fetchall()

            # Fetch data from OPT_ItemDonations
            cursor.execute("""
                SELECT 
                    it.ITP_Name AS Item_Name,
                    SUM(id.ITD_Quantity) AS Quantity_Donated
                FROM 
                    OPT_ItemDonations id
                JOIN 
                    SYS_ItemType it ON id.ITD_ItemType = it.ITP_ID
                WHERE 
                    id.ITD_Party = %s
                GROUP BY 
                    it.ITP_Name
            """, (party_id,))
            
            item_donations = cursor.fetchall()

            filled_dict = {donation['Item_Name']: donation['Quantity_Donated'] for donation in filled_donations}
            item_dict = {donation['Item_Name']: donation['Quantity_Donated'] for donation in item_donations}

            # Combining results
            combined_donations = {}
            for item_name, quantity in filled_dict.items():
                combined_donations[item_name] = quantity + item_dict.get(item_name, 0)

            for item_name, quantity in item_dict.items():
                if item_name not in combined_donations:
                    combined_donations[item_name] = quantity

            formatted_donations = [{'Item_Name': item, 'Quantity_Donated': qty} for item, qty in combined_donations.items()]

            return jsonify(formatted_donations), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
