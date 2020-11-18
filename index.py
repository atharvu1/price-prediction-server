from flask import Flask, request
from flask_cors import CORS, cross_origin
import pickle
import json
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))


@app.route("/")
#@cross_origin(allow_headers=['Content-Type'])
def home():
    return 'Home page'


@app.route( '/get_price', methods=['POST'] )
# @cross_origin(origin='localhost', allow_headers=['Content-Type'])
def analyse_text():
    data = request.data.decode('UTF-8')
    #data = request.data
    # print("Raw data ", data)
    data = json.loads(data)
    area = int(data['area'])
    bhk = int(data['bhk'])
    bathroom = int(data['bathroom'])
    location = data['location']

    print(area)
    print(bhk)
    print(bathroom)
    print(location)

    with open( "./columns.json", "r" ) as f:
        data_columns = json.load( f )['data_columns']
        locations = data_columns[3:]
    try:
        loc_index = data_columns.index( location.lower() )
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = area
    x[1] = bathroom
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    prediction = round(model.predict( [x] )[0], 2 )
    # response = make_response()
    '''
    response.headers.add( "Access-Control-Allow-Origin", "*")
    response.headers.add( 'Access-Control-Allow-Headers', "*" )
    response.headers.add( 'Access-Control-Allow-Methods', "*" )
    '''
    #response.data(prediction)
    print(prediction)
    return str(prediction)


if __name__ == "__main__":
    app.run( debug=True )  # for deployment turn it off(False)
