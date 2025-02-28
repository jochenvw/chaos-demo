import os
import json
from flask import Flask, request, jsonify

import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from dotenv import load_dotenv

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

LOGGING_INITIALIZED = False

def config_logging():
    try:
        # https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=python
        configure_azure_monitor(
            logger_name="chaos-api",
            enable_live_metrics=True,
            instrumentation_options={"azure_sdk": {"enabled": True}, "flask": {"enabled": True}}
        )
    except Exception as e:
        print(f"Error: {e}")

@app.before_request
def before_request():
    global LOGGING_INITIALIZED
    if not LOGGING_INITIALIZED:
        config_logging()   
        LOGGING_INITIALIZED = True

# Mock database
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
    logger = logging.getLogger("chaos-api")

    account_number = request.args.get('accountNumber')
    account_name = request.args.get('accountName')

    logger.info(f"Received request for account number: '{account_number}' and account name: '{account_name}'")
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
    load_dotenv()
    app.run()    