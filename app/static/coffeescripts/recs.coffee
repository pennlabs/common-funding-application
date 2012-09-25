initStore = () {
  $(".bool-q").each (index, el) ->
    [y, n] = [el.dataset.recsyes.split(','), el.dataset.recsno.split(',')]
    Store[el.dataset.qid] = addQuestion(y, n)
}

getFunderQuestions = (funders) -> (fid for fid in funders when fid)

###
# 
# q1: {
#   bob: true,
#   tom: false
# }
#
###
addQuestion = (recsyes, recsno) {
  funders = {}
  funders.fid = true for fid in recsyes
  funders.fid = false for fid in recsno
  funders
}

checkRecommendedFunders = (is_checked, question) ->
  rec = {}
  for funder in _.keys(question)
    rec[funder] = is_checked == question.funder
  rec

showRecommendedFunders = () ->
  label = '<span class="label label-important">Recommended</span>'
  $(".funder-check .checkbox .label-important").remove()
  for funder in _.keys(recommendedFunders)
    if recommendedFunders[funder]
      $(".funder-check input[data-funderid=#{funder}").parent().append(label)
