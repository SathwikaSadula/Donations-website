from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error

fulfill_donations_bp = Blueprint('fulfill_donations', __name__)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

@fulfill_donations_bp.route('/fulfillDonations', methods=['POST'])
def fulfill_donations():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Fetch all pending item requests and not completed requests
            cursor.execute("""
                SELECT ITR_ID, ITR_Party, ITR_ItemType, ITR_Quantity, ITR_PendingQuantity 
                FROM OPT_ItemsRequest 
                WHERE ITR_RequestStatus != 'Completed'
            """)
            item_requests = cursor.fetchall()

            for request in item_requests:
                request_id, party_id, item_id, total_quantity, pending_quantity = request
                # ITR_ItemType here is FK to SYS_ItemType.ITP_ID, hence item_id
                
                if pending_quantity <= 0:
                    cursor.execute("""
                            UPDATE OPT_ItemsRequest 
                            SET ITR_RequestStatus = %s 
                            WHERE ITR_ID = %s
                        """, ('Completed',request_id))
                    continue

                # Fetch matching donations for the item type
                cursor.execute("""
                    SELECT ITD_ID, ITD_Party, ITD_Quantity 
                    FROM OPT_ItemDonations 
                    WHERE ITD_ItemType = %s 
                    ORDER BY ITD_Quantity DESC
                """, (item_id,))
                donations = cursor.fetchall()

                total_donated = 0

                for donation in donations:
                    donation_id, donation_party, donation_quantity = donation
                    q_donated = min(pending_quantity - total_donated, donation_quantity)

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

                    if total_donated >= pending_quantity:
                        break

                # Update the items request status
                if total_donated > 0:
                    new_pending_quantity = pending_quantity - total_donated
                    new_status = "Completed" if new_pending_quantity == 0 else "Processed"
                    
                    cursor.execute("""
                        UPDATE OPT_ItemsRequest 
                        SET ITR_PendingQuantity = %s, ITR_RequestStatus = %s 
                        WHERE ITR_ID = %s
                    """, (new_pending_quantity, new_status, request_id))

            connection.commit()
            return jsonify({'message': 'Checked from available donations & fulfillment process completed!'}), 200

    except Error as e:
        if connection.is_connected():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
