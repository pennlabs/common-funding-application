root = exports ? this

addItem = (e) ->
  $row = $(e).closest('tr')
  $clone = $row.clone().insertBefore $row
  $row.find('.item-amount').html(0)
  $clone.find('.add').replaceWith $('.remove').html()
  $clone.find('input').removeAttr('required')
  $clone.find('.item-category').val $row.find('.item-category').val()
  $row.find('input[type!="hidden"]').removeAttr('required').val('')

removeItem = (e) ->
  $(e).closest('tr').remove()
  updateTotal()

# updates the total amount (quant * ppu) in the column
root.calculateAmount = ->
  quantSel = 'input[name="item_quantity"]'
  ppuSel = 'input[name="item_price_per_unit"]'
  alreadyReceivedSel = 'input[name="item_funding_already_received"]'
  qVal = 0.00
  pVal = 0.00
  aVal = 0.00

  setRowAmount = ($currRow) ->
    qVal = $currRow.find(quantSel).val() or 0.00
    pVal = $currRow.find(ppuSel).val() or 0.00
    aVal = $currRow.find(alreadyReceivedSel).val() or 0.00
    $currRow.find('.item-amount').html (qVal * pVal - aVal).toFixed(2)

  # update existing items
  $('.itemrow').each (index, el) -> setRowAmount $(el)

  amountSel = ".itemrow #{quantSel}, .itemrow #{ppuSel}, .itemrow #{alreadyReceivedSel}"
  $(amountSel).live "input", (e) ->
    setRowAmount $(e.target).closest('.itemrow')
    updateTotal()

  $('#fundingalreadyreceived').on 'input', -> updateTotal()

root.updateTotal = ->
  expTotal = 0
  revTotal = 0
  # lump sum
  lumpFundingReceivedEl = $("#fundingalreadyreceived")
  funded = parseFloat lumpFundingReceivedEl.val() or 0

  $('.items-funded').html funded.toFixed(2)
  expItems = $('.expense-item .item-amount')
  revItems = $('.revenue-item .item-amount')
  expItems.each (index,el) -> expTotal = expTotal + parseFloat el.innerHTML
  revItems.each (index,el) -> revTotal = revTotal + parseFloat el.innerHTML

  $('.items-exp-total').html expTotal.toFixed(2)
  $('.items-rev-total').html revTotal.toFixed(2)

  $('.items-final-total').html (expTotal - revTotal - funded).toFixed(2)

$ ->
  calculateAmount()
  updateTotal()

  $('.add-item').live 'click', (e) ->
    addItem e.target
    return false

  $('.remove-item').live 'click', (e) ->
    removeItem e.target
    return false
