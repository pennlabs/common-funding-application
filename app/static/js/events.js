$(function() {
  $(".event-row").on("click", function() {
    $(this).children().first().children(".funders").slideToggle(200);
  });

  $(".event-row .btn").on("click", e => e.stopPropagation());

  $('.alert [data-dismiss="alert"]').on('click', function(e) {
    $(this).parent().remove();
  });

  return $(".destroy-event").on("click", function(e) {
    e.preventDefault();
    if (!confirm("Are you sure you want to delete this application?")) { return; }
    const $target = $(this);
    $target.addClass("disabled");
    $.ajax({
      type: 'GET',
      url: $target.attr("href"),
      success(data) {
        $target.closest(".event-row").remove();
      },
      error() {
        $target.removeClass("disabled");
      }
    });
    return false;
  });
});
