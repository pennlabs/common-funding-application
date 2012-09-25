Questions = {}
Funders = {}
Selected = {}

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
  fs =  getFunders(Funders)
  for f in fs
    $(".funder-check input[data-funderid="+f+"]").parent().append(label)

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
