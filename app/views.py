from decimal import Decimal
import datetime
from datetime import timedelta
import json
import re

import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import transaction, IntegrityError
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import (Event, Grant, Comment, User, FreeResponseQuestion,
                     EligibilityQuestion, Item, CATEGORIES, CommonFollowupQuestion,
                     FollowupQuestion, CommonFreeResponseQuestion, CFAUser)
from .forms import EventForm

from django.utils import timezone

EVENTS_HOME = 'events'


def authorization_required(view):
    """Ensure only a permitted user can access an event.
    A user is permitted if:
      * They requested the event
      * They are a funder
      * They have a secret key to an event
    """
    def protected_view(request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        try:
            key = request.GET['key']
        except KeyError:
            try:
                user = request.user.profile
            except AttributeError:
                return redirect(EVENTS_HOME)
            else:
                if request.user.is_staff or user.is_funder or\
                        user.requested(event):
                    return view(request, event_id, *args, **kwargs)
                else:
                    return redirect(EVENTS_HOME)
        else:
            if key == event.secret_key:
                return view(request, event_id, *args, **kwargs)
            else:
                return redirect(EVENTS_HOME)
    return protected_view


def requester_only(view):
    """Ensure only the user who requested the event can access a page."""
    def protected_view(request, event_id, *args, **kwargs):
        user = request.user.profile
        event = Event.objects.get(pk=event_id)
        if user.is_requester and user.requested(event):
            return view(request, event_id, *args, **kwargs)
        else:
            return redirect(EVENTS_HOME)
    return protected_view


def save_from_form(event, POST):
    """Save an event from form data."""
    # save items
    names = POST.getlist('item_name')
    quantities = POST.getlist('item_quantity')
    prices_per_unit = POST.getlist('item_price_per_unit')
    funding_already_received =\
        POST.getlist('item_funding_already_received')
    categories = POST.getlist('item_category')
    revenues = POST.getlist('item_revenue')

    for item in event.item_set.all():
        if not Grant.objects.filter(item=item):
            item.delete()

    zipped_items = zip(names, quantities, prices_per_unit,
                       funding_already_received, categories, revenues)
    for name, quantity, price, funding, cat, rev in zipped_items:
        if Item.objects.filter(event=event, name=name):
            continue
        funding = funding or 0
        # set correct category letter
        cat = cat.strip().upper()
        for tup in CATEGORIES:
            if tup[1].strip().upper() == cat:
                cat = tup[0]
                break
        # Remove unwanted commas for int parsing
        rev = rev.replace(",", "")

        if name:
            event.item_set.create(name=name,
                                  quantity=quantity,
                                  price_per_unit=price,
                                  funding_already_received=funding,
                                  category=cat,
                                  revenue=int(rev))

    # save questions

    # delete existing answers
    event.commonfollowupanswer_set.all().delete()
    event.followupanswer_set.all().delete()
    event.eligibilityanswer_set.all().delete()
    event.commonfreeresponseanswer_set.all().delete()
    event.freeresponseanswer_set.all().delete()

    # clear existing funders to re-add new ones
    event.applied_funders.clear()

    # create new answers and save funders
    # unchecked checkboxes will have neither answers nor funders
    # associated with them
    for k, v in POST.items():
        if k.startswith('eligibility'):
            q_id = re.search("[0-9]+", k).group(0)
            question = EligibilityQuestion.objects.get(id=q_id)
            event.eligibilityanswer_set.create(question=question,
                                               event=event, answer='Y')
        elif k.startswith('commonfollowup'):
            q_id = re.search("[0-9]+", k).group(0)
            question = CommonFollowupQuestion.objects.get(id=q_id)
            event.commonfollowupanswer_set.create(question=question,
                                                  event=event, answer=v)
        elif k.startswith('followup'):
            q_id = re.search("[0-9]+", k).group(0)
            question = FollowupQuestion.objects.get(id=q_id)
            event.followupanswer_set.create(question=question,
                                            event=event, answer=v)
        elif k.startswith('commonfreeresponse'):
            q_id = re.search("[0-9]+", k).group(0)
            question = CommonFreeResponseQuestion.objects.get(id=q_id)
            event.commonfreeresponseanswer_set.create(question=question,
                                                      event=event,
                                                      answer=v)
        elif k.startswith('freeresponse'):
            q_id = re.search("[0-9]+", k).group(0)
            question = FreeResponseQuestion.objects.get(id=q_id)
            event.freeresponseanswer_set.create(question=question,
                                                event=event, answer=v)
        elif k.startswith('funder'):
            funder_id = re.search("[0-9]+", k).group(0)
            funder = CFAUser.objects.get(id=funder_id)
            event.applied_funders.add(funder)


# GET  /
# upcoming events
@require_http_methods(["GET", "POST"])
def events(request):
    if not request.user.is_authenticated:
        return login(request)

    user = request.user
    # if the request type has GET query type, set it as the parameter
    sorted_type = request.GET.get('sort').strip() if 'sort' in request.GET else 'date'
    query_dict = {
        'event': 'name',
        'org': 'organizations',
        'submit': '-updated_at'
    }
    sort_by = query_dict[sorted_type] if sorted_type in query_dict else '-date'
    cfauser = user.profile
    two_weeks_ago = timezone.now().date() - timedelta(days=14)
    filter_val = request.GET.get('filter', '')
    app = Event.objects.filter()
    if len(filter_val) != 0:
        if filter_val == 'O':
            app = Event.objects.filter(date__lt=datetime.date.today() - datetime.timedelta(days=14))
        else:
            app = Event.objects.filter(date__gte=datetime.date.today() - datetime.timedelta(days=14))
            app = app.filter(status__in=filter_val)
    app = app.order_by(sort_by)
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1

    if user.is_staff and not user.username == "uacontingency":
        apps = app
    elif cfauser.is_requester:
        apps = app.filter(requester=cfauser)
    else:  # cfauser.is_funder
        apps = cfauser.event_applied_funders.order_by(sort_by)

    p = Paginator(apps, 10)
    return render(request, 'app/events.html',
                  {'apps': p.page(page).object_list,
                   'page_obj': p.page(page),
                   'page_range': p.page_range,
                   'page_length': len(p.page_range),
                   'filter': filter_val})


# GET  /new
# POST /new
@login_required
@require_http_methods(["GET", "POST"])
def event_new(request):
    """Form to create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    event = form.save(commit=False)
                    event.requester = request.user.profile
                    event.save()
                    save_from_form(event, request.POST)
                event.notify_funders(new=True)
                msg = u"Scheduled {} for {}!".format(event.name, event.date.strftime("%b %d, %Y"))
                messages.success(request, msg)
                return redirect(EVENTS_HOME)
            except IntegrityError:
                messages.error(request, "Please make sure your event name, date, and requester ID are UNIQUE!")
            except ValueError:
                messages.error(request, "Please make sure you have entered valid values for all numeric fields!")
        else:
            messages.error(request, "You have one or more errors in your application.")
    else:
        form = EventForm()

    context = {
        'form': form
    }

    return render(request, 'app/application-requester.html', context)


# GET  /1/edit
# POST /1/edit
@login_required
@requester_only
@require_http_methods(["GET", "POST"])
def event_edit(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.over:
        return redirect('event-show', event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            try:
                with transaction.atomic():
                    event = form.save()
                    save_from_form(event, request.POST)
                event.notify_funders(new=False)
                messages.success(request, u'Saved {}!'.format(event.name))
                return redirect(EVENTS_HOME)
            except IntegrityError:
                messages.error(request, "Please make sure your event name, date, and requester ID are UNIQUE!")
            except ValueError:
                messages.error(request, "Please make sure you have entered valid values for all numeric fields!")
        else:
            messages.error(request, "One or more errors occured while saving the application!")
    else:
        form = EventForm(instance=event)
    return render(request, 'app/application-requester.html', {'event': event, 'form': form})


# GET  /1
# POST /1
@authorization_required
@require_http_methods(["GET", "POST"])
def event_show(request, event_id):
    user = request.user
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':  # TODO: should really be PUT
        if user.profile.is_funder:
            grants = []
            for item in event.item_set.all():
                amount = request.POST.get("item_" + str(item.id), None)
                if amount:
                    amount = Decimal(amount)
                    grant, _ =\
                        Grant.objects.get_or_create(funder=user.profile,
                                                    item=item,
                                                    defaults={'amount': 0})
                    amount_funded = sum(grant.amount for grant in
                                        Grant.objects.filter(item=item))
                    amount_funded += item.funding_already_received
                    # if the funder gave too much,
                    # adjust the price to be only enough
                    if amount + amount_funded - grant.amount > item.total:
                        amount = item.total - amount_funded + grant.amount
                    # only append if the amount has changed
                    if grant.amount != amount:
                        grant.amount = amount
                        grant.save()
                        grants.append(grant)
            if grants:
                messages.success(request, "Saved grant!")
                # email the event requester indicating that they've been funded
                event.status = 'F'  # F for FUNDED
                event.save()
                event.notify_requester(grants)
                # try to notify osa, but osa is not guaranteed to exist
                try:
                    user.profile.notify_osa(event, grants)
                except smtplib.SMTPException:
                    pass
            if request.POST.get('new-comment'):
                messages.success(request, "Saved comment!")
                comment = Comment(comment=request.POST['new-comment'],
                                  funder=user.profile, event=event)
                comment.save()
            return redirect('event-show', event_id)
        else:
            return redirect(EVENTS_HOME)
    else:
        if 'id' in request.GET:
            event.shared_funder = \
                User.objects.get(id=request.GET['id']).profile
        return render(request, 'app/application-show.html', {'event': event})


# GET  /1/destroy
@login_required
@requester_only
def event_destroy(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponse(json.dumps({'event_id': event_id}),
                        content_type="application/json")

# GET /funders/1/edit
# POST /funders/1/edit
@login_required
def funder_edit(request, user_id):
    user = User.objects.get(pk=user_id)
    funder = user.profile
    if request.method == 'POST':
        # edit funder basic info.
        funder.funder_name = request.POST['fundername']
        funder.mission_statement = request.POST['missionstatement']
        funder.save()

        # delete removed free response questions.
        request_question_ids = \
            [int(re.search("[0-9]+", k).group(0)) for k, v in request.POST.items()
             if '_' in k and k.startswith('freeresponsequestion')]
        for question in funder.freeresponsequestion_set.all():
            if question.id not in request_question_ids:
                question.delete()

        # create new free response questions.
        for question in request.POST.getlist('freeresponsequestion'):
            if question:
                funder.freeresponsequestion_set.create(funder=funder,
                                                       question=question)

        # edit existing free response questions.
        for k, v in request.POST.items():
            if '_' in k and k.startswith('freeresponsequestion'):
                q_id = re.search("[0-9]+", k).group(0)
                question = FreeResponseQuestion.objects.get(id=q_id)
                question.question = v
                question.save()

        # recreate associated funder constraints.
        funder.funderconstraint_set.all().delete()
        for question_id in request.POST.getlist('funderconstraint'):
            if question_id:
                question = EligibilityQuestion.objects.get(id=question_id)
                funder.funderconstraint_set.create(question=question)

        # update cc emails
        funder.cc_emails.all().delete()
        for email in request.POST.getlist('cc_email'):
            try:
                validate_email(email)
                funder.cc_emails.create(email=email)
            except ValidationError:
                messages.warning(request, 'The invalid email address "{}" was not added.'.format(email))

        messages.success(request, 'Saved Info.')
        return redirect(EVENTS_HOME)
    elif request.method == 'GET':
        funder_questions = FreeResponseQuestion.objects.filter(funder_id=funder.id)
        eligibility_questions = EligibilityQuestion.objects.all()
        return render(
            request,
            'app/funder_edit.html',
            {
                'user': user,
                'funder_questions': funder_questions,
                'eligibility_questions': eligibility_questions
            }
        )
    else:
        return HttpResponseNotAllowed(['GET'])
