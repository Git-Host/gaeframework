$(document).ready(function(){
  var edit_buttons = $("input[type=submit].confirm");
  var first_column = $('tr td:nth-child(1), tr th:nth-child(1)');

  // select all records for delete his
  $("#form_select_all").live("change", function(){
	$("input[type=checkbox].form_delete_records").attr("checked", $(this).attr("checked"));
  });

  // enable/disable edit form data
  $("#form_edit").live("change", function(){
	if ($(this).attr("checked")) {
	  edit_buttons.removeClass("disabled").attr("disabled", false);
	  first_column.show();
	}
	else {
	  edit_buttons.addClass("disabled").attr("disabled", true);
	  first_column.hide();
	}
  });
});