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

class CommonFieldsFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        # Get environment variables once during initialization
        self.app_version = os.getenv('APP_VERSION', 'unknown')

    def filter(self, record):
        # Add common fields to every log record
        record.app_version = self.app_version
        return True

def config_logging():
    try:
        configure_azure_monitor(
            logger_name="chaos-api",
            enable_live_metrics=True,
            instrumentation_options={"azure_sdk": {"enabled": True}, "flask": {"enabled": True}}
        )
        # Get the logger and add our filter
        logger = logging.getLogger("chaos-api")
        logger.addFilter(CommonFieldsFilter())
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

    # Search by account number
    if account_number and account_number in MOCK_ACCOUNTS:
        logger.info("Account found by number", extra={
            'account_number': account_number,
            'account_name': MOCK_ACCOUNTS[account_number]['accountHolder'],
            'lookup_type': 'account_number'
        })
        return jsonify(MOCK_ACCOUNTS[account_number])
    
    # Search by name (case-insensitive)
    if account_name:
        for account in MOCK_ACCOUNTS.values():
            if account_name.lower() in account['accountHolder'].lower():
                logger.info("Account found by name", extra={
                    'account_number': account['accountNumber'],
                    'account_name': account['accountHolder'],
                    'lookup_type': 'account_name'
                })
                return jsonify(account)
    
    logger.error("Account not found", extra={
        'account_number': account_number,
        'account_name': account_name,
        'lookup_type': 'account_number' if account_number else 'account_name'
    })
    return jsonify({"error": "Account not found"}), 404

if __name__ == '__main__': 
    load_dotenv()
    app.run()    