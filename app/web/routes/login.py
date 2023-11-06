import flask as fl
import hashlib
import time

from src.flask_src.app import app
from src.flask_src.deco import inspect_data, inspect_session
from src.mysql_src import mysqlite

@app.route('/login/', methods=['GET'])
def get_login():
	return fl.render_template('login.html')

DATA_TEMPLATE_LOGIN = {
	"email":{"type":str, "required":True},
	"password":{"type":str, "required":True},
	"redirect":{"type":str, "required":False},
	"session_coll":{"type":str, "required":False}
}

TABLE_NAME = "user"
COLL_FOR_SESSION = []
COLL_FOR_SESSION_BLACKLIST = ["password", "auth_id"]
AUTH_BLACKLIST = ["name", "id"]

res = mysqlite.exec("PRAGMA table_info("+TABLE_NAME+");")
for r in res:
	if r["name"] not in COLL_FOR_SESSION_BLACKLIST:
		COLL_FOR_SESSION.append(r["name"])

@app.route('/login', methods=['POST'])
@inspect_data(DATA_TEMPLATE_LOGIN)
def post_login():
	post_data = fl.request.form
	email = str(post_data["email"])
	password = str(post_data["password"])
	redirect = "/"
	if "redirect" in post_data.keys():
		redirect = str(post_data["redirect"])
	digest = hashlib.pbkdf2_hmac('sha256', password.encode(), email.encode(), 10000)
	password = digest.hex()
	coll_for_session = COLL_FOR_SESSION
	if "session_coll" in post_data.keys():
		session_coll = str(post_data["session_coll"]).split(' ')
		for coll in session_coll:
			if coll not in coll_for_session:
				coll_for_session.append(coll)
	if "auth_id" not in coll_for_session:
		coll_for_session.append("auth_id")
	res = mysqlite.exec("SELECT "+",".join(coll_for_session)+" FROM "+TABLE_NAME+" WHERE email = ? AND password = ? AND enabled = 1;", (email, password))
	if len(res) > 0:
		for coll in COLL_FOR_SESSION:
			fl.session[coll] = res[0][coll]
		fl.session["time"] = time.time()
		res = mysqlite.exec("SELECT * FROM auth WHERE id = ?", (res[0]["auth_id"],))
		auth = []
		if len(res) > 0:
			for k, v in res[0].items():
				if k not in AUTH_BLACKLIST and v:
					auth.append(k)
		fl.session["auth"] = auth
		return fl.redirect(redirect)
	fl.flash('Email ou mot de passe incorrect')
	return fl.redirect(fl.request.referrer)

@app.route('/logout', methods=['GET'])
def logout():
	fl.session.clear()
	return fl.redirect("/")