###
# 
# q1: {
#   bob: true,
#   tom: false
# }
#
###
window.addQuestion = (recsyes, recsno) ->
  funders = {}
  funders[fid] = true for fid in recsyes when fid.length
  funders[fid] = false for fid in recsno when fid.length
  funders

window.getRecommendedFunders = (is_checked, question) ->
  recs = {}
  for funder in _.keys(question)
    recs[funder] = is_checked == question[funder]
  recs
