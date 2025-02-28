import os
import requests
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

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
            logger_name="chaos-web",
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


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/lookup', methods=['POST'])
def lookup():
    logger = logging.getLogger("chaos-web")
    account_number = request.form.get('accountNumber')
    account_name = request.form.get('accountName')

    if not account_number and not account_name:
        return redirect(url_for('index'))

    try:
        # Call the API service
        response = requests.get(f"http://api/account", 
                              params={'accountNumber': account_number, 
                                     'accountName': account_name})
        
        if response.status_code == 200:
            account_data = response.json()
            return render_template('account_details.html', account=account_data)
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response content: {response.text}")
            logger.error(f"Error: API returned status code {response.status_code}")
            return render_template('account_details.html', 
                                 error="Account not found or invalid input")
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling API service: {str(e)}")
        logger.error(f"Error calling API service: {str(e)}")
        return render_template('account_details.html', 
                             error="Service temporarily unavailable")

if __name__ == '__main__': 
    load_dotenv()
    app.run()


