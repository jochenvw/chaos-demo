import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database - in real application, this would be a database connection
MOCK_ACCOUNTS = {
    "1234567890": {
        "accountNumber": "1234567890",
        "accountHolder": "John Doe",
        "balance": "5,432.10",
        "accountType": "Checking",
        "status": "Active"
    },
    "9876543210": {
        "accountNumber": "9876543210",
        "accountHolder": "Jane Smith",
        "balance": "12,345.67",
        "accountType": "Savings",
        "status": "Active"
    }
}

@app.route('/account')
def get_account():
    account_number = request.args.get('accountNumber')
    account_name = request.args.get('accountName')

    # Search by account number
    if account_number and account_number in MOCK_ACCOUNTS:
        return jsonify(MOCK_ACCOUNTS[account_number])
    
    # Search by name (case-insensitive)
    if account_name:
        for account in MOCK_ACCOUNTS.values():
            if account_name.lower() in account['accountHolder'].lower():
                return jsonify(account)
    
    return jsonify({"error": "Account not found"}), 404

if __name__ == '__main__':
    app.run()