addQuestion = (e) ->
  e.preventDefault()
  row = $(event.target).closest('tr')
  return unless row.find("textarea").val()
  clone = row.clone().insertAfter row
  row.find("textarea").attr("name", "freeresponsequestion")
  clone.find("textarea").val ""
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
  $(document).on 'click', '.add-freeresponsequestion', addQuestion
  $(document).on 'click', '.remove-freeresponsequestion', removeQuestion
  $("textarea").autosize()

  $(document).on 'click', '.add-funderconstraint', requireQuestion
  $(document).on 'click', '.remove-funderconstraint', ignoreQuestion
