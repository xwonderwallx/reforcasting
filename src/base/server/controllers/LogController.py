from flask import Flask, request, jsonify
from flask.views import MethodView

app = Flask(__name__)


class LogController(MethodView):

    def post(self):
        log_data = request.json
        print("Received log:", log_data)
        return jsonify({"message": "Log received"}), 201


app.add_url_rule('/logs', view_func=LogController.as_view('log_controller'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
