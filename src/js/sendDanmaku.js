window.onload = function (){
	//basic functions 
	function $(arg) {
		return document.querySelector(arg);
	}
	window.addEventListener("message", function(evt){
		var width = evt.data.width;
		var height = evt.data.height;
		$("input").style.width = (width - 80).toString() + "px";
		$("input").style.height = height.toString() + "px";
		$("#sendMessage").style.width = "80px";
		$("#sendMessage").style.height = height.toString() + "px";
	}, false)
	$("#sendMessage").addEventListener("click", function(){
		var xhr = new XMLHttpRequest();
		var data = {
			body: ,
			style: ,
			start_time: ,
			spoiler: 
		}
		// xhr.open("POST", , true)
	})
}
