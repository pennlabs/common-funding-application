$(() =>
  $('.form-actions .btn-primary').click(function(e) {
    const failed = check_form_inputs();
    // if there are any failed input fields, then prevent default and scroll to it
    if (failed) {
      e.preventDefault();
      $('html, body').animate({scrollTop: $(failed).offset().top}, 500);
      return;
    }
  })
);


/*
 * Check that all form inputs are valid.
 * returns the input that is not valid to be scrolled to, else returns undefined
 */
var check_form_inputs = function() {
  // inputs that are allowed to be empty.
  const nullable_inputs = ["advisoremail", "advisorphone"];

  // always scroll to the first failed item
  let first_failed = undefined;

  // iterate over all inputs that are not checkboxes and are not dollar-amount
  // update the first_failed if it is undefined, otherwise just add the error class
  _.each($('input:not([type~=checkbox]):not(.input-with-dollar)'), function(item) {
    // check if parent is not part of the item table (css can't select parents)
    let needle;
    if (!nullable_inputs.includes($(item).attr('name'))) {
      if (!$(item).val() && ($(item).parent().prop('tagName') !== 'TD') &&
          ($(item).parent().prop('tagName') !== 'TR')) {
        const failed_item = $(item).closest('.control-group').addClass('error');
        first_failed = first_failed || failed_item;
      } else {
        $(item).closest('.control-group').removeClass('error');
      }
    }
  });

  // using free-response-error because built in error for bootstrap doesn't affect textareas!
  // iterate over all short answer textareas that are visible
  _.each($('.short-answer .section-content textarea:visible'), function(item) {
    if (!$(item).val()) {
      const failed_item = $(item).addClass('free-response-error');
      first_failed = first_failed || failed_item;
    } else {
      $(item).removeClass('free-response-error');
    }
  });

  _.each($('.itemrow input[type=number]'), function(item) {
    const siblingNodes = item.parentNode.parentNode.children;
    const classList = siblingNodes[siblingNodes.length-1].children[0].classList;
    if (!$(item).val() && classList.contains('remove-item')) {
      const failed_item = $(item).addClass('form-control-error');
      $(item).closest('.itemrow').addClass('error');
      first_failed = first_failed || failed_item;
    }
  });

  return first_failed;
};

