from flask import Blueprint, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

new_item_req_bp = Blueprint('new_item_req', __name__)
CORS(new_item_req_bp)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

# New Item Request Endpoint
@new_item_req_bp.route('/newItemRequest', methods=['POST'])
def new_item_request():
    request_data = request.json
    party_id = request_data.get('partyId') 
    item_type = request_data.get('itemType')
    quantity = request_data.get('quantity')

    if not party_id or not item_type or not quantity:
        return jsonify({'error': 'User ID, item type, and quantity are required.'}), 400

    try:
        quantity = int(quantity)  # Convert quantity to integer

        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT ITP_ID FROM SYS_ItemType WHERE ITP_Name = %s", (item_type,))
            item_row = cursor.fetchone()

            if item_row:
                item_id = item_row[0]
            else:
                return jsonify({'error': 'Item not found.'}), 404

            # Insert a new item request
            cursor.execute("""
                INSERT INTO OPT_ItemsRequest (ITR_Party, ITR_Quantity, ITR_RequestDate, ITR_PendingQuantity, ITR_RequestStatus, ITR_ItemType)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (party_id, quantity, datetime.now(), quantity, 'Pending', item_id))
            request_id = cursor.lastrowid

            cursor.execute("""SELECT ITD_ID, ITD_Party, ITD_Quantity FROM OPT_ItemDonations 
                                WHERE ITD_Itemtype = %s ORDER BY ITD_Quantity DESC""", (item_id,))
            donations_row = cursor.fetchall()

            total_donated = 0
            
            for donation in donations_row:
                donation_id, donation_party, donation_quantity = donation
                q_donated = min(quantity - total_donated, donation_quantity)

                if q_donated > 0:
                    total_donated += q_donated

                    # Update the donation quantity
                    q_left_after_donation = donation_quantity - q_donated
                    if q_left_after_donation > 0:
                        cursor.execute("""
                            UPDATE OPT_ItemDonations 
                            SET ITD_Quantity = %s 
                            WHERE ITD_ID = %s
                        """, (q_left_after_donation, donation_id))
                    else:
                        cursor.execute("""
                            DELETE FROM OPT_ItemDonations 
                            WHERE ITD_ID = %s
                        """, (donation_id,))

                    # Insert into fulfilled donations
                    cursor.execute("""
                        INSERT INTO OPT_FilledDonations (FDS_FromParty, FDS_ToParty, FDS_ItemType, FDS_Quantity) 
                        VALUES (%s, %s, %s, %s)
                    """, (donation_party, party_id, item_id, q_donated))

                if total_donated >= quantity:
                    break

            # Update the item request status
            new_pending_quantity = quantity - total_donated
            new_status = "Completed" if new_pending_quantity == 0 else "Processed"
            cursor.execute("""
                UPDATE OPT_ItemsRequest 
                SET ITR_PendingQuantity = %s, ITR_RequestStatus = %s 
                WHERE ITR_ID = %s
            """, (new_pending_quantity, new_status, request_id))

            connection.commit()
            return jsonify({'message': 'Item request created successfully!'}), 201

    except Error as e:
        if connection.is_connected():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
