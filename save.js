function saveSettings(){

//	var results = document.getElementById("input-w").value + "</br>" +
//		document.getElementById("input-a").value + "</br>" +
//		document.getElementById("input-s").value + "</br>" +
//		document.getElementById("input-d").value + "</br>" +
//		document.getElementById("input-space").value + "</br>";
//	document.getElementById ("testOutput").innerHTML = results;
	var dict = {};
	var keys = ["w","a", "s", "d", "space"];

	console.log("input-"+keys[0]);

	for(i = 0; i<keys.length;i++){
		dict["input-"+keys[i]] = document.getElementById("input-"+keys[i]).value;
	}


	document.getElementById ("testOutput").innerHTML = dict["input-w"];
}
