function prelogin() {
	// pre hash
	document.login.password.value = sha256(document.login.password.value);
	return true;
};