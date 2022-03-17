
		function view_submit() {
			var xmlhttp = new XMLHttpRequest();
			var contentDiv = document.getElementById("auth_form");

			var uname = document.getElementById('uname').value;
			var pwd = document.getElementById('pwd').value;
			var table_element = document.getElementById('view_grid_container')
			xmlhttp.open("POST", "/view_json", true);
			xmlhttp.onreadystatechange = function() {
				if (xmlhttp.readyState==4 && xmlhttp.status==200) {
					viewGrid = document.getElementById('view_grid_container');
					table = JSON.parse(xmlhttp.responseText);
					viewGrid.innerHTML = '<tr><th>Owner</th><th>Item Name</th><th>Number of Items</th></tr>';
					viewGrid = viewGrid.firstChild;
					for (var i = 0; i < table.length; i++) {
						const row_node = document.createElement('tr');
						row_node.class = "table_row";
						for (var j = 0; j < table[i].length; j++) {
							const data_node = document.createElement('td');
							data_node.appendChild(
								document.createTextNode(table[i][j])
							);
							data_node.class = "table_data";
							row_node.appendChild(data_node);
						}
						viewGrid.appendChild(row_node);
						
					}
				}
			}
			xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;");
			xmlhttp.send('uname=' + encodeURIComponent(uname) + '&pwd=' + encodeURIComponent(pwd));

		}
		function mod_submit() {
			var xmlhttp = new XMLHttpRequest();
			var contentDiv = document.getElementById("command_form");

			var uname = document.getElementById('uname').value;
			var pwd = document.getElementById('pwd').value;
			var command = document.querySelector('input[name="command"]:checked').value;
			var item_name = document.getElementById('item_name').value;
			var item_no = document.getElementById('item_no').value;
			xmlhttp.open("POST", "/modify", true);
			xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;");
			xmlhttp.send('uname=' + encodeURIComponent(uname)
			+ '&pwd=' + encodeURIComponent(pwd)
			+ '&command=' + encodeURIComponent(command)
			+ '&item_name=' + encodeURIComponent(item_name)
			+ '&item_no=' + encodeURIComponent(item_no));

		}
		function show_add() {
			add_pair = document.getElementsByClassName('name_input');
			add_pair[0].style.display = "block";
			add_pair[1].style.display = "block";
			del_pair = document.getElementsByClassName('number_input');
			del_pair[0].style.display = "block";
			del_pair[1].style.display = "block";
		}
		function show_del() {
			add_pair = document.getElementsByClassName('name_input');
			add_pair[0].style.display = "block";
			add_pair[1].style.display = "block";
			del_pair = document.getElementsByClassName('number_input');
			del_pair[0].style.display = "none";
			del_pair[1].style.display = "none";
		}
		function show_mod() {
			add_pair = document.getElementsByClassName('name_input');
			add_pair[0].style.display = "block";
			add_pair[1].style.display = "block";
			del_pair = document.getElementsByClassName('number_input');
			del_pair[0].style.display = "block";
			del_pair[1].style.display = "block";
		}