###
#
# Selected is a hash of funder ids with values of checked or unchecked
# true if checked, false otherwise
# Example:
# {
#   funder_id1: true,
#   funder_id2: false
#   .
#   .
# }
#
###
Selected = {}

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
    question_id = el.dataset.qid
    [y, n] = [el.dataset.recsyes.split(','), el.dataset.recsno.split(',')]
    Expectations[question_id] = addExpectation(y, n)

# Show questions based on which funders are selected
showQuestions = () ->
  funder_ids = (".funder-q-#{fid}" for fid in _.keys(Selected) when Selected[fid])
  funders = funder_ids.join()
  $(".extra-answer").hide() # hide elements wh
  $(funders).fadeIn()
  if funders.length
    $("#funder-no-q").hide()
  else
    $("#funder-no-q").show()

# show labels on the funders who are recommended
showRecommendations = () ->
  $(".funder-check .checkbox .label-important").remove()
  label = $("#recommended-label").html()
  funders = getRecommended(Reality)
  $(".funder-check input[data-funderid=#{f}]").parent().append(label) for f in funders

# update the recommended funders
updateRecommendations = (el) ->
  question_id = el.dataset.qid
  funder_relations = Expectations[question_id]
  Reality[question_id] = checkExpectations(el.checked, funder_relations)

$ ->
  initExpectations()

  $(".funder-checkbox").change () ->
    Selected[this.dataset.funderid] = this.checked
    showQuestions()

  $(".bool-q").change () ->
    updateRecommendations(this)
    showRecommendations()

  $(".funder-checkbox").each () -> Selected[this.dataset.funderid] = this.checked
  showQuestions()

  $(".bool-q").each () -> updateRecommendations(this)
  showRecommendations()
