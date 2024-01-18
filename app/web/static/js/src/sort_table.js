document.addEventListener('DOMContentLoaded', function () {
	let tables = document.body.getElementsByTagName("table");
	let table_i = 0;
	for (let table of tables) {
		let ths = table.getElementsByTagName("th");
		if (table.id == undefined || table.id == null || table.id == "") {
			table.id = "_table_"+table_i+"_";
		}
		let th_i = 0;
		for (let th of ths) {
			th.setAttribute("onclick","_sort_table_('"+table.id+"',"+th_i+", this);");
			th_i++;
			th.style.userSelect = "none"
		};
		table_i++;
	};

	// ajout du style des fleches dans le html
	var style = document.createElement('style');
	style.innerHTML = '.headerSortDown:after, .headerSortUp:after { content: \' \'; position: relative; left: 2px; border: 8px solid transparent;} .headerSortDown:after { top: 10px; border-top-color: var(--main-color);} .headerSortUp:after { bottom: 15px; border-bottom-color: var(--main-color);} .headerSortDown, .headerSortUp { padding-right: 10px;}'
	document.getElementsByTagName('head')[0].appendChild(style);
});

function _isNumeric_(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
};

var thAenlever = []
function _sort_table_(table_id, row_n, elem) {
	var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
	table = document.getElementById(table_id);
	switching = true;
	dir = "asc";
	while (switching) {
		switching = false;
		rows = table.rows;
		for (i = 1; i < (rows.length - 1); i++) {
			shouldSwitch = false;
			x = rows[i].getElementsByTagName("TD")[row_n];
			y = rows[i + 1].getElementsByTagName("TD")[row_n];
			x_content = x.innerHTML.toLowerCase();
			y_content = y.innerHTML.toLowerCase();
			if (_isNumeric_(x_content), _isNumeric_(y_content)) {
				x_content = parseFloat(x_content);
				y_content = parseFloat(y_content);
			};
			if (dir == "asc") {
				if (x_content > y_content) {
					shouldSwitch = true;
					break;
				};
			} else if (dir == "desc") {
				if (x_content < y_content) {
					shouldSwitch = true;
					break;
				};
			}
		}
		if (shouldSwitch) {
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
			switchcount++;
		} else {
			if (switchcount == 0 && dir == "asc") {
				dir = "desc";
				switching = true;
			};
		};
	};

	// il faut enlever la fleche des colones qui ne sont plus triés
	for (let th in thAenlever) {
		thAenlever[th].classList.remove("headerSortUp")
		thAenlever[th].classList.remove("headerSortDown")
		thAenlever.pop(th)
	}

	// ajout d'une fleche vers le haut ou le bas
	if (dir == "asc") {
		elem.classList.remove("headerSortUp")
		elem.classList.add("headerSortDown")
	} else if (dir == "desc") {
		elem.classList.remove("headerSortDown")
		elem.classList.add("headerSortUp")
	}
	thAenlever.push(elem)

	// pagination
	let pagination = false
	if (Array.from(table.classList).includes("pagnination")) {
		pagination = true
	}
	if (pagination) {
		actualiserVisibiliteLignes()
	}
};