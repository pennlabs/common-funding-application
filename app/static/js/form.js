/*
 * Selected is an array of selected funders: [ funder_id1, funder_id2, ... ]
 */
let Selected = [];

/*
 *
 * Expectations is a hash of eligibility question ids with values of
 * an array of funders that require that question.
 *
 * Example:
 * {
 *   question_id1: [ funder_id1, funder_id2, funder_id3],
 *   question_id2: [ funder_id2, funder_id4],
 *   .
 *   .
 * }
 *
 */
const Expectations = {};

/*
 *
 * EligibleFunders is an array of funders that are still eligible:
 * [ funder_id1, funder_id3, ... ]
 *
 */
let EligibleFunders = [];

// initialize expected answers to eligibility questions
const initExpectations = () =>
  $(".bool-q").each(function(index, el) {
    const question_id = $(el).data("qid");
    const funder_ids = parseDataIds($(el), "required-funder-ids");
    if (funder_ids.length) {
      Expectations[question_id] = funder_ids;
    }
  })
;

// update the eligible funders
const updateEligibileFunders = function() {
  EligibleFunders = allFunderIds();
  $(".bool-q").each(function(index, el) {
    const question_id = $(el).data("qid");
    if (!el.checked && question_id in Expectations) {
      Expectations[question_id].map((required_funder_id) =>
        (EligibleFunders = _.without(EligibleFunders, required_funder_id)));
    }
  });
};

// disable ineligible funders
const disableIneligibleFunders = function() {
  enableAllFunders();
  const ineligible_funders = _.difference(allFunderIds(), EligibleFunders);
  for (let funder_id of ineligible_funders) {
    const funder = $(`#funder-checkbox-${funder_id}`);
    const question_ids = _.difference(parseDataIds(funder, "required-question-ids"),
                                      allCheckedQuestionIds());
    const question_labels = (question_ids.map((qid) => `#eligibilitylabel_${qid}`)).join();
    const insert_text = _.map($(question_labels), l => l.innerText).join(", ");
    funder.addClass("ineligible").attr("checked", false)
      .attr("readonly", true).data("toggle", "tooltip")
      .attr("title", `${insert_text} is required to be eligible`);
  }
  $(".funder-checkbox").tooltip();
};

// enable all funders
var enableAllFunders = () =>
  $(".funder-checkbox").removeClass("ineligible")
    .removeAttr("readonly").removeAttr("toggle").removeAttr("title")
    .removeAttr("data-original-title").tooltip('dispose')
;

// parse ids as an array of integers from associated data field
var parseDataIds = function(elem, id_name) {
  const ids = elem.data(id_name).toString().split(',').filter(id => id !== "");
  return _.map(ids, id => parseInt(id, 10));
};

// retrieve all funder ids
var allFunderIds = () => _.map($(".funder-checkbox"), e => $(e).data("funderid"));

// retrieve all checked eligibility questions ids
var allCheckedQuestionIds = () => _.map($("#eligibility [type='checkbox']:checked"), e => $(e).data("qid"));

// show questions based on which funders are selected and eligible
const showQuestions = function() {
  const funder_ids = _.intersection(Selected, EligibleFunders);
  const funders = (funder_ids.map((fid) => `.funder-q-${fid}`)).join();
  $(".extra-answer").hide(); // hide elements
  $(funders).fadeIn();
  if ($(funders).length) {
    $("#funder-no-q").hide();
  } else {
    $("#funder-no-q").show();
  }
};

const toggleSection = function(e) {
  $(e).parent().siblings(".section-content").toggle();
  $(e).toggleClass("collapsed");
};

const disableCheckbox = e => e.preventDefault();

$(function() {
  initExpectations();
  updateEligibileFunders();
  disableIneligibleFunders();

  $(document).on('click', '.ineligible', disableCheckbox);
  $(document).on('click', '.disable', disableCheckbox);

  $(".funder-checkbox").change(function() {
    const funder_id = $(this).data("funderid");
    if ($(this).hasClass("ineligible")) {
      return;
    }
    if (!this.checked) {
      Selected = _.without(Selected, funder_id);
    } else if (this.checked && !_.contains(Selected, funder_id)) {
      Selected.push(funder_id);
    }
    showQuestions();
  });

  $(".bool-q").change(function() {
    if ($(this).hasClass("disable")) {
      return;
    }
    updateEligibileFunders();
    disableIneligibleFunders();
    showQuestions();
  });

  $(".funder-checkbox").each(function(index, el) {
    const funder_id = $(el).data("funderid");
    if (this.checked) {
      Selected.push(funder_id);
    }
  });
  showQuestions();

  $("#id_time").timepicker({
    timeFormat: "G:i",
    step: 30,
    scrollDefaultNow: true
  });

  const $calendar = $("#id_date");
  $calendar.pickadate({
    format: 'mm/dd/yyyy',
    format_submit: 'mm/dd/yyyy',
    onStart() {
      if ($calendar.val()) {
        this.set('select', $calendar.val(), {format: 'yyyy-mm-dd'});
      }
    }
  });

  // toggle sections
  $(".section-toggle").click(function() {
    toggleSection(this);
  });

  $('#no-fund').click(() => $('.funding-given').val(0));

  // dynamic textarea elements heights to fit content.
  $("textarea").autosize();
});
