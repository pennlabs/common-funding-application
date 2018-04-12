const addQuestion = function(e) {
  e.preventDefault();
  const row = $(event.target).closest('tr');
  if (!row.find("textarea").val()) {
    return;
  }
  const clone = row.clone().insertAfter(row);
  row.find("textarea").attr("name", "freeresponsequestion");
  clone.find("textarea").val("");
  $(event.target)
    .attr("class", "btn btn-danger remove-freeresponsequestion")
    .html("Remove");
};

const removeQuestion = function(e) {
  e.preventDefault();
  $(event.target).closest('tr').remove();
};

const requireQuestion = function(e) {
  e.preventDefault();
  const button = $(event.target);
  button.siblings("input").val(button.data("qid"));
  button
    .attr("class", "btn btn-danger remove-funderconstraint")
    .html("Required");
};

const ignoreQuestion = function(e) {
  e.preventDefault();
  const button = $(event.target);
  button.siblings("input").val("");
  button
    .attr("class", "btn add-funderconstraint")
    .html("Not Required");
};

const addEmail = function(e) {
  e.preventDefault();
  const input = $("#cc-email").val();
  $("#cc-email").val("");
  if (!input) {
    return;
  }
  if ($('input[name="cc_email"]').filter(function() { return this.value === input; }).length) { return; }
  const hidden_element = $("<input type='hidden' name='cc_email' />").val(input);
  const list_element = $("<li class='list-group-item' />").text(input);
  list_element.append(hidden_element);
  list_element.append("<button class='close email-delete'>&times;</button>");
  $("#cc-emails").append(list_element);
};

const removeEmail = function(e) {
  e.preventDefault();
  $(event.target).closest("li").remove();
};

$(function() {
  $(document).on('click', '.add-freeresponsequestion', addQuestion);
  $(document).on('click', '.remove-freeresponsequestion', removeQuestion);
  $("textarea").autosize();

  $(document).on('click', '.add-funderconstraint', requireQuestion);
  $(document).on('click', '.remove-funderconstraint', ignoreQuestion);

  $(document).on('click', '.email-delete', removeEmail);

  $("#cc-email").keypress(function(e) {
    if (e.which === 13) {
      return addEmail(e);
    }
  });
  $("#add-cc-email").click(addEmail);
});
