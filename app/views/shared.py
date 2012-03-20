import os

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from sandbox_config import URL_ROOT


@login_required
def index(request):
  return redirect(os.path.join(URL_ROOT, 'apps'))


def login(request):
  if request.method == 'POST':
    username = request.POST['user']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
      auth_login(request, user)
      return redirect(os.path.join(URL_ROOT, 'apps'))
    else:
      return render_to_response('login.html',
                                {'login_failed': True},
                                context_instance=RequestContext(request))
  else:
    return render_to_response('login.html',
                              context_instance=RequestContext(request))


def logout(request):
  auth_logout(request)
  return redirect(URL_ROOT)
