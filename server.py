#!flask/bin/python
import json
from flask import Flask, request
from ContentBased import content_engine
from flask import Response

app = Flask(__name__)
@app.route('/mentorica',methods=['POST'])
def get_tasks():
    #json_data = jsonify(request.json)
    print(request.json)
    # Get the products in sorted order according to their recommendation in form of json
    json_response = content_engine.trainFeature('mentorica_article_test.csv', request.json)
    return Response(json_response, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False, port=9000)