from mods.sunspec_debug_pannel.src import getModels, getOnduleurs, setPoint

import flask as fl

from src.flask_src.app import app
from src.flask_src.deco import inspect_session

@app.route("/sunspec_debug_pannel/getModels", methods=["POST"])
@inspect_session(["dev"])
def sunspec_debug_pannel_getModels():
    arguments = fl.request.get_json(force=True)
    return fl.jsonify(getModels(arguments["ip"], arguments["port"], arguments["slave_id"]))

@app.route("/sunspec_debug_pannel/getOnduleurs", methods=["POST"])
@inspect_session(["dev"])
def sunspec_debug_pannel_getOnduleurs():
    arguments = fl.request.get_json(force=True)
    return fl.jsonify(getOnduleurs(arguments["refresh"]))

@app.route("/sunspec_debug_pannel/onduleur", methods=["GET"])
@inspect_session(["dev"])
def sunspec_debug_pannel_onduleur():
    arguments = fl.request.args.to_dict()
    return fl.render_template("/mods/sunspec_debug_pannel/onduleur.html", ip=arguments["ip"], port=arguments["port"], slave_id=arguments["slave_id"])

@app.route("/sunspec_debug_pannel/setPoint", methods=["POST"])
@inspect_session(["dev"])
def sunspec_debug_pannel_setPoint():
    data = fl.request.get_json(force=True)
    if data["val"].replace('.','',1).isdigit():
        if data["val"].__contains__("."):
            val = float(data["val"])
        else:
            val = int(data["val"])
    else:
        val = data["val"]
    pointRoute = data["pointRoute"]
    erreur = setPoint(pointRoute, val, data["ip"], data["port"], data["slave_id"])
    if erreur:
        return f"Pas le bon type ou erreur sunspec {data['val'].isdigit()}", 422
    else:    
        return "Valeur mise à jour", 200

@app.route("/sunspec_debug_pannel/", methods=["GET"])
@inspect_session(["dev"])
def index():
    return fl.render_template("/mods/sunspec_debug_pannel/index.html")