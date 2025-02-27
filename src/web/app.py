import os
import requests
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

API_URL = "http://api"  # This should match your API service name in Kubernetes

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
    account_number = request.form.get('accountNumber')
    account_name = request.form.get('accountName')

    if not account_number and not account_name:
        return redirect(url_for('index'))

    try:
        # Call the API service
        response = requests.get(f"{API_URL}/account", 
                              params={'accountNumber': account_number, 
                                     'accountName': account_name})
        
        if response.status_code == 200:
            account_data = response.json()
            return render_template('account_details.html', account=account_data)
        else:
            return render_template('account_details.html', 
                                 error="Account not found or invalid input")
    
    except requests.exceptions.RequestException as e:
        return render_template('account_details.html', 
                             error="Service temporarily unavailable")

if __name__ == '__main__':
    app.run()