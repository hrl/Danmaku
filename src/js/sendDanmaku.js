window.onload = function (){
	//basic functions 
	function $(arg) {
		return document.querySelector(arg);
	}
	function sendDanmaku(startTime, ifSpolier){
		var xhr = new XMLHttpRequest();
		var body = $("input").value;
		if (body) {
			var data = {
				body: body,
				style: {},
				start_time: startTime,
				spoiler: ifSpolier
			}
		} else {
			return 0;
		}
	}
	window.addEventListener("message", function(evt){
		if (!evt.data.send) {
			var width = evt.data.width;
			var height = evt.data.height;
			$("input").style.width = (width - 80).toString() + "px";
			$("input").style.height = height.toString() + "px";
		} else {
			sendDanmaku();
		}
	}, false)
}
