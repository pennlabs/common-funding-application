function toggleEventRow(e) {
  $("e").children(".funders").toggle()
}


$(document).ready(function() {
  
  $(".app-item-row").on("click", function() {
    $(this).children().first().children(".funders").slideToggle(200);
  });

  $(".app-item-row .btn").on("click", function(e) {
    e.stopPropagation();
  });
  
});
