var assert = require("assert"),
    recs = require("../js/recs")
    _ = require("../js/underscore")

describe('Recommendations', function(){
  describe("#addExpectation()", function() {
    it("should be empty object", function() {
      assert.ok( _.isEmpty( recs.addExpectation([], []) ) );
    })
  })
})
