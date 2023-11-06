import flask as fl
import random

def inspect_data(template:dict, data=None, c_type:bool=True, c_required:bool=True, strict_type=True):
	def decorator(func):
		def inner(*args, **kwargs):
			if len(template) == 0:
				return func(*args, **kwargs)
			p_data = data
			if p_data is None:
				if len(fl.request.data) > 0:
					p_data = fl.request.get_json(force=True)
				elif len(fl.request.form) > 0:
					p_data = fl.request.form
			for key, value in template.items():
				if c_required and value["required"]:
					if key not in p_data:
						fl.abort(400)
				if c_type:
					if key in p_data.keys():
						if value["type"] != type(p_data[key]):
							if not strict_type and type(p_data[key]) == str and value["type"] in [int, float, bool] and p_data[key].isnumeric():
								pass
							else:
								fl.abort(400)
			return func(*args, **kwargs)
		decoret = inner
		decoret.__name__ = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(16))
		return decoret
	return decorator