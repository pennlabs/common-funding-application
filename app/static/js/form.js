var totalFunders;
var selectedFunders;

function showFunderQuestions() {
  var selectHide = "";
  var selectShow = "";
  for (var i=0; i<totalFunders; i++) {
    if (selectedFunders[i])
      selectShow += ".funder-q-"+i+", ";
  }
  $(".funder-q").hide();
  $(selectShow).show();
  
  if ($(selectShow).length)
    $("p#funder-no-q").hide();
  else
    $("p#funder-no-q").show();
}

$(document).ready(function() {
  totalFunders = $(".funder-check input").length
  selectedFunders = new Array(totalFunders);
    
  // register funder checkbox click
  $(".funder-check input").change(function () {
    selectedFunders[ $(this).attr("class").substring(16) ] = $(this).attr("checked") == "checked";
    showFunderQuestions();
  });
  
  // count already checked checkboxes
  $(".funder-check input").each(function () {
    selectedFunders[ $(this).attr("class").substring(16) ] = $(this).attr("checked") == "checked";
  });
  showFunderQuestions();

});