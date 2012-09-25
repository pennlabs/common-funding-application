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
  updateTotal();
});

//updates the total amount (quant * ppu) in the column
function calculateAmount() {
  // selectors
  var quantSel = 'input[name="item_quantity"]';
  var ppuSel = 'input[name="item_price_per_unit"]';
  var alreadyReceivedSel = 'input[name="item_funding_already_received"]';
  var qVal = 0;
  var pVal = 0.00;
  var aVal = 0.00;
  var currRow;
 
  // helper, calculates the row amount for the passed row
  var setRowAmount = function(currRow){
    //defaults to 0
    qVal = currRow.find(quantSel).val() || 0.00;
    pVal = currRow.find(ppuSel).val() || 0.00;
    aVal = currRow.find(alreadyReceivedSel).val() || 0.00;
    currRow.find('.item-amount').html((qVal * pVal - aVal).toFixed(2));
  }

  //update the existing items
  var existingItemEls = $('.app-itemrow');
  for(var i=0; i < existingItemEls.length; i++){
    currRow = $(existingItemEls.get(i));
    setRowAmount(currRow);
  }

  //selector for any item, either existing (app-itemrow) or new
  var amountSel = '.itemrow ' + quantSel + ', .itemrow ' +
    ppuSel + ', .itemrow ' + alreadyReceivedSel +
    ', .app-itemrow ' + quantSel + ', .app-itemrow ' + 
    ppuSel + ', .app-itemrow ' + alreadyReceivedSel;

  //upon keystroke input, update totals
  $(amountSel).bind('input', function(){
    // find current selection
    currRow = $($(this).closest('.itemrow, .app-itemrow'));
    setRowAmount(currRow);
    updateTotal();
  });
  
  var lumpFundingReceivedEl = $("#fundingalreadyreceived");
  //upon changing lump funding, updateTotal
  lumpFundingReceivedEl.bind('input', function(){
    updateTotal();
  });
}
//update item total
function updateTotal(){
    var total = 0;
    //lump sum (existing funding) calculations and generation
    var lumpFundingReceivedEl = $("#fundingalreadyreceived");
    var funded = parseFloat(lumpFundingReceivedEl.val()) || 0;
 
    $('.items-funded span').html(funded);
    var items = $('.item-amount');
    //for each item, add on the amount
    for(var i=0; i < items.length ; i++){
      total = total + parseFloat(items.get(i).innerHTML);
    }
    //remove existing funding
    $('.items-total small').html(total.toFixed(2) - funded);
}

$(document).ready(function() {
  if ($(".app-item-row").length == 1) {
    addItem();
  }
  calculateAmount();
});
