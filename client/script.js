	$(document).ready(function() {
		
		initClock(6,0);
		actualTab = 0;
		activateTab(1);

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


	function formatClock(sepa) {

		var h = "" + clockHour;
		if (clockHour < 10) h = "0" + h;
		var m = "" + clockMin;
		if (clockMin < 10) m = "0" + m;

		return (h + sepa + m);
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

		clockHour = h;
		clockMin = m;

		paintClock();
		reportClock();

	} // initClock()


	function clickClock() {

		setHour = clockHour;
		setMin = clockMin;

	} // clickClock()
