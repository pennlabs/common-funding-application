addQuestion = (e) ->
  e.preventDefault()
  $row = $(event.target).closest('tr')
  $clone = $row.clone().insertAfter $row
  $row.find('.add-freeresponsequestion').replaceWith(
        $('.remove-freeresponsequestion').first().clone())

removeQuestion= (e) ->
  e.preventDefault()
  $(event.target).closest('tr').remove()

$ ->
  $('.add-freeresponsequestion').live 'click', addQuestion
  $('.remove-freeresponsequestion').live 'click', removeQuestion
  $("textarea").autosize()
