import flask as fl
from src.flask_src.app import app

@app.route('/soe/', methods=['GET'])
def index_soe():
    if "time" in fl.session.keys():
        return fl.render_template('/mods/soe/pages/index/index.html')
    return fl.redirect("/soe/login/")