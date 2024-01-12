import flask as fl
from flask import request
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
from mods.onduleur.src.utils import getLastEnergyBeforeDate, getDefauts

@app.route('/soe/onduleur/LastEnergyData/', methods=['POST'])
@inspect_session([], redirect_url="/soe/logout/")
def onduleur_last_energy():
    params = request.get_json(force=True)
    return fl.jsonify(getLastEnergyBeforeDate(mac=params["mac"], slaveID=params["slave_id"], dateLimite=params["dateLimite"]))

@app.route('/soe/onduleur/alarmes/', methods=['POST'])
@inspect_session([], redirect_url="/soe/logout/")
def onduleur_alarmes():
    params = request.get_json(force=True)
    return fl.jsonify(getDefauts(mac=params["mac"], slave_id=params["slave_id"]))