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

window.getFunders = (AllFunders) ->
  recs = {}
  for funders in _.values(AllFunders)
    for fid in _.keys(funders)
      if recs[fid] is undefined
        recs[fid] = funders[fid]
      else
        recs[fid] = recs[fid] and funders[fid]
  console.log recs
  (fid for fid in _.keys(recs) when recs[fid])
