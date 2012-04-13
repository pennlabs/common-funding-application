var totalFunders;
var selectedFunders;
var totalFunderRecQs;
var recommendedFunders;

function checkFunderQuestions(e) {
  
}
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

function showRecommendedFunders() {
  var label = '<span class="label label-important">Recommended</span>';
  $(".funder-check .checkbox .label-important").remove();
  
  for (var i=0; i<totalFunders; i++) {
    var boolCheck = true;
    for (j in recommendedFunders[i]) {
      boolCheck &= recommendedFunders[i][j];
    }
    
    if (boolCheck) {
      $(".funder-check input[data-funderid="+i+"]").parent().append(label);
    }
  }
}

$(document).ready(function() {
  
  // Init funder questions showing logic
  // maintain a boolean list of selectedFunders
  // show funder i if selectedFunders[i] is true
  totalFunders = $(".funder-check input").length
  selectedFunders = new Array(totalFunders);    
  // register funder checkbox click
  $(".funder-check input").change(function() {
    selectedFunders[ $(this)[0].dataset.funderid ] = $(this).attr("checked") == "checked";
    showFunderQuestions();
  });  
  // initial count already checked checkboxes
  $(".funder-check input").each(function() {
    selectedFunders[ $(this)[0].dataset.funderid ] = $(this).attr("checked") == "checked";
  });
  showFunderQuestions();
  
  // Init recommended funders logic
  // maintain a 2D array of funders and questions, recommendedFunders
  // show funder i if recommendedFunders[i] is all true
  // there will be unused entries
  // trade-off is simplicity of implementing 2D array
  totalFunderRecQs = $(".bool-q").length
  recommendedFunders = new Array(totalFunders);
  // init question arrays to all true
  for (var i=0; i<totalFunders; i++) {
    recommendedFunders[i] = new Array(totalFunderRecQs);
    for (var j=0; j<totalFunderRecQs; j++) {
      recommendedFunders[i][j] = true;
    }
  }
  
  // recommend click
  $(".bool-q input[type=radio]").change(function() {
    var currVal = $(this).val();
    var qid = $(this).parents(".bool-q")[0].dataset.qid;
    var funders = $(this).parents(".bool-q")[0].dataset.funders.split(" ");
    var expected = $(this).parents(".bool-q")[0].dataset.expected.split(" ");
    
    for (i in funders) {
      recommendedFunders[funders[i]][qid] = expected[i]==currVal;
    }
    
    showRecommendedFunders();
  });
  // initial check recommend
  $(".bool-q").each(function() {
    var currVal = $(this).find("input[type=radio]").val();
    var qid = this.dataset.qid;
    var funders = this.dataset.funders.split(" ");
    var expected = this.dataset.expected.split(" ");
    
    for (i in funders) {
      recommendedFunders[funders[i]][qid] = expected[i]==currVal;
    }
    
    showRecommendedFunders();
  });
  

});