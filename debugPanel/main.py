from sunData import getModels
import flask as fl

templateFolder = "./web/templates"
staticFolder = "./web/static"

app = fl.Flask(__name__, template_folder=templateFolder, static_folder=staticFolder)

@app.route("/getModels", methods=["GET"])
def _getModels():
    return fl.jsonify(getModels())

@app.route("/", methods=["GET"])
def index():
    return fl.render_template("/index.html")

app.run(host="0.0.0.0", debug=True, port=8080)