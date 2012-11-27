$ ->
  $(".app-item-row").on "click", () ->
    $(this).children().first().children(".funders").slideToggle(200)

  $(".app-item-row .btn").on "click", (e) -> e.stopPropagation()

  $(".destroy-event").on "click", (e) ->
    e.preventDefault()
    $target = $(e.target)
    $target.addClass("disabled")
    $.ajax(
      type: 'GET'
      url: $target.attr("href")
      success: (data) ->
        $target.closest(".app-item-row").remove()
      error: () ->
        $target.removeClass("disabled")
    )
    return false
