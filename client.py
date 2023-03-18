from flask import Flask, render_template
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return render_template('search.html')

if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()