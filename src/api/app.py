import os
import json

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


if __name__ == '__main__':
   app.run()