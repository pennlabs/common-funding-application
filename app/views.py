from decimal import Decimal
from datetime import datetime
import json
import re

import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from app.models import Event, Grant, Comment, User, FreeResponseQuestion, EligibilityQuestion


EVENTS_HOME = 'app.views.events'


def authorization_required(view):
    """Ensure only a permitted user can access an event.
    A user is permitted if:
      * They requested the event
      * They are a funder
      * They have a secret key to an event
    """
    def protected_view(request, event_id, *args, **kwargs):
        event = Event.objects.get(pk=event_id)
        try:
            key = request.GET['key']
        except KeyError:
            try:
                user = request.user.get_profile()
            except:
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
        user = request.user.get_profile()
        event = Event.objects.get(pk=event_id)
        if user.is_requester and user.requested(event):
            return view(request, event_id, *args, **kwargs)
        else:
            return redirect(EVENTS_HOME)
    return protected_view


# GET  /
# upcoming events
@login_required
def events(request):
    if request.method == 'GET':
        user = request.user
        #if the request type has GET query type, set it as the parameter
        sorted_type = request.GET.get('sort').strip() if 'sort' in request.GET else 'date'
        query_dict = {'event':'name',
                      'org' : 'organizations'
                      }
        sort_by = query_dict[sorted_type] if sorted_type in query_dict else '-date'
        cfauser = user.get_profile()
        app = Event.objects.filter(date__gt=datetime.today().date()).order_by(sort_by)
        if user.is_staff and not user.username == "uacontingency":
            apps = app
        elif cfauser.is_requester:
            apps = app.filter(requester=cfauser)
        else:  # cfauser.is_funder
            apps = cfauser.event_applied_funders.order_by(sort_by)
        return render_to_response('app/events.html',
                                  {'apps': apps},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])

# GET  /
# previous events
@login_required
def events_old(request):
    if request.method == 'GET':
        user = request.user
        cfauser = user.get_profile()
        if user.is_staff:
            apps = Event.objects.filter(date__lt= datetime.today().date()).order_by('-date')
        elif cfauser.is_requester:
            apps = Event.objects.filter(requester=cfauser).filter(date__lt= datetime.today().date()).order_by('-date')
        else:  # cfauser.is_funder
            apps = cfauser.event_applied_funders.order_by('-date')
        return render_to_response('app/events_old.html',
                                  {'apps': apps},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])


# GET  /new
# POST /new
@login_required
def event_new(request):
    """Form to create a new event."""
    if request.method == 'POST':
        if "submit-event" in request.POST:
            status = 'B'  # B for SUBMITTED
        else:
            status = 'S'  # S for SAVED

        date = datetime.strptime(request.POST['date'], '%m/%d/%Y')

        event = Event.objects.create(
            name=request.POST['name'],
            status=status,
            date=date,
            requester=request.user.get_profile(),
            location=request.POST['location'],
            organizations=request.POST['organizations'],
            contact_name = request.POST['contactname'],
            contact_email=request.POST['contactemail'],
            time=request.POST['time'],
            contact_phone=request.POST['contactphone'],
            anticipated_attendance=request.POST['anticipatedattendance'],
            advisor_email=request.POST['advisoremail'],
            advisor_phone=request.POST['advisorphone'],
            funding_already_received=request.POST['fundingalreadyreceived'],
        )
        event.save_from_form(request.POST)
        event.notify_funders(new=True)
        msg = "Scheduled %s for %s!" %\
            (event.name, event.date.strftime("%b %d, %Y"))
        messages.success(request, msg)
        return redirect(EVENTS_HOME)
    elif request.method == 'GET':
        return render_to_response('app/application-requester.html',
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])


# GET  /1/edit
# POST /1/edit
@login_required
@requester_only
def event_edit(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.locked:
        return redirect('app.views.event_show', event_id)
    if request.method == 'POST':
        if event.followup_needed:
            status = 'O'  # O for OVER
        elif "submit-event" in request.POST:
            status = 'B'  # B for SUBMITTED
        else:
            status = 'S'  # S for SAVED

        event.name = request.POST['name']
        event.status = status
        event.date = datetime.strptime(request.POST['date'], '%m/%d/%Y')
        event.organizations = request.POST['organizations']
        event.location = request.POST['location']
        event.time = request.POST['time']
        event.contact_name = request.POST['contactname']
        event.contact_email = request.POST['contactemail']
        event.contact_phone = request.POST['contactphone']
        event.anticipated_attendance = request.POST['anticipatedattendance']
        event.advisor_email = request.POST['advisoremail']
        event.advisor_phone = request.POST['advisorphone']
        event.funding_already_received = request.POST['fundingalreadyreceived']
        event.save()
        event.save_from_form(request.POST)
        event.notify_funders(new=False)
        messages.success(request, 'Saved %s!' % event.name)
        return redirect(EVENTS_HOME)
    elif request.method == 'GET':
        return render_to_response('app/application-requester.html',
                                  {'event': event},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])


# GET  /1
# POST /1
@authorization_required
def event_show(request, event_id):
    user = request.user
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':  # TODO: should really be PUT
        if user.get_profile().is_funder:
            grants = []
            for item in event.item_set.all():
                amount = request.POST.get("item_" + str(item.id), None)
                if amount:
                    amount = Decimal(amount)
                    grant, _ =\
                        Grant.objects.get_or_create(funder=user.get_profile(),
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
                    user.get_profile().notify_osa(event, grants)
                except smtplib.SMTPException:
                    pass
            if request.POST.get('new-comment', None):
                comment = Comment(comment=request.POST['new-comment'],
                                  funder=user.get_profile(), event=event)
                comment.save()
            return redirect(EVENTS_HOME)
        else:
            return redirect(EVENTS_HOME)
    elif request.method == 'GET':
        if 'id' in request.GET:
            event.shared_funder = \
                User.objects.get(id=request.GET['id']).get_profile()
        return render_to_response('app/application-show.html',
                                  {'event': event},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['POST'])


# GET  /1/destroy
@login_required
@requester_only
def event_destroy(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponse(json.dumps({'event_id': event_id}),
                        mimetype="application/json")

# GET /funders/1/edit
# POST /funders/1/edit
@login_required
def funder_edit(request, user_id):
    user = User.objects.get(pk=user_id)
    funder = user.get_profile()
    if request.method == 'POST':
        # edit funder basic info.
        funder.funder_name = request.POST['fundername']
        funder.mission_statement = request.POST['missionstatement']
        funder.save()

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

        messages.success(request, 'Saved Info.')
        return redirect(EVENTS_HOME)
    elif request.method == 'GET':
        funder_questions = FreeResponseQuestion.objects.filter(funder_id=funder.id)
        eligibility_questions = EligibilityQuestion.objects.all()
        return render_to_response('app/funder_edit.html',
                                  {'user': user,
                                   'funder_questions': funder_questions,
                                   'eligibility_questions': eligibility_questions },
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseNotAllowed(['GET'])
