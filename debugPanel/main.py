from sunData import getModels
from sunData import setPoint
import flask as fl

templateFolder = "./web/templates"
staticFolder = "./web/static"

app = fl.Flask(__name__, template_folder=templateFolder, static_folder=staticFolder)

@app.route("/getModels", methods=["GET"])
def _getModels():
    return fl.jsonify(getModels())

@app.route("/setPoint", methods=["POST"])
def _setPoint():
    data = fl.request.get_json(force=True)
    if data["val"].replace('.','',1).isdigit():
        if data["val"].__contains__("."):
            val = float(data["val"])
        else:
            val = int(data["val"])
    else:
        val = data["val"]
    pointRoute = data["pointRoute"]
    erreur = setPoint(pointRoute, val)
    if erreur:
        return f"Pas le bon type ou erreur sunspec {data['val'].isdigit()}", 422
    else:    
        return "Valeur mise à jour", 200

@app.route("/", methods=["GET"])
def index():
    return fl.render_template("/index.html")

@app.route("/test", methods=["GET"])
def test():
    return fl.render_template("/test.html")

app.run(host="0.0.0.0", debug=True, port=8080)