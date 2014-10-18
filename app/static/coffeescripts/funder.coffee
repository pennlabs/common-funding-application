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

requireQuestion = (e) ->
  e.preventDefault()
  button = $(event.target)
  button.siblings("input").val(button.data("qid"))
  button.attr("class", "btn btn-danger remove-funderconstraint")
    .html("Required")

ignoreQuestion = (e) ->
  e.preventDefault()
  button = $(event.target)
  button.siblings("input").val("")
  button.attr("class", "btn add-funderconstraint")
    .html("Not Required")

$ ->
  $('.add-freeresponsequestion').live 'click', addQuestion
  $('.remove-freeresponsequestion').live 'click', removeQuestion
  $("textarea").autosize()

  $('.add-funderconstraint').live 'click', requireQuestion
  $('.remove-funderconstraint').live 'click', ignoreQuestion
