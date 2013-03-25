$ ->
  $('.form-actions .btn-primary').click (e) ->
    failed = check_form_inputs()
    if failed
      e.preventDefault()
      $('html, body').animate scrollTop: $(failed).offset().top, 500
      return


check_form_inputs = ->
  # always scroll to the first failed item
  first_failed = undefined
  # using free-response-error because built in error for bootstrap doesn't affect textareas!
  _.each $('input:not([type~=checkbox]):not(.input-with-dollar)'), (item) ->
    if not $(item).val() and $(item).parent().prop('tagName') != 'TD' and $(item).parent().prop('tagName') != 'TR'
      failed_item = $(item).closest('.control-group').addClass 'error'
      first_failed = first_failed || failed_item
    else
      $(item).closest('.control-group').removeClass 'error'

  _.each $('.short-answer .section-content textarea:visible'), (item) ->
    if not $(item).val()
      failed_item = $(item).addClass 'free-response-error'
      first_failed = first_failed || failed_item
    else
      $(item).removeClass 'free-response-error'
  return first_failed

