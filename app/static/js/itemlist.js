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

    function parseSpreadsheet(file, rowName) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var data = e.target.result;
            if(!rABS) data = new Uint8Array(data);
            var workbook = XLSX.read(data, {type: rABS ? 'binary' : 'array'});

            var first_sheet_name = workbook.SheetNames[0];
            // Get first worksheet in file
            var worksheet = workbook.Sheets[first_sheet_name];
            var f_json = XLSX.utils.sheet_to_json(worksheet, {header: 1, raw: true});
            var column_mapping = {};
            var probably_has_header = true;

            // Try to account for swapped columns
            for (var i = 0; i < f_json[0].length; i++) {
                var name = f_json[0][i].replace(/\s/g, "").toLowerCase();
                column_mapping[name] = i;

                // If a cell has just numbers, there probably is not a header
                if (/^\d+$/.test(name)) {
                    probably_has_header = false;
                    break;
                }
            }

            if (!probably_has_header) {
                column_mapping = {};
            }

            function getCellFromColumn(i, name, idx) {
                var tidx = column_mapping[name.replace(/\s/g, "").toLowerCase()];
                idx = typeof tidx !== "undefined" ? tidx : idx;
                return f_json[i][idx];
            }

            for (var i = 1; i < f_json.length; i++) {
                const $row = $(rowName).first();
                const $clone = $row.clone().insertBefore($row);
                $row.find('.item-amount').html(0);
                $clone.removeClass(rowName.substring(1));
                $clone.find('#item_name').val(getCellFromColumn(i, "Name", 0));
                var categoryText = $.trim(getCellFromColumn(i, "Category", 1));
                $clone.find('.item_category option').filter(function() {
                    return $(this).text().indexOf(categoryText) !== -1;
                }).prop('selected', true);
                $clone.find('#item_quantity').val(getCellFromColumn(i, "Quantity", 2) || 1);
                $clone.find('#item_price_per_unit').val(getCellFromColumn(i, "Price Per Unit", 3));
                $clone.find('#item_funding_already_received').val(getCellFromColumn(i, "Already Received", 4) || 0);
                $clone.find('.add').replaceWith($('.remove').html());
                $clone.find('input').removeAttr('required');

                $row.find('input[type!="hidden"]').removeAttr('required').val('');
                calculateAmount();
                updateTotal();
            }
        };
        if(rABS) reader.readAsBinaryString(file); else reader.readAsArrayBuffer(file);
    }

    $("#expense-itemlist-file").on('change',function(e){
        parseSpreadsheet(this.files[0], ".expense-item-add-new");
        $("#expense-itemlist-file").replaceWith($("#expense-itemlist-file").val('').clone(true));
    });

    $("#revenue-itemlist-file").on('change',function(e){
        parseSpreadsheet(this.files[0], ".revenue-item-add-new");
        $("#revenue-itemlist-file").replaceWith($("#revenue-itemlist-file").val('').clone(true));
    });

    $("#revenue-itemlist-button").click(function(e) {
        e.preventDefault();
        $("#revenue-itemlist-file").click();
    });

    $("#expense-itemlist-button").click(function(e) {
        e.preventDefault();
        $("#expense-itemlist-file").click();
    });

    $(document).on('click', '.remove-item', function(e) {
        removeItem(e.target);
        return false;
    });
});
