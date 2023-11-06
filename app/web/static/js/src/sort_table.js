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
			th.setAttribute("onclick","_sort_table_('"+table.id+"',"+th_i+");");
			th_i++;
		};
		table_i++;
	};
});

function _isNumeric_(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
};

function _sort_table_(table_id, row_n) {
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
};