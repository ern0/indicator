	$(document).ready(function() {
		
		/*---------------------------------------------------------*/

		// kezdeti aktív tab száma
		initTab = 1;
		
		// induláskori játékbeli idő
		initHour = 11;
		initMin = 55;

		// óra beállításnál perc léptetési egység
		minStep = 15;

		// ennyi valós másodperc alatt telik el egy játékbeli perc
		tick = 2;

		/*---------------------------------------------------------*/

		clockTimeout = null;
		initClock(initHour,initMin);
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


	function reportClock() {
		var c = formatClock("");
		macro("/light/clock/" + c);
	} // reportClock()


	function initClock(h,m) {

		if (clockTimeout != null) clearTimeout(clockTimeout);

		clockHour = h;
		clockMin = m;

		updateClock();

	} // initClock()


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
		initClock(setHour,setMin);
		clockSetBack();
	} // clockSetOkay()


	function tickClock() {
		incClock();
		updateClock();
	} // tickClock()


	function incClock() {

		clockMin++;
		if (clockMin == 60) {
			clockMin = 0;
			clockHour++;
			if (clockHour == 24) clockHour = 0;
		}

	} // incClock()


	function updateClock() {

		paintClock();
		reportClock();

		clockTimeout = setTimeout(tickClock,tick * 1000);

	} // tickClock()
