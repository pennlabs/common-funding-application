$ ->
  $(".event-row").on "click", ->
    $(this).children().first().children(".funders").slideToggle(200)

  $(".event-row .btn").on "click", (e) -> e.stopPropagation()

  $(".destroy-event").on "click", (e) ->
    e.preventDefault()
    $target = $(e.target)
    $target.addClass("disabled")
    $.ajax(
      type: 'GET'
      url: $target.attr("href")
      success: (data) ->
        $target.closest(".event-row").remove()
      error: ->
        $target.removeClass("disabled")
    )
    return false
