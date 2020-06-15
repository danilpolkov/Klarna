import flask
from flask import request, jsonify

import pandas as pd

from pathlib import Path
import sys

PATH = '/Users/danil/Documents/github/Klarna/'
sys.path.append(str(PATH))

from src.pickle_utils import read_pickle

# read recommendations
pred = pd.read_csv(PATH + 'data/processed/recommendations.csv')
recoms = {u: r.tolist() for u, r in zip(pred['visitorid'], pred.iloc[:, 1:].values)}

most_rated = read_pickle(PATH + 'data/processed/most_rated.pickle')

# create api app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Klarna test API</h1><p> small instruction, pass user_id to 'recom/v1?visitorid=user_id  to get 100 recommendations</p>"


@app.route('/recom/v1', methods=['GET'])
def get_recoms():
    # Check if an ID was provided as part of the URL.
    # If visitorid is provided, assign it to a variable.
    # If no visitorid is provided, display an error in the browser.
    print(request.args['visitorid'])
    if 'visitorid' in request.args:
        visitorid = int(request.args['visitorid'])
        result = recoms.get(visitorid, most_rated)
    else:
        result = "<h1>Klarna test API</h1><p> cant fild proper argument, looking for 'visitorid'</p>"

    return jsonify(result)


app.run()