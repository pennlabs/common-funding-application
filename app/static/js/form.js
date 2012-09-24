var selectedFunders;
var recommendedFunders;
var qStorage;

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

  
  //console.log(selectedFunders.length);
  
  if ($(selectShow).length)
    $("p#funder-no-q").hide();
  else
    $("p#funder-no-q").show();
}

function checkRecommendedFunders(elem) {
  var currVal = elem.checked;
  var qid = elem.dataset.qid;
  var funders = qStorage[qid].funders;
  var expected = qStorage[qid].expected;
  
  for (var i in funders) {
    // check if valid funder id
    if (recommendedFunders[funders[i]])
      recommendedFunders[funders[i]][qid] = expected[i]==currVal;
    //console.log("funder"+funders[i]+",qid"+qid+" : "+"expected-"+expected[i]+" got-"+currVal+" = "+(expected[i]==currVal));
  }
  
  showRecommendedFunders();
}

function showRecommendedFunders() {
  var label = '<span class="label label-important">Recommended</span>';
  $(".funder-check .checkbox .label-important").remove();
  
  for (var i in recommendedFunders) {
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
    var totalFunders = $(".funder-check input").length
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
    var fids = new Array();
    $(".funder-checkbox").each(function(){
      fids.push(this.dataset.funderid);
    });
    
    // collect question ids
    var qids = new Array();
    $(".bool-q").each(function(){
      qids.push(this.dataset.qid);
    });
    
    // init recommendedFunders 2D ("associated") array
    // init them to all true, "true" for indifferent
    recommendedFunders = {};
    for (var i in fids) {
      recommendedFunders[fids[i]] = {};
      for (var j in qids) {
        recommendedFunders[fids[i]][qids[j]] = true;
      }
    }    
    
    // build questions storage, for quick lookup for question onClick
    // for each question, stores list of funders that cares, and list of expected values
    qStorage = {};
    for (var i in qids)
      qStorage[qids[i]] = { funders:[], expected:[] };
    
    $(".funder-checkbox").each(function(){
      var funderid = this.dataset.funderid;
      var yesIds = this.dataset.recsyes;
      if (!!yesIds) {
        yesIds = yesIds.split(",");
        for (var i in yesIds) {
          qStorage[yesIds[i]].funders.push(funderid);
          qStorage[yesIds[i]].expected.push(true);
        }
      }
      var noIds = this.dataset.recsno;
      if (!!noIds) {
        noIds = noIds.split(",");
        for (var i in noIds) {
          qStorage[noIds[i]].funders.push(funderid);
          qStorage[noIds[i]].expected.push(false);
        }
      }
    });
    
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
