var totalFunders;
var selectedFunders;
var recommendedFunders;
var funderIds;

function checkFunderQuestions(e) {
  
}
function showFunderQuestions() {
  var selectHide = "";
  var selectShow = "";
  
  for (var i=0; i<selectedFunders.length; i++) {
    if (selectedFunders[i])
      selectShow += ".funder-q-"+i+", ";
  }
  $("[class^=funder-q]").hide();
  $(selectShow).fadeIn();

  
  console.log(selectedFunders.length);
  
  if ($(selectShow).length)
    $("p#funder-no-q").hide();
  else
    $("p#funder-no-q").show();
}

function checkRecommendedFunders(elem) {
  var currVal = String(elem.checked); // convert to string for comparison
  var qid = elem.dataset.qid;
  var funders = elem.dataset.funders.split(" ");
  var expected = elem.dataset.expected.split(" ");
  
  for (i in funders) {
    recommendedFunders[funders[i]][qid] = expected[i]==currVal;
    //console.log("funder"+i+",qid"+qid+" : "+"expected-"+expected[i]+" got-"+currVal+" = "+(expected[i]==currVal));
  }
  
  showRecommendedFunders();
}

function showRecommendedFunders() {
  var label = '<span class="label label-important">Recommended</span>';
  $(".funder-check .checkbox .label-important").remove();
  
  for (i in recommendedFunders) {
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
  (function() {
    totalFunders = $(".funder-check input").length
    selectedFunders = []
    // register funder checkbox click
    $(".funder-check input").change(function() {
      selectedFunders[ $(this)[0].dataset.funderid ] = $(this).attr("checked") == "checked";
      showFunderQuestions();
    });  
    // initial count already checked checkboxes
    $(".funder-check input").each(function() {
      console.log($(this)[0].dataset.funderid);
      selectedFunders[ $(this)[0].dataset.funderid ] = $(this).attr("checked") == "checked";
    });
    showFunderQuestions();
  })();
  
  // Init recommended funders logic
  // maintain a 2D array of funders and questions, recommendedFunders
  // show funder i if recommendedFunders[i] is all true
  // there will be unused entries
  // trade-off is simplicity of implementing 2D array
  (function() {
    // collect funder ids
    funderIds = new Array(totalFunders);
    for (var i=0; i<totalFunders; i++) {
      funderIds[i] = $(".funder-checkbox")[i].dataset.funderid;
    }
    
    // collect qids
    var qids = new Array();
    $(".bool-q").each(function(){
      qids.push(this.dataset.qid);
    });
    
    // init recommendedFunders 2D ("associated") array
    var totalFunderRecQs = $(".bool-q").length
    recommendedFunders = {};
    for (var i=0; i<totalFunders; i++) {
      recommendedFunders[funderIds[i]] = {};
      for (j in qids) {
        recommendedFunders[funderIds[i]][qids[j]] = false;
      }
    }
  })();
    
  // initial check recommend
  $(".bool-q").each(function() {
    checkRecommendedFunders(this);
  });
  // register recommend click
  $(".bool-q").change(function() {
    checkRecommendedFunders(this);
  });
  

});
