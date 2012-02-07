var itemCount = 0;

function addItem() {
  $("div.form-actions").before(
    $("#itemrow").html()
  );
  
  itemCount++;
}

function newInputClicked(e) {
  $(e).removeClass("new")
    .attr("value","");
}

function numericOnly(event) {
  
  console.log(event.keyCode);
  
  // Allow: backspace, delete, tab and escape
  if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || 
    // Allow: Ctrl+A
    (event.keyCode == 65 && event.ctrlKey === true) || 
    // Allow: home, end, left, right
    (event.keyCode >= 35 && event.keyCode <= 39)) {
    // let it happen, don't do anything
    return;
  }
  else {
    // Ensure that it is a number and stop the keypress
    if ((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
        event.returnValue = false;
        event.preventDefault();
    }   
  }
}

$(document).ready(function() {
  addItem();
});