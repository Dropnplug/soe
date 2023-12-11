import flask as fl
from flask import request
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
from src.memo import memo


@app.route('/dropnwifi/config/', methods=['GET'])
@inspect_session(['dev'], redirect_url="/soe/logout/")
def config_dropnwifi():
    return fl.render_template('/mods/dropnwifi/pages/config/config.html')

@app.route('/dropnwifi/config/enable_hotspot/', methods=['GET'])
@inspect_session(['dev'])
def dropnwifi_config_enable_hotspot():
    return fl.jsonify({"succes":memo["dropnwifi_data"].enable_hotspot()})

@app.route('/dropnwifi/config/disable_hotspot/', methods=['GET'])
@inspect_session(['dev'])
def dropnwifi_config_disable_hotspot():
    return fl.jsonify({"succes":memo["dropnwifi_data"].disable_hotspot()})

@app.route('/dropnwifi/config/arp_scan/', methods=['GET'])
@inspect_session(['dev'])
def dropnwifi_config_arp_scan():
    return fl.jsonify({"succes":memo["dropnwifi_data"].arp_scan(nmap_scan=True)})