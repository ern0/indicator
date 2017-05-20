	$(document).ready(function() {
		
		/*---------------------------------------------------------*/

		// kezdeti aktív tab száma
		initTab = 1;
		
		// óra beállításnál perc léptetési egység
		minStep = 15;

		/*---------------------------------------------------------*/

		clockTimeout = null;
		reqHour = "";
		reqMin = "";
		fetchClock();
		actualTab = 0;
		activateTab(initTab);

		$(".tabsel").click(function() {
			var id = $(this).attr("id");
			$(this).addClass(id + "active");
			setTimeout(function() {
				$("#" + id).removeClass(id + "active");
			},200)
			var tabnum = id.substr(6);
			activateTab(tabnum);
		});

		$(".cell").click(function() {
			var id = $(this).attr("id");
			
			var pep = "";
			for (var i = 1; i <= 4; i++) {
				var t = "t" + i;
				if ($(this).hasClass(t + "pep1")) pep = t + "pep1";
				if ($(this).hasClass(t + "pep2")) pep = t + "pep2";
				$(this).removeClass(t + "pep1 " + t + "pep2");
			}

			$(this).addClass("cellactive");

			setTimeout(function() {
				$("#" + id).removeClass("cellactive");
				$("#" + id).addClass(pep);				
			},200)
		});
		
	})


	function activateTab(id) {

		if (id == actualTab) {
			if (id == 4) activateTab(lastTab);
			return;
		}
		lastTab = actualTab;
		actualTab = id;

		$(".tab").hide();
		$("#tab" + id).show();
		for (var i = 1; i <= 4; i++) {
			$(".tabind").removeClass("tabind" + i + "active");
		}
		$("#tabind" + id).addClass("tabind" + id + "active");

		if (id == 4) clickClock();

	} // activateTab()


	function macro(url) {
		$.ajax(url);
	} // macro()


	function formatNum(num) {
		var result = "" + num;
		if (result < 10) result = "0" + result;
		return result;
	} // formatNum()


	function formatClock(sepa) {
		return (formatNum(clockHour) + sepa + formatNum(clockMin));
	} // formatClock()


	function paintClock() {
		var c = formatClock(":");
		$("#clock").html(c);
	} // paintClock()


	function clickClock() {

		setHour = clockHour;
		setMin = clockMin;

		clockSetPaint();

	} // clickClock()


	function clockSetPaint() {
		$(".clocksethour").html( formatNum(setHour) );
		$(".clocksetmin").html( formatNum(setMin) );
	} // clockSetPaint()


	function clockSetHourPlus() {
		
		setHour++;
		if (setHour > 23) setHour = 0;
		
		clockSetPaint();

	} // clockSetHourPlus()


	function clockSetHourMinus() {
		
		--setHour;
		if (setHour < 0) setHour = 23;

		clockSetPaint();

	} // clockSetHourMinus()


	function clockSetMinPlus() {

		setMin = setMin - (setMin % minStep)
		setMin += minStep;
		if (setMin > 59) {
			setMin = 0;
			clockSetHourPlus();
			return;
		}

		clockSetPaint();
		
	} // cloxkSetMinPlus()


	function clockSetMinMinus() {

		if (setMin % minStep == 0) {
			setMin -= minStep;
		} else {
			setMin = setMin - (setMin % minStep)
		}
		if (setMin < 0) {
			setMin = 60 - minStep;
			clockSetHourMinus();
			return;
		}

		clockSetPaint();

	} // clockSetMinMinus()


	function clockSetBack() {
		activateTab(lastTab);
	} // clockSetBack()


	function clockSetOkay() {

		reqHour = setHour;
		clockHour = setHour;
		reqMin = setMin;
		clockMin = setMin;

		clockSetBack();

	} // clockSetOkay()


	function fetchClock() {

		$.ajax(
			"/clock/" + reqHour + "/" + reqMin
		).done(function(resp) {

			var r = resp.split("/");
			clockHour = r[0];
			clockMin = r[1];
			paintClock();

			setTimeout(fetchClock,1000);

		}).fail(function() {

			setTimeout(fetchClock,2000);

		});

		reqHour = "";
		reqMin = "";

	} // fetchClock()


