function addItem() {
  var $row = $('.add').closest('tr');
  var $clone = $row.clone().insertBefore($row);
  //set previous amount to zero.
  $row.find('.item-amount').html(0);
  $clone.find('.add').replaceWith($('.remove').html());
  $clone.find('input').removeAttr('required');
  $row.find('input').removeAttr('required').val('');

}
function removeItem(e) {
  $(e).closest('tr').remove();
  updateTotal();
}
function makeRequired(input) {
  var $inputs = $(input).closest('tr').find('input');
  var input = $inputs.map(function(){ return $(this).val(); }).get().join('');
  if (input !== "")
    $inputs.attr('required','required');
  else
    $inputs.removeAttr('required');
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
  calculateAmount();
});


//updates the total amount (quant * ppu) in the column
function calculateAmount() {
  // selectors
  var quant_sel = 'input[name="item_quantity"]';
  var ppu_sel = 'input[name="item_price_per_unit"]';
  var alr_rcvd_sel = 'input[name="item_funding_already_received"]';
  var amt_sel = '.itemrow ' + quant_sel + ', .itemrow ' +
    ppu_sel + ', .itemrow ' + alr_rcvd_sel;

  $(amt_sel).bind('input', function(){
    // find current selection
    var curr_row = $(this).closest('.itemrow');
    var q_val = $(curr_row).find(quant_sel).val() || 0.00;
    var p_val = $(curr_row).find(ppu_sel).val() || 0.00;
    var a_val = $(curr_row).find(alr_rcvd_sel).val() || 0.00;

    $(curr_row).find('.item-amount').html((q_val * p_val - a_val).toFixed(2));

    updateTotal();
  });
}

function updateTotal(){
    var total = 0;
    console.log($('.item-amount'));
    for(var i=0; i < $('.item-amount').length ; i++){
      total = total + parseFloat($('.item-amount').get(i).innerHTML);
    }
    $('.items-total small').html(total.toFixed(2));
}
