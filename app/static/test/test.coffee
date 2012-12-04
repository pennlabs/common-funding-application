`_ = require("../js/lib/underscore.min")`

assert = require "assert"
recs = require "../js/recs"

describe "Recommendations", ->
  describe "#addExpectation()", ->
    it "should be empty object", ->
      assert.ok _.isEmpty(recs.addExpectation([], []))

  describe "#getRecommended()", ->
    it "should be empty array", ->
      assert.equal recs.getRecommended({}).length, 0

  describe "#checkExpectations()", ->
    it "should be empty object", ->
      assert.ok _.isEmpty(recs.checkExpectations(null, {}))

  describe "#addExpectation()", ->
    it "should add positive expectation", ->
      E = {}
      E = recs.addExpectation(["1"], [])
      # E should be {1: true}
      assert.ok E[1]

  describe "#addExpectation()", ->
    it "should add two expectations", ->
      E = recs.addExpectation(["1"], ["2"])
      # E should be {1: true, 2: false}
      assert.ok E[1]
      assert.equal E[2], false

  describe "#checkRelations()", ->
    it "should remain the same", ->
      y = ["1"]
      E = recs.addExpectation(y, [])
      expected = 1: true
      assert.ok _.isEqual(E, expected)
      is_checked = true
      reality = 1: true
      assert.ok _.isEqual(recs.checkExpectations(is_checked, E), reality)

  describe "#checkRelations()", ->
    it "should differ from reality", ->
      y = ["1"]
      E = recs.addExpectation(y, [])
      expected = 1: true
      assert.ok _.isEqual(E, expected)
      is_checked = false
      reality = 1: false
      assert.ok _.isEqual(recs.checkExpectations(is_checked, E), reality)
