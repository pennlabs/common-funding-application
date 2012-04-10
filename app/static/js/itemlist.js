function addItem(button) {
  $row = $(button).closest('tr');
  $remove = $('.remove_button');
  $clone = $row.clone()
            .insertBefore($row)
            .find('.add')
            .replaceWith($('.remove').html());

  $row.find('input').val('');
}
function removeItem(e) {
  $(e).closest('tr').remove();
}

function newInputClicked(e) {
  if ($(e).hasClass("new"))
    $(e).removeClass("new")
      .attr("value","");
}
function newInputCheck(e,s) {
  if ($(e).attr("value")=="") {    
    $(e).addClass("new")
      .attr("value",s);
  }
}

function numericOnly(event) {
  
  console.log(event.keyCode);
  
  // Allow: backspace, delete, tab and escape
  if (event.keyCode == 46 || event.keyCode == 8 ||
      event.keyCode == 9 || event.keyCode == 27 || 
      // Allow: Ctrl+A
      (event.keyCode == 65 && event.ctrlKey === true) || 
      // Allow: home, end, left, right
      (event.keyCode >= 35 && event.keyCode <= 39)) {
      // let it happen, don't do anything
      return;
  }
  else {
    // Ensure that it is a number and stop the keypress
    if ((event.keyCode < 48 || event.keyCode > 57) &&
	(event.keyCode < 96 || event.keyCode > 105) &&
	(event.keyCode != 190)) {
        event.returnValue = false;
        event.preventDefault();
    }   
  }
}

function expandFunders(e) {
  $(e).parents(".app-item-row").find(".funders-list").slideToggle(500);
}

$(document).ready(function() {
  if ($(".app-item-row").length == 1) {
    addItem();
  }
});
