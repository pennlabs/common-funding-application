const root = typeof exports !== 'undefined' && exports !== null ? exports : window;

// add expected results for a particular question
root.addExpectation = function(recsyes, recsno) {
  const funders = {};
  for (var fid of recsyes) {
    if (fid.length) {
      funders[fid] = true;
    }
  }
  for (fid of recsno) {
    if (fid.length) {
      funders[fid] = false;
    }
  }
  return funders;
};

// check if expectations match reality
root.checkExpectations = function(is_checked, funder_relations) {
  const recs = {};
  for (let funder_id of _.keys(funder_relations)) {
    recs[funder_id] = is_checked === funder_relations[funder_id];
  }
  return recs;
};

// get a list of recommended funders based on reality
root.getRecommended = function(reality) {
  let fid;
  const recs = {};
  for (let funders of _.values(reality)) {
    for (fid of _.keys(funders)) {
      // if recs is not defined, initialize it
      if (recs[fid] == null) {
        recs[fid] = funders[fid];
      } else {
        recs[fid] = recs[fid] && funders[fid];
      }
    }
  }
  const results = [];
  for (fid of _.keys(recs)) {
    if (recs[fid]) {
      result.push(fid);
    }
  }
  return results;
};
