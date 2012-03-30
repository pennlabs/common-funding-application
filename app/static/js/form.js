var totalFunders = 3;
var selectedFunders;

function showFunderQuestions() {
  var selectHide = "";
  var selectShow = "";
  for (var i=0; i<totalFunders; i++) {
    if (selectedFunders[i])
      selectShow += ".funder-q-"+i+",";
    else
      selectHide += ".funder-q-"+i+",";
  }
  $(selectShow).show();
  $(selectHide).hide();
}

$(document).ready(function() {
  
  selectedFunders = new Array(totalFunders);
  
  $(".funder-check input").change(function () {
    selectedFunders[ $(this).attr("class").substring(16) ] = $(this).attr("checked") == "checked";
    showFunderQuestions();
  });

});