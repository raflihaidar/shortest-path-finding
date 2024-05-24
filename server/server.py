from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import algoritm
import os

app = app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")
CORS(app, origins=["http://localhost:1234"])

@app.route("/", methods=['GET'])
def index() :
       return render_template("index.html")

@app.route("/api/data", methods=['POST'])
def short() :
        if request.is_json:
                data = request.get_json()

                origin_latitude = float(data[0].get('lat'))
                origin_longitude = float(data[0].get('lng'))
                target_latitude = float(data[1].get('lat'))
                target_longitude = float(data[1].get('lng'))

                origin_point = (origin_latitude, origin_longitude)
                target_point = (target_latitude, target_longitude)

                print("Origin Point:", origin_point)
                print("Target Point:", target_point)

                long = []
                lat = []

                perimeter = 0.10 # Perimeter is the boundary of the roadmap

                x, y = algoritm.generate_path(origin_point, target_point, perimeter)
                
                long.append(x)
                lat.append(y)

                fig_json = algoritm.plot_map(origin_point, target_point, long, lat)
                
                
                response = {
                "message": "Data received successfully",
                "data": fig_json
                }
                return jsonify(response), 200
        else:
                return jsonify({"message": "Request body must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)