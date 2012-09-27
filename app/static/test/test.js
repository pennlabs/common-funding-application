var assert = require("assert"),
    recs = require("../js/recs")
    _ = require("../js/underscore")

describe('Recommendations', function(){
  describe("#addExpectation()", function() {
    it("should be empty object", function() {
      assert.ok( _.isEmpty( recs.addExpectation([], []) ) );
    })
  })
  describe("#getRecommended()", function() {
    it("should be empty array", function() {
      assert.ok( _.isEmpty( recs.getRecommended({}) ) );
    })
  })
  describe("#checkExpectations()", function() {
    it("should be empty object", function() {
      assert.ok( _.isEmpty( recs.checkExpectations(null, {}) ) );
    })
  })
  describe("#addExpectation()", function() {
    it("should add positive expectation", function() {
      var E = {};
      var y = ["1"];
      E = recs.addExpectation(y, []);
      var expected = {1: true};
      assert.ok( _.isEqual(E, expected) );
    })
  })
  describe("#addExpectation()", function() {
    it("should add two expectations", function() {
      var E = {};
      var y = ["1"];
      var n = ["2"];
      E = recs.addExpectation(y, n);
      var expected = {1: true, 2: false};
      assert.ok( _.isEqual(E, expected) );
    })
  })
})
