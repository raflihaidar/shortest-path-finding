from flask import Flask, request, jsonify, render_template
import algoritm

app = app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

@app.route("/", methods=['GET'])
def getHome() :
       return render_template("home.html")

@app.route("/map", methods=['GET'])
def index() :
       return render_template("index.html")

@app.route("/api/data", methods=['POST'])
def short() :
        if request.is_json:
                data = request.get_json()

                origin_latitude = float(data[1].get('lat'))
                origin_longitude = float(data[1].get('lng'))
                target_latitude = float(data[0].get('lat'))
                target_longitude = float(data[0].get('lng'))

                origin_point = (origin_latitude, origin_longitude)
                target_point = (target_latitude, target_longitude)

                print("Origin Point:", origin_point)
                print("Target Point:", target_point)

                perimeter = 0.10 # Perimeter is the boundary of the roadmap

                route_coords = algoritm.generate_path(origin_point, target_point, perimeter)
                
                response = {
                "message": "Data received successfully",
                "route": route_coords
                }
                return jsonify(response), 200
        else:
                return jsonify({"message": "Request body must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)