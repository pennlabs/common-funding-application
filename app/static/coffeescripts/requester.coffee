$ ->
  $('.form-actions .btn-primary').click (e) ->
    failed = check_form_inputs()
    # if there are any failed input fields, then prevent default and scroll to it
    if failed
      e.preventDefault()
      $('html, body').animate scrollTop: $(failed).offset().top, 500
      return


###
# Check that all form inputs are valid.
# returns the input that is not valid to be scrolled to, else returns undefined
###
check_form_inputs = ->
  # inputs that are allowed to be empty.
  nullable_inputs = ["advisoremail", "advisorphone"]

  # always scroll to the first failed item
  first_failed = undefined

  # iterate over all inputs that are not checkboxes and are not dollar-amount
  # update the first_failed if it is undefined, otherwise just add the error class
  _.each $('input:not([type~=checkbox]):not(.input-with-dollar)'), (item) ->
    # check if parent is not part of the item table (css can't select parents)
    if $(item).attr('name') not in nullable_inputs
      if not $(item).val() and $(item).parent().prop('tagName') != 'TD' and
          $(item).parent().prop('tagName') != 'TR'
        failed_item = $(item).closest('.control-group').addClass 'error'
        first_failed = first_failed || failed_item
      else
        $(item).closest('.control-group').removeClass 'error'

  # using free-response-error because built in error for bootstrap doesn't affect textareas!
  # iterate over all short answer textareas that are visible
  _.each $('.short-answer .section-content textarea:visible'), (item) ->
    if not $(item).val()
      failed_item = $(item).addClass 'free-response-error'
      first_failed = first_failed || failed_item
    else
      $(item).removeClass 'free-response-error'

  _.each $('.itemrow input[type=number]'), (item) ->
    siblingNodes = item.parentNode.parentNode.children
    classList = siblingNodes[siblingNodes.length-1].children[0].classList
    if not $(item).val() and 'remove-item' in classList
      failed_item = $(item).addClass 'form-control-error'
      $(item).closest('.itemrow').addClass 'error'
      first_failed = first_failed || failed_item

  return first_failed

