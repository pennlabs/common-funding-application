root = exports ? this

# add expected results for a particular question
root.addExpectation = (recsyes, recsno) ->
  funders = {}
  funders[fid] = true for fid in recsyes when fid.length
  funders[fid] = false for fid in recsno when fid.length
  funders

# check if expectations match reality
root.checkExpectations = (is_checked, funder_relations) ->
  recs = {}
  for funder_id in _.keys(funder_relations)
    recs[funder_id] = is_checked == funder_relations[funder_id]
  recs

# get a list of recommended funders based on reality
root.getRecommended = (reality) ->
  recs = {}
  for funders in _.values(reality)
    for fid in _.keys(funders)
      # if recs is not defined, initialize it
      if not recs[fid]?
        recs[fid] = funders[fid]
      else
        recs[fid] = recs[fid] and funders[fid]
  (fid for fid in _.keys(recs) when recs[fid])
