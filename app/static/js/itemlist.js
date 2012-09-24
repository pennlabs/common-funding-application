(function(){

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
    var quantSel = 'input[name="item_quantity"]';
    var ppuSel = 'input[name="item_price_per_unit"]';
    var alreadyReceivedSel = 'input[name="item_funding_already_received"]';
    var amountSel = '.itemrow ' + quantSel + ', .itemrow ' +
      ppuSel + ', .itemrow ' + alreadyReceivedSel;

    //upon keystroke input, update totals
    $(amountSel).bind('input', function(){
      // find current selection
      var currRow = $($(this).closest('.itemrow'));
      //quantity, ppu, already received values, defaults to 0
      var qVal = currRow.find(quantSel).val() || 0.00;
      var pVal = currRow.find(ppuSel).val() || 0.00;
      var aVal = currRow.find(alreadyReceivedSel).val() || 0.00;

      currRow.find('.item-amount').html((qVal * pVal - aVal).toFixed(2));

      updateTotal();
    });
  }
  //update item total
  function updateTotal(){
      var total = 0;
      var items = $('.item-amount');
      //for each item, add on the amount
      for(var i=0; i < items.length ; i++){
        total = total + parseFloat(items.get(i).innerHTML);
      }
      $('.items-total small').html(total.toFixed(2));
  }
})();
