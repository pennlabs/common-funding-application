addQuestion = (e) ->
  e.preventDefault()
  row = $(event.target).closest('tr')
  clone = row.clone().insertAfter row
  $(event.target)
    .attr("class", "btn btn-danger remove-freeresponsequestion")
    .html("Remove")

removeQuestion= (e) ->
  e.preventDefault()
  $(event.target).closest('tr').remove()

$ ->
  $('.add-freeresponsequestion').live 'click', addQuestion
  $('.remove-freeresponsequestion').live 'click', removeQuestion
  $("textarea").autosize()
