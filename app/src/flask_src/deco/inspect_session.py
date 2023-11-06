import flask as fl
import time
import random

SESSION_TIMEOUT = 10800

def inspect_session(auth:list, redirect:bool=True, redirect_url="/login"):
	def decorator(func):
		def inner(*args, **kwargs):
			if not fl.session.get("time", False) or not fl.session.get("auth", False):
				fl.session.clear()
				if not redirect:
					fl.abort(401)
				return fl.redirect(redirect_url)
			if "dev" in fl.session["auth"]:
				return func(*args, **kwargs)
			if fl.session["time"]+SESSION_TIMEOUT < time.time():
				fl.session.clear()
				if not redirect:
					fl.abort(401)
				return fl.redirect(redirect_url)
			if len(auth) == 0:
				return func(*args, **kwargs)
			for au in auth:
				if au in fl.session["auth"]:
					return func(*args, **kwargs)
			fl.abort(403)
		decoret = inner
		decoret.__name__ = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(16))
		return decoret
	return decorator