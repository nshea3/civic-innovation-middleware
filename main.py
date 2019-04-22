# -*- coding: utf-8 -*-

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import os

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for

#import requests

try:
  from googleapiclient import discovery
  from oauth2client.client import GoogleCredentials
  from google.appengine.api import app_identity
  api = discovery.build('ml', 'v2')
  project = 'elated-effect-238107'
  model_name = 'pb_model_041919'

except:
  pass


#credentials = GoogleCredentials.get_application_default()

app = Flask(__name__)


def get_prediction(features):
  #input_data = {'instances': [features]}
  parent = 'projects/%s/models/%s' % (project, model_name)
  prediction = api.projects().predict(body=features, name=parent).execute()
  return prediction


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/form')
def input_form():
  return render_template('form.html')

@app.route('/zip')
def zip_form():
  return render_template('zip.html')

@app.route('/elevated')
def elevated():
  return render_template('elevated.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/lower')
def lowrisk():
  return render_template('low_risk.html')

@app.route('/map_leadlevels')
def map_leadlevels():
  return render_template('map_pblevels.html')



@app.route('/api/predict', methods=['POST'])
def predict():
  print(request.form)
  #Make a request to the public data URL for tax parcel info

  #If that does not work, make a zillow request

  features = json.loads(request.data.decode())
  print(features)
  prediction = get_prediction(features)
  response = jsonify({'result': prediction})
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

if __name__ == "__main__":
  app.run()