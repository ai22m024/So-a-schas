from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import negative_summarizer as neg_sum
import json 

@app.route('/search/<location_name>', methods = ['GET'])
@cross_origin()
def search(location_name):
    if request.method == 'GET':
        """return the information for <user_id>"""
        
        summarizer = neg_sum.NegativeSummarizer(location_name)
        summary_list = summarizer.summarize(6)
        print(summary_list)
        return json.dumps(summary_list)
app.run(port = 4999)

