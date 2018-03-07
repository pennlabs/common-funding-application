from app.templatetags.helpers import funder_item_data, get_or_none
from app.models import (CATEGORIES, FreeResponseAnswer, FreeResponseQuestion, EligibilityAnswer, EligibilityQuestion,
                        CommonFreeResponseAnswer, CommonFreeResponseQuestion, CFAUser, CommonFollowupAnswer,
                        CommonFollowupQuestion, FollowupAnswer, FollowupQuestion)
from collections import namedtuple

from django import template
from django.template.loader import render_to_string

register = template.Library()

# question-answer pair
QA = namedtuple('QA', 'question answer')


@register.simple_tag
def itemlist_requester(is_revenue, items, funded):
    """ Render the table of items in the requester view """
    new_context = {'funded': funded,
                   'CATEGORIES': CATEGORIES, 'is_revenue': is_revenue}
    new_context['items'] =\
        [item for item in items if bool(item.revenue) == bool(is_revenue)]
    return render_to_string('app/templatetags/itemlist-requester.html',
                            context=new_context)


@register.simple_tag
def itemlist_funder(is_revenue, items, applied_funders, funder_id):
    """ Render the table of items in the funder view """
    items_data = []
    title_row = \
        ['Name', 'Category', 'Quantity', 'Price Per Unit', 'Total Amount']
    if not bool(is_revenue):
        title_row.append('Total Received')
        for funder in applied_funders:
            title_row.append(str(funder))

    for item in items:
        # only add certain items to items_data array
        if item.revenue == bool(is_revenue):
            if item.revenue:
                # applied_funders = []
                items_data.append(funder_item_data(item, []))
            else:
                items_data.append(funder_item_data(item, applied_funders))
    new_context = {'is_revenue': is_revenue,
                   'titles': title_row,
                   'current_funder': funder_id,
                   'items_data': items_data}
    return render_to_string('app/templatetags/itemlist-funder.html', context=new_context)


@register.simple_tag
def application(user, event, form):
    event = event or None

    new_context = {
        'user': user,
        'event': event,
        'form': form,
        'funder_qas': [QA(question, get_or_none(FreeResponseAnswer,
                                                question=question,
                                                event=event))
                       for question in FreeResponseQuestion.objects.all()],
        'eligibility_qas': [QA(question, get_or_none(EligibilityAnswer,
                                                     question=question,
                                                     event=event))
                            for question in EligibilityQuestion.objects.all()],
        'commonfreeresponse_qas':
        [QA(question, get_or_none(CommonFreeResponseAnswer,
                                  question=question,
                                  event=event))
         for question in CommonFreeResponseQuestion.objects.all()],
        'funders': CFAUser.objects.filter(user_type='F')
    }

    if event is None:
        return render_to_string('app/templatetags/application.html', context=new_context)

    if event.followup_needed or event.over:
        new_context['event_over_disable'] = 'readonly'
        new_context['commonfollowup_qas'] = [
            QA(question, get_or_none(CommonFollowupAnswer,
                                     question=question,
                                     event=event))
            for question in CommonFollowupQuestion.objects.all()
        ]
        new_context['followup_qas'] = [
            QA(question, get_or_none(FollowupAnswer,
                                     question=question,
                                     event=event))
            for question in
            FollowupQuestion.objects.filter(funder__event_applied_funders=event)]

    try:
        is_funder = user.profile.is_funder
        if not user or not user.is_authenticated or user.is_staff or is_funder or event.over:
            new_context['extra_attrs'] = 'readonly'
            new_context['readonly'] = True
    except AttributeError:
        new_context['extra_attrs'] = 'readonly'
        new_context['readonly'] = True

    return render_to_string('app/templatetags/application.html', context=new_context)


@register.simple_tag(takes_context=True)
def event_details(context):
    new_context = {"event": context["event"], "form": context["form"]}
    if 'readonly' in context or not context["form"]:
        if 'readonly' in context:
            new_context["extra_attrs"] = "disabled='disabled'"
        return render_to_string('app/templatetags/event-details-show.html', new_context)
    else:
        return render_to_string('app/templatetags/event-details-form.html', new_context)
