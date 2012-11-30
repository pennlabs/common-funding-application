# Registration email validator
$ ->
  $("label[for=id_email]").html("Penn Email Address:")

  $("#register-form").on "submit", (e) ->
    email = $("#id_email").val()
    pattern = /@.*upenn\.edu$/
    if !pattern.test(email)
      $("#id_email").addClass("email-error")
      e.preventDefault()
    
  $("#id_email").on "keyup", ->
    $(this).removeClass("email-error")
