const addItem = function(e) {
  const $row = $(e).closest('tr');
  const $clone = $row.clone().insertBefore($row);
  $row.find('.item-amount').html(0);
  $clone.removeClass('expense-item-add-new');
  $clone.removeClass('revenue-item-add-new');
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

  var rABS = true; // true: readAsBinaryString ; false: readAsArrayBuffer

  $("#expense-itemlist-file").on('change',function(e){
    const fileList = this.files;
    var f = fileList[0];
    var reader = new FileReader();
    reader.onload = function(e) {
      var data = e.target.result;
      if(!rABS) data = new Uint8Array(data);
      var workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});

      var first_sheet_name = workbook.SheetNames[0];
      /* Get worksheet */
      var worksheet = workbook.Sheets[first_sheet_name];
      var f_json = XLSX.utils.sheet_to_json(worksheet, {header:1,raw: true});
      console.log(f_json);

      for(var i=1; i < f_json.length; i++) {
        const $row = $(".expense-item-add-new").first();
        const $clone = $row.clone().insertBefore($row);
        $row.find('.item-amount').html(0);
        $clone.removeClass('expense-item-add-new');
        $clone.find('#item_name').val(f_json[i][0]);
        f_json[i][1] = $.trim(f_json[i][1])
        $clone.find('#item_category option').filter(function() {
                return $.trim($(this).text()) == f_json[i][1];
            }).prop('selected', true);
        $clone.find('#item_quantity').val(f_json[i][2]);
        $clone.find('#item_price_per_unit').val(f_json[i][3]);
        $clone.find('#item_funding_already_received').val(f_json[i][4]);
        $clone.find('.add').replaceWith($('.remove').html());
        $clone.find('input').removeAttr('required');
        $clone.find('[name="item_category"]').val($row.find('[name="item_category"]').val());

        $row.find('input[type!="hidden"]').removeAttr('required').val('');
        calculateAmount();
        updateTotal();
      }
    };
    if(rABS) reader.readAsBinaryString(f); else reader.readAsArrayBuffer(f);
      $("#expense-itemlist-file").replaceWith($("#expense-itemlist-file").val('').clone(true));
  });

  $("#revenue-itemlist-file").on('change',function(e){
    const fileList = this.files;
    var f = fileList[0];
    var reader = new FileReader();
    reader.onload = function(e) {
      var data = e.target.result;
      if(!rABS) data = new Uint8Array(data);
      var workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});

      var first_sheet_name = workbook.SheetNames[0];
      /* Get worksheet */
      var worksheet = workbook.Sheets[first_sheet_name];
      var f_json = XLSX.utils.sheet_to_json(worksheet, {header:1,raw: true});
      console.log(f_json);

      for(var i=1; i < f_json.length; i++) {
        const $row = $(".revenue-item-add-new").first();
        const $clone = $row.clone().insertBefore($row);
        $row.find('.item-amount').html(0);
        $clone.removeClass('revenue-item-add-new');
        $clone.find('#item_name').val(f_json[i][0]);
        $clone.find('#item_category option').filter(function() {
                return $.trim($(this).text()) == f_json[i][1];
            }).prop('selected', true);
        $clone.find('#item_quantity').val(f_json[i][2]);
        $clone.find('#item_price_per_unit').val(f_json[i][3]);
        $clone.find('.add').replaceWith($('.remove').html());
        $clone.find('input').removeAttr('required');
        $clone.find('[name="item_category"]').val($row.find('[name="item_category"]').val());

        $row.find('input[type!="hidden"]').removeAttr('required').val('');
        calculateAmount();
        updateTotal();
      }
    };
    if(rABS) reader.readAsBinaryString(f); else reader.readAsArrayBuffer(f);
    $("#revenue-itemlist-file").replaceWith($("#revenue-itemlist-file").val('').clone(true));
  });

  $(document).on('click', '.remove-item', function(e) {
    removeItem(e.target);
    return false;
  });
});
