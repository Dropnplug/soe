import flask as fl
from src.flask_src.app import app

@app.route('/soe/', methods=['GET'])
def index_soe():
    return fl.render_template('/mods/soe/pages/index/index.html')