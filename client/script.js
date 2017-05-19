	$(document).ready(function() {
		
		activateTab(1);
		
	})


	function activateTab(id) {

		$(".tab").hide();
		$("#tab" + id).show();

	} // activateTab()
