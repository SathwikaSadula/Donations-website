from flask import Blueprint, jsonify, request
import mysql.connector
from mysql.connector import Error


requests_bp = Blueprint('requests', __name__)

# MySQL Configuration
db_config = {
    'user': 'user_name',
    'password': 'password',
    'host': 'host_name',
    'database': 'database_name'
}

# Get Pending Requests Endpoint
@requests_bp.route('/getPendingRequests/<int:party_id>', methods=['GET'])
def get_pending_requests(party_id):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for easier access

            cursor.execute("""
                    SELECT 
                        it.ITP_Name AS Item_Name,
                        ir.ITR_Quantity AS Requested_Quantity,
                        ir.ITR_PendingQuantity AS Pending_Quantity,
                        ir.ITR_RequestStatus AS Status
                    FROM 
                        OPT_ItemsRequest ir
                    JOIN 
                        SYS_ItemType it ON ir.ITR_ItemType = it.ITP_ID
                    WHERE 
                        ir.ITR_Party = %s AND 
                        ir.ITR_RequestStatus != 'Completed'
                """, (party_id,))

            pending_requests = cursor.fetchall()

            if not pending_requests:
                return jsonify({'message': 'No pending requests found.'}), 404
            
            formatted_requests = [{
                'Item_Name': request['Item_Name'],
                'Requested_Quantity': request['Requested_Quantity'],
                'Pending_Quantity': request['Pending_Quantity'],
                'Status': request['Status']
            } for request in pending_requests]

            return jsonify(formatted_requests), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()


# Get Processed & Completed Requests Endpoint
@requests_bp.route('/getProcessedRequests/<int:party_id>', methods=['GET'])
def get_processed_requests(party_id):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for easier access

            cursor.execute("""
                SELECT 
                    ir.ITR_ID,
                    it.ITP_Name AS Item_Name,
                    p.PTY_ImageName AS Company_Name,
                    fd.FDS_Quantity AS Quantity
                FROM 
                    OPT_ItemsRequest ir
                JOIN 
                    SYS_ItemType it ON ir.ITR_ItemType = it.ITP_ID
                JOIN 
                    OPT_FilledDonations fd ON ir.ITR_ItemType = fd.FDS_ItemType
                JOIN 
                    OPT_Party p ON fd.FDS_FromParty = p.PTY_ID
                WHERE 
                    ir.ITR_Party = %s AND 
                    ir.ITR_RequestStatus != 'Pending';
            """, (party_id,))

            processed_requests = cursor.fetchall()

            if not processed_requests:
                return jsonify({'message': 'No processed requests found.'}), 404
            
            formatted_requests = [{
                'Item_Name': request['Item_Name'],
                'Company_Name': request['Company_Name'],
                'Quantity': request['Quantity']
            } for request in processed_requests]

            return jsonify(formatted_requests), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection.is_connected():
            connection.close()
