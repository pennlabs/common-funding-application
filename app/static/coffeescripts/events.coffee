toggleEventRow = (e) ->
  $(e).children(".funders").toggle()

$ ->
  $(".app-item-row").on "click", () ->
    $(this).children().first().children(".funders").slideToggle(200)

  $(".app-item-row .btn").on "click", (e) -> e.stopPropagation()
