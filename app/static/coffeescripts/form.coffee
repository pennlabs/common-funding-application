window.Questions = {}
window.Funders = {}
window.Selected = {}

initStore = () ->
  $(".bool-q").each (index, el) ->
    [y, n] = [el.dataset.recsyes.split(','), el.dataset.recsno.split(',')]
    Questions[el.dataset.qid] = addQuestion(y, n)

showFunderQuestions = () ->
  funder_ids = (".funder-q-#{fid}" for fid in _.keys(Selected) when Selected[fid])
  funders = funder_ids.join()
  $("[class^=funder-q]").hide()
  $(funders).fadeIn()
  if funders.length
    $("p#funder-no-q").hide()
  else
    $("p#funder-no-q").show()

showRecommendedFunders = () ->
  label = '<span class="label label-important">Recommended</span>'
  $(".funder-check .checkbox .label-important").remove()

  recs = {}

  for funders in _.values(Funders)
    for fid in _.keys(funders)
      if recs[fid] is undefined
        recs[fid] = funders[fid]
      else
        recs[fid] = recs[fid] and funders[fid]
  console.log recs
  for fid in _.keys(recs)
    $(".funder-check input[data-funderid="+fid+"]").parent().append(label) if recs[fid]

checkRecommendedFunders = (el) ->
  qid = el.dataset.qid
  question = Questions[qid]
  Funders[qid] = getRecommendedFunders(el.checked, question)

$ ->
  initStore()

  $(".funder-check input").change () ->
    Selected[this.dataset.funderid] = this.checked
    showFunderQuestions()

  $(".bool-q").change () ->
    checkRecommendedFunders(this)
    showRecommendedFunders()

  $(".funder-check input").each () -> Selected[this.dataset.funderid] = this.checked
  showFunderQuestions()

  $(".bool-q").each () -> checkRecommendedFunders(this)
  showRecommendedFunders()
