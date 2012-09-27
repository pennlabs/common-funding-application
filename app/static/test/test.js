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
      var y = ["1"];
      var n = ["2"];
      var E = recs.addExpectation(y, n);
      var expected = {1: true, 2: false};
      assert.ok( _.isEqual(E, expected) );
    })
  })
  describe("#checkRelations()", function() {
    it("should remain the same", function() {
      var y = ["1"];
      var E = recs.addExpectation(y, []);
      var expected = {1: true};
      assert.ok( _.isEqual(E, expected) );

      var is_checked = true;
      var reality = {1: true};
      assert.ok( _.isEqual(recs.checkExpectations(is_checked, E), reality ) );
    })
  })
  describe("#checkRelations()", function() {
    it("should differ from reality", function() {
      var y = ["1"];
      var E = recs.addExpectation(y, []);
      var expected = {1: true};
      assert.ok( _.isEqual(E, expected) );

      var is_checked = false;
      var reality = {1: false};
      assert.ok( _.isEqual(recs.checkExpectations(is_checked, E), reality ) );
    })
  })
})
