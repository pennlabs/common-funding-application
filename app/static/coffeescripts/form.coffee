###
#
# Selected is an array of selected funders: [ funder_id1, funder_id2, ... ]
#
###
Selected = []

###
#
# Expectations is a hash of question ids with values of 
# an object* that contains which funders want a check
# and which do not. This object* will be referred to as
# funder_relations
#
# true if funder wants a check on this question
# false if funder does NOT want a check on this question
# otherwise funder is not included in object
# Example:
# {
#   question_id1: {
#     funder_id1: true,
#     funder_id2: false,
#     funder_id3: false
#   },
#   question_id2: {
#     funder_id1: true
#   }
#   .
#   .
# }
#
###
Expectations = {}

###
#
# Reality is a hash of question ids with values of
# an object that contains which funder questions have
# satisfied the expectations.
# It is essentially the same object as Expectations but checks each
# expected answer with the checkboxes on the physical DOM
#
###
Reality = {}

# initialize expected answers to questions
initExpectations = () ->
  $(".bool-q").each (index, el) ->
    question_id = $(el).data("qid")
    expectations = (type) -> $(el).data(type).toString().split(',')
    [y, n] = [expectations("recsyes"), expectations("recsno")]
    Expectations[question_id] = addExpectation(y, n)

# Show questions based on which funders are selected
showQuestions = () ->
  funder_ids = (".funder-q-#{fid}" for fid in Selected)
  funders = funder_ids.join()
  $(".extra-answer").hide() # hide elements
  $(funders).fadeIn()
  if funders.length
    $("#funder-no-q").hide()
  else
    $("#funder-no-q").show()

# show labels on the funders who are recommended
showRecommendations = () ->
  $(".funder-check .checkbox .recommended-label").remove()
  label = $("#recommended-label").html()
  funders = getRecommended(Reality)
  $(".funder-check input[data-funderid=#{f}]").parent().append(label) for f in funders

# update the recommended funders
updateRecommendations = (el) ->
  question_id = $(el).data("qid")
  funder_relations = Expectations[question_id]
  Reality[question_id] = checkExpectations(el.checked, funder_relations)

$ ->
  initExpectations()

  $(".funder-checkbox").change () ->
    funder_id = $(this).data("funderid")
    if !this.checked
      Selected = _.without(Selected, funder_id)
    else if this.checked and !_.contains(Selected, funder_id)
      Selected.push funder_id
    showQuestions()

  $(".bool-q").change () ->
    updateRecommendations(this)
    showRecommendations()

  $(".funder-checkbox").each (index, el) ->
    funder_id = $(el).data("funderid")
    Selected.push(funder_id) if this.checked
  showQuestions()

  $(".bool-q").each (index, el) -> updateRecommendations(el)
  showRecommendations()
	
	$("#questiontime").timepicker({		
		timeFormat: "G:i"
		step: 30
		scrollDefaultNow: true		
	})
