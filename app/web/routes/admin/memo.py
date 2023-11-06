import inspect
import flask as fl
from src.flask_src.app import app
from src.flask_src.deco import inspect_session, inspect_data

from src.memo import memo

TYPES = [bool, int, float, complex, str, bytes, bytearray, set, frozenset]

DICT_KEY_TYPES = [int, float, str, bool, bytes, bytearray]

def replace_for_json(srt):
	return srt.replace("\"","'").replace("True","true").replace("False","false").replace("None","null")

def memo_fct_td(path, fct):
	ins = inspect.getfullargspec(fct)
	vars = list(ins.args)
	vars.remove('self')
	args = []
	kwargs = {}
	if vars is not None:
		defa = 0
		if ins.defaults is not None:
			defa = len(ins.defaults)
		for i in range(len(vars)-defa):
			var = vars.pop(0)
			if var in ins.annotations:
				args.append(var+"("+str(ins.annotations[var]).replace("'","").replace("<","").replace(">","").replace("class ","")+")")
			else:
				args.append(var)
		if ins.defaults is not None:
			for i in ins.defaults:
				kwargs[vars.pop(0)] = i
	return "<td data-label='Content'><button onclick=\"memo_exec("+str(path.split('/'))+","+replace_for_json(str(args))+", "+replace_for_json(str(kwargs))+")\">execute</button></td></tr>"

def memo_values_tr(name, obj, subpath):
	tr = ""
	path = subpath+"/"+str(name)
	tr = tr+"<tr><td data-label='Name'>"+str(name)+"</td><td data-label='Type'>"+str(type(obj)).replace("<", "").replace(">", "")+"</td>"
	if not callable(obj):
		if type(obj) in TYPES:
			tr = tr+"<td data-label='Content'>"+str(obj).replace("<", "").replace(">", "")+"</td></tr>"
		else:
			tr = tr+"<td data-label='Content'><button onclick=\"location.href='/admin/memo/"+path+"'\">open</button></td></tr>"
	else:
		tr = tr+memo_fct_td(path, obj)
	return tr

def get_memo_values(obj, subpath):
	memo_values = ""
	if type(obj) in [list, tuple, dict]:
		i_var = []
		if type(obj) is dict:
			i_var = obj.keys()
		else:
			i_var = range(len(obj))
		for elem in i_var:
			el = obj[elem]
			memo_values = memo_values+memo_values_tr(elem, el, subpath)
	else:
		for elem in dir(obj):
			if '__' not in elem:
				el = obj.__getattribute__(elem)
				memo_values = memo_values+memo_values_tr(elem, el, subpath)
	return memo_values

def memo_explore(subpath_list, obj, obj_only=False):
	if len(subpath_list) > 0:
		obj_name = subpath_list.pop(0)
		if type(obj) in [list, tuple]:
			if len(obj) > int(obj_name):
				return memo_explore(subpath_list, obj[int(obj_name)])
			return None
		elif type(obj) in [dict]:
			for d in DICT_KEY_TYPES:
				var = None
				try:
					var = d(obj_name)
				except:
					pass
				if var in obj.keys():
					return memo_explore(subpath_list, obj[d(obj_name)])
			return None
		elif type(obj) not in TYPES:
			if obj_name in dir(obj):
				return memo_explore(subpath_list, obj.__getattribute__(obj_name))
			return None
		else:
			return None
	if obj in TYPES and obj_only:
		return None
	return obj	

@app.route('/admin/memo/', methods=['GET'])
@app.route('/admin/memo/<path:subpath>', methods=['GET'])
@inspect_session(["dev"])
def memo_r(subpath=None):
	memo_keys = ""
	memo_values = ""
	for k in memo.keys():
		memo_keys = memo_keys+"<a href='/admin/memo/"+k+"'>"+k+"</a><br>"
	if subpath:
		subpath_list= subpath.split('/')
		explore = memo.getattr(subpath_list[0])
		if explore is None:
			# fl.flash("'"+str(subpath_list[0])+"' introuvable")
			return fl.redirect("/admin/memo")
		subpath_list.pop(0)
		explore = memo_explore(subpath_list, explore)
		if explore is None:
			return fl.redirect("/admin/memo")
		memo_values = get_memo_values(explore, subpath)
	return fl.render_template('admin/memo.html', memo_keys=memo_keys, memo_values=memo_values)

DATA_TEMPLATE_MEMO_EXEC = {
	"path":{"type":list, "required":True},
	"args":{"type":list, "required":True},
	"kwargs":{"type":dict, "required":True}
}

@app.route('/admin/memo/', methods=['POST'])
@inspect_session(["dev"], redirect = False)
@inspect_data(DATA_TEMPLATE_MEMO_EXEC)
def memo_exec():
	post_data = fl.request.get_json(force=True)
	path = post_data["path"]
	args = post_data["args"]
	kwargs = post_data["kwargs"]
	if len(path) > 0:
		path_list = path
		obj = memo.__getitem__(path_list[0])
		path_list.pop(0)
		fct = memo_explore(path_list, obj)
		return fl.jsonify(fct(*args, **kwargs))
	return fl.jsonify({})