###
#
# Selected is an array of selected funders: [ funder_id1, funder_id2, ... ]
#
###
Selected = []

###
#
# Expectations is a hash of eligibility question ids with values of
# an array of funders that require that question.
#
# Example:
# {
#   question_id1: [ funder_id1, funder_id2, funder_id3],
#   question_id2: [ funder_id2, funder_id4],
#   .
#   .
# }
#
###
Expectations = {}

###
#
# EligibleFunders is an array of funders that are still eligible:
# [ funder_id1, funder_id3, ... ]
#
###
EligibleFunders = []

# initialize expected answers to eligibility questions
initExpectations = ->
  $(".bool-q").each (index, el) ->
    question_id = $(el).data("qid")
    funder_ids = parseDataIds($(el), "required-funder-ids")
    if funder_ids.length
      Expectations[question_id] = funder_ids

# update the eligible funders
updateEligibileFunders = ->
  EligibleFunders = allFunderIds()
  $(".bool-q").each (index, el) ->
    question_id = $(el).data("qid")
    if !el.checked and question_id of Expectations
      for required_funder_id in Expectations[question_id]
        EligibleFunders = _.without(EligibleFunders, required_funder_id)

# disable ineligible funders
disableIneligibleFunders = ->
  enableAllFunders()
  ineligible_funders = _.difference(allFunderIds(), EligibleFunders)
  for funder_id in ineligible_funders
    funder = $("#funder-checkbox-#{funder_id}")
    question_ids = _.difference(parseDataIds(funder, "required-question-ids"),
                                allCheckedQuestionIds())
    question_labels =
      ("#eligibilitylabel_#{qid}" for qid in question_ids).join()
    insert_text = _.map($(question_labels), (l) -> l.innerText).join(", ")
    funder.addClass("ineligible").attr("checked", false)
      .attr("readonly", true).data("toggle", "tooltip")
      .attr("title", "#{insert_text} is required to be eligible")
  $(".funder-checkbox").tooltip()

# enable all funders
enableAllFunders = ->
  $(".funder-checkbox").removeClass("ineligible")
    .removeAttr("readonly").removeAttr("toggle").removeAttr("title")
    .removeAttr("data-original-title").tooltip('dispose')

# parse ids as an array of integers from associated data field
parseDataIds = (elem, id_name) ->
  ids = elem.data(id_name).toString().split(',').filter((id) -> id != "")
  _.map(ids, (id) -> parseInt(id, 10))

# retrieve all funder ids
allFunderIds = ->
  _.map($(".funder-checkbox"), (e) -> $(e).data("funderid"))

# retrieve all checked eligibility questions ids
allCheckedQuestionIds = ->
  _.map($("#eligibility [type='checkbox']:checked"), (e) -> $(e).data("qid"))

# show questions based on which funders are selected and eligible
showQuestions = ->
  funder_ids = _.intersection(Selected, EligibleFunders)
  funders = (".funder-q-#{fid}" for fid in funder_ids).join()
  $(".extra-answer").hide() # hide elements
  $(funders).fadeIn()
  if $(funders).length
    $("#funder-no-q").hide()
  else
    $("#funder-no-q").show()

toggleSection = (e) ->
  $(e).parent().siblings(".section-content").toggle()
  $(e).toggleClass("collapsed")

disableCheckbox = (e) ->
  e.preventDefault()

$ ->
  initExpectations()
  updateEligibileFunders()
  disableIneligibleFunders()

  $(document).on 'click', '.ineligible', disableCheckbox
  $(document).on 'click', '.disable', disableCheckbox

  $(".funder-checkbox").change ->
    funder_id = $(this).data("funderid")
    return if $(this).hasClass("ineligible")
    if !this.checked
      Selected = _.without(Selected, funder_id)
    else if this.checked and !_.contains(Selected, funder_id)
      Selected.push funder_id
    showQuestions()

  $(".bool-q").change ->
    if $(this).hasClass("disable")
      return
    updateEligibileFunders()
    disableIneligibleFunders()
    showQuestions()

  $(".funder-checkbox").each (index, el) ->
    funder_id = $(el).data("funderid")
    Selected.push(funder_id) if this.checked
  showQuestions()

  $("#id_time").timepicker(
    timeFormat: "G:i"
    step: 30
    scrollDefaultNow: true
  )

  $calendar = $("#id_date")
  $calendar.pickadate(
    format: 'mm/dd/yyyy'
    format_submit: 'mm/dd/yyyy'
    onStart: ->
      @setDate $calendar.data("year"), $calendar.data("month"), $calendar.data("day") if $calendar.data("edit")
  )

  # toggle sections
  $(".section-toggle").click -> toggleSection(this)

  $('#no-fund').click -> $('.funding-given').val 0

  # dynamic textarea elements heights to fit content.
  $("textarea").autosize()
