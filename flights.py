from flask import Flask, render_template, request
import datetime
from flask_cors import CORS
import json
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return render_template('flights.html')

@app.route('/api/getFlights')
def get_api_flights():

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    url = "https://www.allegiantair.com/graphql"

    payload = json.dumps({
        "operationName": "flights",
        "variables": {
            "flightSearchCriteria": {
                "tripType": "ONEWAY",
                "origin": origin,
                "destination": destination,
                "departDate": {
                    "plusDays": 60,
                    "minusDays": 0,
                    "date": date
                },
                "adultsCount": 1,
                "childrenCount": 0,
                "lapInfantCount": 0,
                "lapInfantDobs": []
            }
        },
        "query": "query flights($flightSearchCriteria: FlightSearchCriteriaInput!) {\n  transactionId\n  flights(flightSearchCriteria: $flightSearchCriteria) {\n    departing {\n      ...FlightOptionFragment\n      __typename\n    }\n    returning {\n      ...FlightOptionFragment\n      __typename\n    }\n    loyaltyFare {\n      discount\n      __typename\n    }\n    __typename\n  }\n  order {\n    items {\n      id\n      __typename\n      ... on FlightOrderItem {\n        flight {\n          id\n          __typename\n        }\n        __typename\n      }\n      ... on ShowOrderItem {\n        id\n        type\n        show {\n          categoryCode\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n}\n\nfragment FlightOptionFragment on FlightOption {\n  id\n  flight {\n    id\n    number\n    origin {\n      displayName\n      code\n      __typename\n    }\n    destination {\n      code\n      displayName\n      __typename\n    }\n    departingTime\n    arrivalTime\n    isOvernight\n    __typename\n  }\n  strikethruPrice\n  price\n  baseFare\n  availableSeatsCount\n  discountType\n  totalDiscountValue\n  incentiveType\n  incentiveSavedAmount\n  incentiveReturnDate\n  onTimePerformance {\n    onTimeArrival\n    thirtyMinuteLate\n    cancellations\n    disclaimer\n    __typename\n  }\n  __typename\n}\n"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    js = json.loads(response.content)
    return js

@app.route('/getflights')
def get_flights():
    url = "https://www.allegiantair.com/graphql"

    payload = json.dumps({
        "operationName": "flights",
        "variables": {
            "flightSearchCriteria": {
                "tripType": "ONEWAY",
                "origin": "AVL",
                "destination": "PIE",
                "departDate": {
                    "plusDays": 60,
                    "minusDays": 0,
                    "date": "2022-10-13"
                },
                "adultsCount": 1,
                "childrenCount": 0,
                "lapInfantCount": 0,
                "lapInfantDobs": []
            }
        },
        "query": "query flights($flightSearchCriteria: FlightSearchCriteriaInput!) {\n  transactionId\n  flights(flightSearchCriteria: $flightSearchCriteria) {\n    departing {\n      ...FlightOptionFragment\n      __typename\n    }\n    returning {\n      ...FlightOptionFragment\n      __typename\n    }\n    loyaltyFare {\n      discount\n      __typename\n    }\n    __typename\n  }\n  order {\n    items {\n      id\n      __typename\n      ... on FlightOrderItem {\n        flight {\n          id\n          __typename\n        }\n        __typename\n      }\n      ... on ShowOrderItem {\n        id\n        type\n        show {\n          categoryCode\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n}\n\nfragment FlightOptionFragment on FlightOption {\n  id\n  flight {\n    id\n    number\n    origin {\n      displayName\n      code\n      __typename\n    }\n    destination {\n      code\n      displayName\n      __typename\n    }\n    departingTime\n    arrivalTime\n    isOvernight\n    __typename\n  }\n  strikethruPrice\n  price\n  baseFare\n  availableSeatsCount\n  discountType\n  totalDiscountValue\n  incentiveType\n  incentiveSavedAmount\n  incentiveReturnDate\n  onTimePerformance {\n    onTimeArrival\n    thirtyMinuteLate\n    cancellations\n    disclaimer\n    __typename\n  }\n  __typename\n}\n"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    js = json.dumps(json.loads(response.content)['data']['flights']['departing'])

    file = open('flights.json', 'w')
    file.write(js)
    file.close()

    with open('flights.json') as fd:
        data = json.load(fd)
    
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
