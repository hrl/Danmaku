(function () {
	//basic functions 
	function $(arg) {
		return document.querySelector(arg);
	}

	var tools = {
		getStyle: function(element, style) {
			// style must be a string
			var elementStyle =  window.getComputedStyle(element);
			if (style) {
				return eval("elementStyle." + style);
			} else {
				return elementStyle;
			}
		},
		insertAfter: function (newElement, targetElement) {
			var parent = targetElement.parentNode;
			if (parent.lastChild == targetElement) {
				parent.appendChild(newElement);
			} else {
				parent.insertBefore(newElement, targetElement.nextSibling);
			}
		},
		warp: function (target, height, width) {
			// create the main UI
			// warp some parent(or sibling) node for the video
			// the parent node is unchangeable
			// height and width are the size of the orgin video
			var unit = document.createElement("div");
			var video = document.createElement("div");
			var text = document.createElement("div");
			var control = document.createElement("div");
			var parent = target.parentNode;

			// unit contain the full parts
			unit.className = "edanmaku-unit";
			unit.style.height = height;
			unit.style.width = width;

			// video displays danmu
			video.className = "edanmaku-video";
			video.style.height = height;
			video.style.width = width;

			// text let user enter and send their danmu
			text.className = "edanmaku-text";
			text.style.width = width;

			// control is a bar for user to control the video
			control.className = "edanmaku-control";
			control.style.width = width;
			var button = document.createElement("div");
			var progress = document.createElement("div");
			var bar = document.createElement("div");
			var darkBar = document.createElement("div");
			var commetShow = document.createElement("div");
			var fullScreen = document.createElement("div");

			button.className = "button";
			progress.className = "progress";
			bar.className = "bar";
			darkBar.className = "darkbar";
			commetShow.className = "commetshow";
			fullScreen.className = "fullscreen";

			progress.appendChild(darkBar);
			progress.appendChild(bar);
			control.appendChild(button);
			control.appendChild(progress);
			control.appendChild(commetShow);
			control.appendChild(fullScreen);

			var progressWidth = parseInt(width) - 40*3;
			progress.style.width = progressWidth.toString() + "px";

			var autoDisappear;
			var progressQuery;
			var dragFlag;
			// control bar appears when mouse over the video
			// control bar disappears when mouse hold over more than 10s
			video.addEventListener("mouseover", function(){
				text.style.opacity = 1;
				control.style.opacity = 1;
				autoDisappear = setTimeout(function(){
					text.style.opacity = 0;
					control.style.opacity = 0;
				}, 10000);
			}, false);
			// control bar disappears when mouse leave the video
			unit.addEventListener("mouseleave", function(){
				clearTimeout(autoDisappear);
				text.style.opacity = 0;
				control.style.opacity = 0;
			}, false);
			// control the video to play or pause
			button.addEventListener("click", function(){
				if (target.paused) {
					target.play();
				} else {
					target.pause();
				}
			}, false);
			control.addEventListener("mouseover", function(){
				clearTimeout(autoDisappear);
				text.style.opacity = 1;
				control.style.opacity = 1;
			},false);
			// progress.addEventListener("click", function(evt){
				var rate = evt.layerX / progressWidth;
				target.currentTime = target.duration * rate;
				bar.style.width = (progressWidth * rate).toString() + "px";
			}, false);
			// mouse drag to adjust video
			progress.addEventListener("mousedown", function(){
				dragFlag = 1;
			}, false);
			progress.addEventListener("mousemove", function(evt){
				if (dragFlag) {
					var rate = evt.layerX / progressWidth;
					target.currentTime = target.duration * rate;
					bar.style.width = (progressWidth * rate).toString() + "px";
				}
			}, false);
			progress.addEventListener("mouseup", function(){
				dragFlag = 0;
			}, false);
			// control the video to be fullscreen
			fullScreen.addEventListener("click", function(){
				target.webkitRequestFullScreen();
			}, false);
			// update the progress bar infomation
			target.addEventListener("playing", function(){
				progressQuery = setInterval(function(){
					var playRate = target.currentTime / target.duration;
					bar.style.width = (progressWidth * playRate).toString() + "px";
				}, 60);
			}, false);
			// stop progress information query when the video pause
			target.addEventListener("pause", function(){
				clearInterval(progressQuery);
			}, false);

			// warp the elements to video
			unit.appendChild(video);
			unit.appendChild(text);
			unit.appendChild(control);
			parent.insertBefore(unit, target);
			video.appendChild(target);
		}
	}

	var edanmaku = {
		// load the core library for edanmaku
		loadSrc: function (){
			var head = document.getElementsByTagName("head")[0];
			var playerStyle = document.createElement("link");
			playerStyle.rel = "stylesheet";
			playerStyle.type = "text/css";
			playerStyle.href = "edanmaku.css";
			head.appendChild(playerStyle);
		},
		// detect the video player
		// create a div for danmu to display
		// and let user control the video
		init: function (){
			var video = $("video") || $("object");
			var height = tools.getStyle(video, "height");
			var width = tools.getStyle(video, "width");

			tools.warp(video, height, width);
			// tools.insertAfter(canvas, video);
		},
		sendDanmu: function (){},
		getDanmu: function (){}
	}

	window.onload = function () {
		edanmaku.loadSrc();
		edanmaku.init();
	}
})()
