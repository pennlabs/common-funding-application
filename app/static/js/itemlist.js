const addItem = function(e) {
  const $row = $(e).closest('tr');
  const $clone = $row.clone().insertBefore($row);
  $row.find('.item-amount').html(0);
  $clone.find('.add').replaceWith($('.remove').html());
  $clone.find('input').removeAttr('required');
  $clone.find('[name="item_category"]').val($row.find('[name="item_category"]').val());
  $row.find('input[type!="hidden"]').removeAttr('required').val('');
};

const removeItem = function(e) {
  $(e).closest('tr').remove();
  updateTotal();
};

// updates the total amount (quant * ppu) in the column
const calculateAmount = function() {
  const quantSel = 'input[name="item_quantity"]';
  const ppuSel = 'input[name="item_price_per_unit"]';
  const alreadyReceivedSel = 'input[name="item_funding_already_received"]';
  let qVal = 0.00;
  let pVal = 0.00;
  let aVal = 0.00;

  const setRowAmount = function($currRow) {
    qVal = $currRow.find(quantSel).val() || 0.00;
    pVal = $currRow.find(ppuSel).val() || 0.00;
    aVal = $currRow.find(alreadyReceivedSel).val() || 0.00;
    $currRow.find('.item-amount').html(((qVal * pVal) - aVal).toFixed(2));
  };

  // update existing items
  $('.itemrow').each((index, el) => setRowAmount($(el)));

  const amountSel = `.itemrow ${quantSel}, .itemrow ${ppuSel}, .itemrow ${alreadyReceivedSel}`;
  $(document).on("input", amountSel, function(e) {
    setRowAmount($(e.target).closest('.itemrow'));
    updateTotal();
  });
};

const updateTotal = function() {
  let expTotal = 0;
  let recvTotal = parseFloat($("#fundingalreadyreceived").val() || 0);
  let revTotal = 0;

  const expItems = $('.expense-item .item-amount');
  const recvItems = $('.expense-item .item-received');
  const revItems = $('.revenue-item .item-amount');
  expItems.each((index,el) => expTotal = expTotal + parseFloat(el.innerHTML));
  recvItems.each((index,el) => recvTotal = recvTotal + parseFloat(el.innerHTML));
  revItems.each((index,el) => revTotal = revTotal + parseFloat(el.innerHTML));

  $('.items-exp-total').html(expTotal.toFixed(2));
  $('.items-recv-total').html(recvTotal.toFixed(2));
  $('.items-rev-total').html(revTotal.toFixed(2));

  $('.items-final-total').html((expTotal - recvTotal - revTotal).toFixed(2));
};

$(function() {
  calculateAmount();
  updateTotal();

  $(document).on('click', '.add-item', function(e) {
    addItem(e.target);
    return false;
  });

  $(document).on('click', '.remove-item', function(e) {
    removeItem(e.target);
    return false;
  });
});
