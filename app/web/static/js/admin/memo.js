function memo_exec(path, args, kwargs) {
	let memo_fct = document.getElementById("memo_fct");
	let memo_res = document.getElementById("memo_res");
	let memo_function = document.getElementById("memo_function");
	let memo_args = document.getElementById("memo_args");
	let memo_kwargs = document.getElementById("memo_kwargs");
	let memo_execute = document.getElementById("memo_execute");
	let memo_function_content = "Function path: | ";
	path.forEach(function(element) {
		memo_function_content += element;
		memo_function_content += " | ";
	});
	memo_function.innerHTML = memo_function_content;
	memo_args.innerHTML = JSON.stringify(args, null, 4);
	memo_kwargs.innerHTML = JSON.stringify(kwargs, null, 4);
	memo_execute.onclick = function(){memo_post(path)};
	memo_fct.style.display = '';
	memo_res.style.display = 'none';
};

function memo_post(path) {
	let memo_fct = document.getElementById("memo_fct");
	let memo_res = document.getElementById("memo_res");
	let memo_args = document.getElementById("memo_args");
	let memo_kwargs = document.getElementById("memo_kwargs");
	let memo_result = document.getElementById("memo_result");
	request("POST", '/admin/memo/', {'path': path, 'args': JSON.parse(memo_args.innerHTML), 'kwargs': JSON.parse(memo_kwargs.innerHTML)}).then(result => {
		memo_result.innerHTML = JSON.stringify(result, null, 4);
		memo_fct.style.display = 'none';
		memo_res.style.display = '';
	})
};