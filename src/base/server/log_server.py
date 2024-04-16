from flask import Flask, request, jsonify
from flask.views import MethodView

app = Flask(__name__)



@app.route('/logs', methods=['POST'])
def logs():


    log_data = request.json

    # TODO Save to the logs DB and share with client
    print("Received log:", log_data)
    return jsonify({"message": "Log received"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=8000)