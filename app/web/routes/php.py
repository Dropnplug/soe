import flask as fl
import requests
from src.flask_src.app import app
from src.flask_src.deco import inspect_session
import config
import pickle
from src.fct.logs import logs

@app.route('/php/<path:subpath>', methods=['GET', 'POST'])
@inspect_session(["dev"])
def php(subpath):
	try:
		if not config.PHP_ENABLE:
			return "PHP is not enabled"
		arg = ""
		if len(str(fl.request.query_string.decode())) > 0:
			arg = "?"+str(fl.request.query_string.decode())
		url = "http://localhost:"+str(config.PHP_PORT)+"/"+subpath+arg
		if not fl.session.get("php_session", False):
			session = requests.Session()
		else:
			session = pickle.loads(fl.session["php_session"])
		r = getattr(session, str(fl.request.method).lower())(url, verify=False, data=fl.request.form)
		fl.session["php_session"] = pickle.dumps(session)
		return fl.Response(r.content, mimetype=r.headers.get('content-type')), r.status_code
	except Exception as e:
		logs(e)