function closeAlert(elem) {
	elem.parentNode.style.display = "none";
}

setTimeout(function () {
	var element = document.getElementById("alert_box");
	element.classList.add('alert_hide');
}, 7000);

setTimeout(function () {
	var element = document.getElementById("alert_box");
	element.style.display = "none";
}, 8000);