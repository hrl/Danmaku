window.onload = function (){
	//basic functions 
	function $(arg) {
		return document.querySelector(arg);
	}
    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }
	function sendDanmaku(danmakuId, startTime, ifSpolier){
		var xhr = new XMLHttpRequest();
		var body = $("input").value;
		if (body) {
			var data = {
				body: body,
				style: {},
				start_time: startTime,
				spoiler: ifSpolier,
			}
            xhr.open("POST", "/api/v1/danmakus/" + danmakuId + "/tsukkomis");
            xsrfToken = getCookie("_xsrf");
            xhr.setRequestHeader("X-Xsrftoken", xsrfToken);
            xhr.send(JSON.stringify(data))
		} else {
			return 0;
		}
		$("input").value = "";
	}
	window.addEventListener("message", function(evt){
		if (!evt.data.send) {
			var width = evt.data.width;
			var height = evt.data.height;
			$("input").style.width = (width - 80).toString() + "px";
			$("input").style.height = height.toString() + "px";
		} else {
			sendDanmaku(evt.data.danmakuId, evt.data.startTime, false);
		}
	}, false)
}
