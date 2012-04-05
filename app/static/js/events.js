function toggleEventRow(e) {
  $("e").children(".funders").toggle()
}


$(document).ready(function() {
  
  $(".app-item-row").click(function() {
    $(this).children().first().children(".funders").slideToggle(200);
  });
  
});