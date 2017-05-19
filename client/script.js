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
		})
		
	})


	function activateTab(id) {

		$(".tab").hide();
		$("#tab" + id).show();

	} // activateTab()
