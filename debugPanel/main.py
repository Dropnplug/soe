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
    if fl.request.form["val"].replace('.','',1).isdigit():
        if fl.request.form["val"].__contains__("."):
            val = float(fl.request.form["val"])
        else:
            val = int(fl.request.form["val"])
    else:
        val = fl.request.form["val"]
    pointRoute = fl.request.form["pointRoute"].split(",")
    erreur = setPoint(pointRoute, val)
    if erreur:
        return f"Pas le bon type ou erreur sunspec {fl.request.form['val'].isdigit()}", 422
    else:    
        return "Valeur mise à jour", 200

@app.route("/", methods=["GET"])
def index():
    return fl.render_template("/index.html")

app.run(host="0.0.0.0", debug=True, port=8080)