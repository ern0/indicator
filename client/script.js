	$(document).ready(function() {
		
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
			for (var i = 1; i <= 3; i++) {
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

		$(".tab").hide();
		$("#tab" + id).show();
		$(".tabind").removeClass("tabind1active tabind2active tabind3active")
		$("#tabind" + id).addClass("tabind" + id + "active");

	} // activateTab()


	function macro(url) {
		$.ajax(url);
	}