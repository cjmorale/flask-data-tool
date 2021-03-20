import os
from flask import Flask,  request, render_template
import requests

import pandas as pd
from pandas.io.json import json_normalize

app = Flask(__name__)


@app.route("/", methods =["GET", "POST"])
def index(databricks_result='', databricks_data=pd.DataFrame(),
          sf_result='', sf_data=pd.DataFrame(),
          step_result='', step_data=pd.DataFrame()):

    if request.args.get('databricks', ''):
        databricks_result = request.args['databricks']
        databricks_data = process_text(request.args['databricks'])

    if request.args.get('salesforce', ''):
        sf_result = request.args['salesforce']
        sf_data = process_soql(request.args['salesforce'])

    if request.args.get('step', ''):
        step_result = request.args['step']
        step_data = process_soql(request.args['step'])

    return render_template('index.html', databricks_result=databricks_result, databricks_data=databricks_data,
                           sf_result=sf_result, sf_data=sf_data,
                           step_result=step_result, step_data=step_data)

def process_text(text):
    json_data = requests.get('https://swapi.dev/api/planets/').json()['results']
    df = pd.DataFrame(json_normalize(json_data)).drop(['films', 'residents'], axis=1)
    print(type(df))
    data = df.to_html()

    return data


def process_soql(text):
    url = "https://test.salesforce.com/services/oauth2/token?grant_type=password&client_id=3MVG9d3kx8wbPieE1owJgtExii9jGmRDjErGmLQxQReZbPft3i9IuGZONgHIgXyUdwrz19npqCkVZcFZyA01o&client_secret=EA45A27823F561395D2B598B48F46F1E342F2E5A453CD4F58B911F149C180EA3&username=carlo.morales@jhi.crm.ac&password=@Pacmet9149rMAWBtcY9Ro1zzg3VByXPZ9"

    payload = {}
    headers = {
        'Cookie': 'BrowserId=wnza7IaaEeuPyr1Y5pp0Og'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    token = response['access_token']

    header_soql = {
        'Authorization': 'Bearer {}'.format(token)
    }


    url = "https://janushenderson--ac.my.salesforce.com/services/data/v51.0/query/?q=" + text


    response = requests.request("GET", url, headers=header_soql, data=payload)

    df = pd.DataFrame(response.json()['records']).drop('attributes', axis = 1)
    data = df.to_html()

    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)