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

addEmail = (e) ->
  e.preventDefault()
  input = $("#cc-email").val()
  $("#cc-email").val ""
  return unless input
  return if $('input[name="cc_email"]').filter(() -> this.value == input).length
  hidden_element = $("<input type='hidden' name='cc_email' />").val(input)
  list_element = $("<li class='list-group-item' />").text(input)
  list_element.append hidden_element
  list_element.append "<button class='close email-delete'>&times;</button>"
  $("#cc-emails").append list_element

removeEmail = (e) ->
  e.preventDefault()
  $(event.target).closest("li").remove()

$ ->
  $(document).on 'click', '.add-freeresponsequestion', addQuestion
  $(document).on 'click', '.remove-freeresponsequestion', removeQuestion
  $("textarea").autosize()

  $(document).on 'click', '.add-funderconstraint', requireQuestion
  $(document).on 'click', '.remove-funderconstraint', ignoreQuestion

  $(document).on 'click', '.email-delete', removeEmail

  $("#cc-email").keypress (e) -> addEmail e if e.which == 13
  $("#add-cc-email").click addEmail
